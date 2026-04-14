import pytest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.models import db, Bug

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_bug(client):
    response = client.post('/api/bugs', json={
        "title": "Test Bug",
        "description": "This is a test bug"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Test Bug"
    assert data['status'] == "OPEN"

def test_invalid_status_transition(client):
    # Create bug
    res = client.post('/api/bugs', json={"title": "T1", "description": "D1"})
    bug_id = res.get_json()['id']

    # Try OPEN -> RESOLVED (Invalid, must go through IN_PROGRESS)
    # Our flow: OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED
    response = client.patch(f'/api/bugs/{bug_id}', json={"status": "RESOLVED"})
    assert response.status_code == 400
    assert "Invalid transition" in response.get_json()['error']

def test_valid_status_transition_flow(client):
    res = client.post('/api/bugs', json={"title": "T1", "description": "D1"})
    bug_id = res.get_json()['id']

    # OPEN -> IN_PROGRESS
    res = client.patch(f'/api/bugs/{bug_id}', json={"status": "IN_PROGRESS"})
    assert res.status_code == 200
    assert res.get_json()['status'] == "IN_PROGRESS"

    # IN_PROGRESS -> RESOLVED
    res = client.patch(f'/api/bugs/{bug_id}', json={"status": "RESOLVED"})
    assert res.status_code == 200
    assert res.get_json()['status'] == "RESOLVED"

    # RESOLVED -> CLOSED (Missing notes)
    res = client.patch(f'/api/bugs/{bug_id}', json={"status": "CLOSED"})
    assert res.status_code == 400
    assert "Notes required" in res.get_json()['error']

    # RESOLVED -> CLOSED (With notes)
    res = client.patch(f'/api/bugs/{bug_id}', json={
        "status": "CLOSED",
        "resolution_notes": "Fixed it"
    })
    assert res.status_code == 200
    assert res.get_json()['status'] == "CLOSED"

def test_missing_fields(client):
    response = client.post('/api/bugs', json={"title": ""})
    assert response.status_code == 400
