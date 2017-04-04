import pytest
from flask import url_for
from app.models import User


def test_register_user(app, db):
    client = app.test_client()
    rv = client.post(url_for('main.index'),
                     data=dict(email='test@example.com', password='cat'))
    u = User.query.filter_by(email='test@example.com').first()
    assert u
    assert u.verify_password('cat')
