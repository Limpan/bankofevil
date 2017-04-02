from flask import render_template, request, jsonify, current_app
from . import main


@main.app_errorhandler(401)
def unauthorized(e):
    current_app.logger.warning('Unauthorized access attempt at route %s (%s).' % (request.path, request.method))
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({ 'error': 'unauthorized' })
        response.status_code = 401
        return response
    return render_template('401.html'), 401
