from flask import render_template, request, jsonify, current_app
from . import api


@api.errorhandler(401)
def unauthorized(e):
    return {'errors': [{ 'status': '401', 'title': 'Unauthorized' }]}, 401


@api.errorhandler(404)
def unauthorized(e):
    return {'errors': [{ 'status': '404', 'title': 'Unauthorized' }]}, 404
