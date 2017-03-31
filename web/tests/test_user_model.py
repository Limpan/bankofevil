import pytest
import time
import json
from app.models import User

def test_password_setter():
    u = User(password='secret')
    assert u.password_hash is not None


def test_no_password_getter():
    u = User(password='secret')
    with pytest.raises(AttributeError):
        u.password


def test_password_verification():
    u = User(password='cat')
    assert u.verify_password('cat')
    assert not u.verify_password('dog')


def test_password_salts_are_random():
    u1 = User(password='cat')
    u2 = User(password='cat')
    assert not u1.password_hash == u2.password_hash


def test_valid_auth_token(db):
    u1 = User(password='cat')
    db.session.add(u1)
    db.session.commit()
    token = u1.generate_auth_token()
    u2 = User.verify_auth_token(token)
    assert u1.id == u2.id


def test_invalid_auth_token():
    token = json.dumps({'id': 'bogus'})
    assert User.verify_auth_token(token) is None


def test_expired_auth_token():
    u = User(password='cat')
    token = u.generate_auth_token(expiration=0)
    time.sleep(1)
    assert User.verify_auth_token(token) is None
