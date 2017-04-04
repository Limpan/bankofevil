import pytest
import base64
import json
from flask import url_for
from werkzeug.datastructures import Headers
from app.models import User


def test_home_page(app):
    rv = app.test_client().get(url_for('main.index'))
    assert rv.status_code == 200
    assert b'Bank of Phony' in rv.data


def test_token_endpoint(app, db):
    u = User(email='test@example.com', password='cat')
    db.session.add(u)
    db.session.commit()

    client = app.test_client()
    auth = 'Basic {}'.format(base64.b64encode(b'test@example.com:cat').decode('ascii'))
    rv = client.get(url_for('api.get_auth_token'),
                    headers={'Authorization': auth})
    data = json.loads(rv.data)
    assert u == User.verify_auth_token(data['token'])
