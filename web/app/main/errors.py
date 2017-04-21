from flask import render_template, request, jsonify, current_app
from . import main


@main.app_errorhandler(401)
def unauthorized(e):
    current_app.logger.warning('Unauthorized access attempt at route %s (%s).' % (request.path, request.method))
    return render_template('401.html'), 401
