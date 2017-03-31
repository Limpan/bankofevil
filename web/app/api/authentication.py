from flask import current_app, jsonify
from flask_login import login_required
from . import api
from .. import login_manager


@login_manager.header_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    api_key = api_key.replace('Token', '', 1).strip()
    return User.verify_auth_token(api_key)


@api.route('/token')
@login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
