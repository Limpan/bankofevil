from flask import render_template
from . import main
from .forms import RegisterForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default application route."""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('Creating user %()s' % user)
    return render_template('index.html', form=form)
