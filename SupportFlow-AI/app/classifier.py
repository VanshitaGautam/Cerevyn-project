"""Explainable keyword-based baseline classifier for support tickets."""
import re

CATEGORY_RULES = {
    "Billing": [
        "payment", "invoice", "refund", "charged", "billing",
        "subscription", "duplicate charge", "charged twice", "credit card",
        "renewal fee", "receipt", "overcharged",
    ],
    "Technical": [
        "crash", "bug", "error", "not working", "application",
        "upload", "outage", "slow", "server", "loading",
        "screen freezes", "exception", "failed to load",
    ],
    "Access": [
        "login", "log in", "password", "locked out", "sign in",
        "authentication", "account access", "reset password",
        "cannot access my account", "two-factor", "verification code",
    ],
    "General": [
        "product information", "business hours", "general question",
        "pricing information", "hello", "greetings", "feature request",
        "how does", "documentation", "available in",
    ],
}

TEAM_MAP = {
    "Billing": "Billing Team",
    "Technical": "Technical Support",
    "Access": "Account Support",
    "General": "Customer Support",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def classify_ticket(message: str) -> dict:
    text = normalize(message)
    scores = {
        category: sum(1 for keyword in keywords if keyword in text)
        for category, keywords in CATEGORY_RULES.items()
    }
    highest_score = max(scores.values())
    winners = [
        category for category, score in scores.items()
        if score == highest_score and score > 0
    ]

    # No clear winning category means a person must triage it.
    if highest_score == 0 or len(winners) != 1:
        category = "General"
        requires_review = True
    else:
        category = winners[0]
        requires_review = False

    critical_terms = [
        "complete outage", "all users affected", "system down",
        "security breach", "data breach",
    ]
    high_terms = [
        "cannot access", "charged twice", "duplicate charge",
        "urgent", "locked out", "production is down",
    ]

    if any(term in text for term in critical_terms):
        priority = "Critical"
    elif any(term in text for term in high_terms):
        priority = "High"
    elif category == "General":
        priority = "Low"
    else:
        priority = "Medium"

    if requires_review:
        priority = "Medium"

    return {
        "category": category,
        "priority": priority,
        "assigned_team": TEAM_MAP[category],
        "summary": message.strip()[:160],
        "draft_response": (
            f"Thank you for contacting support about your {category.lower()} issue. "
            "A support team member will review your request and follow up with the "
            "appropriate next steps."
        ),
        "requires_review": requires_review,
    }
