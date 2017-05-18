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


def test_verify_pow_challenge():
    u = User(email='test@example.com', pow_challenge='1231ad79')
    assert u.verify_pow_challenge('52644813', '0000001ca483d104feb3c2da2efaa635a2f62b8c3cf22d0b3c39061300b93883')


def test_invalid_pow_challenge():
    u = User(email='test@example.com', pow_challenge='1231ad79')
    assert not u.verify_pow_challenge('4813', '0000001ca483d104feb3c2da2efaa635a2f62b8c3cf22d0b3c39061300b93883')
    assert not u.verify_pow_challenge('52644813', '0000001ca483d104fecf22d0b3c3906130b3c2da2efaa635a2f62b8c30b93883')


def test_refresh_pow_challenge():
    u = User(pow_challenge='1231ad79')
    assert u.pow_challenge == '1231ad79'
    u.refresh_pow_challenge()
    assert not u.pow_challenge == '1231ad79'
