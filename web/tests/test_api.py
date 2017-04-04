import pytest
import json
from flask import url_for
from app.models import User, Account


def get_token_headers(email):
    u = User.query.filter_by(email=email).first()
    return {
        'Authorization': 'Token {}'.format(u.generate_auth_token()),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def test_list_accounts(app, db):
    user = User(email='test@example.com', password='cat')
    db.session.add(user)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.accounts'))
    assert rv.data  # Make something better
    assert False
