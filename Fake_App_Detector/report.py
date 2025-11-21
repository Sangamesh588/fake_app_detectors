from data import OFFICIAL_APP
from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)
from scoring import risk_score

def build_evidence(app: dict) -> dict:
    """
    Build an evidence object for a candidate app.
    """
    return {
        "official_app_name": OFFICIAL_APP["name"],
        "candidate_app_name": app["name"],
        "candidate_package": app["package"],
        "candidate_publisher": app["publisher"],
        "scores": {
            "name_similarity": name_similarity(app),
            "package_similarity": package_similarity(app),
            "publisher_match": publisher_match(app),
            "text_suspicion": text_suspicion_score(app),
            "permission_suspicion": permission_suspicion_score(app),
            "risk_score": risk_score(app),
        },
    }

def generate_takedown_email(evidence: dict) -> str:
    """
    Generate a human-readable takedown email based on the evidence.
    """
    app_name = evidence["candidate_app_name"]
    package = evidence["candidate_package"]
    publisher = evidence["candidate_publisher"]
    s = evidence["scores"]

    return f"""
To: Google Play Support
Subject: Urgent takedown request – Fake app impersonating PhonePe

Dear Google Play Team,

We have identified a suspicious app that appears to be impersonating the official PhonePe application.

App details:
- Name: {app_name}
- Package: {package}
- Publisher: {publisher}

Automated analysis:
- Name similarity to official PhonePe app: {s['name_similarity']:.2f}
- Package similarity to official PhonePe package: {s['package_similarity']:.2f}
- Publisher match with official publisher: {s['publisher_match']}
- Text suspicion score (scammy keywords): {s['text_suspicion']:.2f}
- Permission suspicion score (dangerous permissions): {s['permission_suspicion']:.2f}
- Overall risk score (0–100): {s['risk_score']:.2f}

Based on these signals, we believe this app may mislead users and could be used for fraud.

This is part of an academic prototype for detecting fake apps impersonating financial brands.

Regards,
[Your Name]
[Your College]
"""
