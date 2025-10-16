import json
import pytest
from app import create_app, db
from app.models import Account

@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    # use in-memory or tmp sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_account_and_get(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "9999999999",
        "dob": "1990-01-01",
        "balance": 100.0
    }
    rv = client.post('/api/accounts', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['email'] == payload['email']

    # get list
    rv2 = client.get('/api/accounts')
    assert rv2.status_code == 200
    lst = rv2.get_json()
    assert len(lst) == 1
