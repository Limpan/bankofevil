#!/usr/bin/env python
import os
import click
from flask.cli import FlaskGroup


APP_FOLDER = 'app'

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


def create_app(info):
    from app import create_app
    return create_app(os.environ.get('CONFIG') or 'default')


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """This is a management script for the web application."""
    pass


@cli.command()
@click.option('--only', '-o', multiple=True)
@click.option('--coverage', 'with_coverage', is_flag=True)
@click.option('--no-html', is_flag=True)
@click.option('--no-report', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def test(with_coverage, no_html, no_report, verbose, only):
    """Run the tests."""
    if with_coverage:
        # Initialize coverage.py.
        import coverage
        COV = coverage.coverage(branch=True,
                                source=[APP_FOLDER])
        COV.start()

    # Decide what arguments to use.
    args = []
    if only:
        for name in only:
            args.append('tests/test_{}.py'.format(name))
    else:
        args.append('tests')

    if verbose:
        args.append('-v')

    # Invoke pytest
    import pytest
    exit_code = pytest.main(args)

    if with_coverage:
        # Sum up the results of the code coverage analysis.
        COV.stop()
        COV.save()

        if not no_html:
            # Generate HTML report and move to tmp directory.
            import os
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)

        if not no_report:
            # Show the report and clean up.
            click.echo('\nCoverage Summary\n{}'.format('=' * 70))
            COV.report()
            COV.erase()

    raise SystemExit(exit_code)


@cli.command()
@click.option('--all', is_flag=True)
@click.option('--stats', is_flag=True)
def lint(all, stats):
    """Run the linter."""
    if all:
        click.echo('Running linter (including skeleton code).')
        args = ['flake8', '.']
    else:
        click.echo('Running Linter...')
        args = ['flake8', APP_FOLDER]

    if stats:
        args.extend(['--statistics', '-qq'])

    exit_code = os.system(' '.join(args))

    raise SystemExit(exit_code)


@cli.command()
@click.option('--builder', default='html', help='Sphinx builder to use.')
def sphinx(builder):
    """Build docs with sphinx."""
    cmd = 'sphinx-build -b {builder} docs/source docs/build'.format(builder=builder)

    exit_code = os.system(cmd)
    raise SystemExit(exit_code)


@cli.command()
def deploy():
    """Deploy application."""
    from flask_migrate import upgrade

    # Migrate database to latest revision.
    upgrade()


@cli.command()
@click.option('--zeroes', default=4, help='Number of leading zeroes required.')
@click.option('--challenge', default='', help='Challenge string. Usually ')
@click.option('--email', default='test@example.com', help='Email used in construction of problem.')
def generate(email, challenge, zeroes):
    """Generate proof-of-work-token."""
    import hashlib
    solution = ' ' * 64
    count = 0
    while solution[:zeroes] != '0' * zeroes:
        count += 1
        solution = hashlib.sha256('{}-{}-{}'.format(email, challenge, count).encode('UTF-8')).hexdigest()

    output = '''
### Solution found after {count} tries. ###
 e-mail: {email}
 challenge: {challenge}
 number_of_zeroes (difficulty): {zeroes}

------------------------------------------------------------------------------
       {solution}
------------------------------------------------------------------------------
'''

    click.echo(output.format(solution=solution, count=count, challenge=challenge, zeroes=zeroes, email=email))


if __name__ == '__main__':
    cli()
