import json
from data import CANDIDATE_APPS
from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)

def get_results():
    results = []

    for app in CANDIDATE_APPS:
        # 1) calculate signals
        name_sim = name_similarity(app)
        pkg_sim = package_similarity(app)
        pub_ok = publisher_match(app)
        text_score = text_suspicion_score(app)
        perm_score = permission_suspicion_score(app)

        # 2) risk is still TEMP dummy (we'll compute real risk in the next step)
        risk = 0

        # 3) build reasons list
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

        # 4) build one result item in frontend format
        result_item = {
            "appName": app["name"],
            "packageId": app["package"],
            "risk": risk,
            "reason": reasons
        }
        results.append(result_item)

    return {"results": results}

def main():
    print("Running backend...\n")
    output = get_results()
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
