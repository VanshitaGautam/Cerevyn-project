from app.classifier import classify_ticket


def test_billing_classification():
    assert classify_ticket("I need a refund for my payment.")["category"] == "Billing"


def test_access_classification():
    assert classify_ticket("I cannot log in because I forgot my password.")["category"] == "Access"


def test_technical_classification():
    assert classify_ticket("The application crashes when I upload a file.")["category"] == "Technical"


def test_unknown_message_is_flagged():
    assert classify_ticket("Please help me with something.")["requires_review"] is True
