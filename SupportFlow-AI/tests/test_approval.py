def test_approve_ticket(client):
    created = client.post("/tickets", json={
        "ticket_id": "TEST-APPROVE",
        "message": "I need a refund for my invoice.",
    })
    assert created.status_code == 201
    response = client.post("/tickets/TEST-APPROVE/approve")
    assert response.status_code == 200
    assert response.json()["status"] == "READY"


def test_cannot_approve_twice(client):
    client.post("/tickets", json={
        "ticket_id": "TEST-DOUBLE",
        "message": "I need a refund for my invoice.",
    })
    assert client.post("/tickets/TEST-DOUBLE/approve").status_code == 200
    assert client.post("/tickets/TEST-DOUBLE/approve").status_code == 409


def test_approve_missing_ticket(client):
    assert client.post("/tickets/UNKNOWN/approve").status_code == 404
