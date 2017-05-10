import pytest
import json
from flask import url_for
from app.models import User, Account


def get_token_headers(email):
    u = User.query.filter_by(email=email).first()
    return {
        'Authorization': 'Token {}'.format(u.generate_auth_token().decode('UTF-8')),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def test_show_single_account(app, db):
    user = User(email='test@example.com', password='cat')
    account = Account(number='34564123', balance=1000)
    user.accounts = [account]
    db.session.add(user)
    db.session.add(account)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.accounts', account_id='34564123'), headers=get_token_headers('test@example.com'))
    data = json.loads(rv.data)
    print(data)
    assert data['account'] == '34564123'
    assert data['balance'] == 1000


def test_list_single_account(app, db):
    user = User(email='test@example.com', password='cat')
    account = Account(number='92142030', balance=1000)
    user.accounts = [account]
    db.session.add(user)
    db.session.add(account)
    db.session.commit()

    client = app.test_client()
    rv = client.get(url_for('api.accounts'), headers=get_token_headers('test@example.com'))
    accounts = sorted(json.loads(rv.data)['data'], key=lambda x: x['number'])
    assert len(accounts) == 1
    assert accounts[0]['number'] == '92142030'
    assert accounts[0]['balance'] == 1000


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
    accounts = sorted(json.loads(rv.data)['data'], key=lambda x: x['number'])
    assert len(accounts) == 2
    assert accounts[0]['number'] == '14054320'
    assert accounts[0]['balance'] == 1000
    assert accounts[1]['number'] == '24570434'
    assert accounts[1]['balance'] == 500
