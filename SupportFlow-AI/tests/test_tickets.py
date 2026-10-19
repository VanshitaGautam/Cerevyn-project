def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_billing_ticket(client):
    response = client.post("/tickets", json={
        "ticket_id": "TEST-001",
        "message": "I was charged twice for my subscription.",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Billing"
    assert data["priority"] == "High"
    assert data["assigned_team"] == "Billing Team"
    assert data["status"] == "PENDING_REVIEW"


def test_duplicate_ticket_id(client):
    payload = {"ticket_id": "TEST-002", "message": "Please explain my invoice payment."}
    assert client.post("/tickets", json=payload).status_code == 201
    assert client.post("/tickets", json=payload).status_code == 409


def test_empty_message_rejected(client):
    response = client.post("/tickets", json={"ticket_id": "TEST-003", "message": ""})
    assert response.status_code == 422


def test_ambiguous_ticket_needs_review(client):
    response = client.post("/tickets", json={
        "ticket_id": "TEST-004",
        "message": "I need some help with something.",
    })
    assert response.status_code == 201
    assert response.json()["requires_review"] is True
    assert response.json()["status"] == "NEEDS_REVIEW"


def test_get_missing_ticket(client):
    assert client.get("/tickets/DOES-NOT-EXIST").status_code == 404
