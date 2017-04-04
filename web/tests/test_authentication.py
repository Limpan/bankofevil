import pytest
import base64
import json
from flask import url_for
from app.models import User


def api_headers(email, password):
    return {
        'Authorization': 'Basic {}'.format(base64.b64encode('{}:{}'.format(email, password).encode('UTF-8')).decode('UTF-8')),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def test_home_page(app):
    rv = app.test_client().get(url_for('main.index'))
    assert rv.status_code == 200
    assert b'Bank of Phony' in rv.data


def test_token_endpoint(app, db):
    u = User(email='test@example.com', password='cat')
    db.session.add(u)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.get_auth_token'),
                    headers=api_headers('test@example.com', 'cat'))
    data = json.loads(rv.data)
    assert data.get('token')
    assert u == User.verify_auth_token(data['token'])


def test_token_endpoint_unauthorized(app, db):
    u = User(email='test@example.com', password='cat')
    db.session.add(u)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.get_auth_token'),
                    headers=api_headers('test@example.com', 'dog'))
    assert rv.status_code == 401
    rv = client.get(url_for('api.get_auth_token'),
                    headers=api_headers('test@example.net', 'cat'))
    assert rv.status_code == 401
