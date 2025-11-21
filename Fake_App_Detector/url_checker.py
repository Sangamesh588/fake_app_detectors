import json
from data import APP_INDEX
from url_utils import package_from_play_store_url
from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)
from scoring import risk_score

def check_url(url: str) -> dict:
    pkg = package_from_play_store_url(url)
    if pkg is None:
        return {
            "url": url,
            "found": False,
            "risk": None,
            "reason": ["Not a valid Google Play app URL (no id= parameter)."]
        }

    app = APP_INDEX.get(pkg)
    if app is None:
        return {
            "url": url,
            "packageId": pkg,
            "found": False,
            "risk": None,
            "reason": [
                "Package id not present in our curated dataset.",
                "In production, this step would fetch metadata from Play Store and re-run detection."
            ]
        }

    name_sim = name_similarity(app)
    pkg_sim = package_similarity(app)
    pub_ok = publisher_match(app)
    text_score = text_suspicion_score(app)
    perm_score = permission_suspicion_score(app)
    risk = risk_score(app)

    reasons = [
        f"Name similarity with official PhonePe app: {name_sim}",
        f"Package name similarity with official PhonePe app: {pkg_sim}",
        f"Text suspicion score (keywords): {text_score}",
        f"Permission suspicion score: {perm_score}",
    ]
    if pub_ok:
        reasons.append("Publisher matches official PhonePe publisher")
    else:
        reasons.append("Publisher does NOT match official PhonePe publisher")

    return {
        "url": url,
        "packageId": pkg,
        "found": True,
        "risk": risk,
        "reason": reasons,
    }

def main():
    url = input("Enter Play Store URL: ").strip()
    result = check_url(url)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
