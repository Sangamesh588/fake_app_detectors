from data import CANDIDATE_APPS
from scoring import risk_score
from report import build_evidence, generate_takedown_email

def main():
    # Pick the most suspicious app based on risk score
    sorted_apps = sorted(CANDIDATE_APPS, key=risk_score, reverse=True)
    top_app = sorted_apps[0]

    evidence = build_evidence(top_app)

    print("Most suspicious app evidence:\n")
    print(evidence)

    print("\nGenerated takedown email:\n")
    print(generate_takedown_email(evidence))

if __name__ == "__main__":
    main()
