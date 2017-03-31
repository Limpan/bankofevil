import pytest
from flask import url_for
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
    rv = client.get(url_for('api.get_auth_token'),
                    headers={'Authorization': 'Basic test@example.com:cat'})
    token = rv.json['token']
    assert u == User.verify_auth_token(token)
