import base64
from flask import current_app, jsonify
from flask_login import login_required, current_user
from . import api
from .. import login_manager
from ..models import User


@login_manager.request_loader
def load_user_from_request(request):
    auth = request.headers.get('Authorization')
    if not auth:
        return None

    # Try to login with token...
    token = auth.replace('Token', '', 1).strip()
    user = User.verify_auth_token(token)
    if user:
        return user

    # Try to login using basic auth...
    credentials = auth.replace('Basic', '', 1)
    try:
         email, password = base64.b64decode(credentials).split(b':', 1)
         current_app.logger.debug('%s, %s' % (email, password))
    except:
        return None

    user = User.query.filter_by(email=email.decode('UTF-8')).first()
    if user and user.verify_password(password):
        return user

    return None


@api.route('/token')
@login_required
def get_auth_token():
    token = current_user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
