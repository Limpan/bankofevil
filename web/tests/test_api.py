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
    account_a = Account(number='14054320', balance=1000)
    account_b = Account(number='24570434', balance=500)
    user.accounts = [account_a, account_b]
    db.session.add(user)
    db.session.add(account_a)
    db.session.add(account_b)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.accounts'), headers=get_token_headers('test@example.com'))
    data = json.loads(rv.data)
    assert data.accounts
