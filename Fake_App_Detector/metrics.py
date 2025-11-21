from data import CANDIDATE_APPS
from scoring import risk_score
from labels import LABELS

THRESHOLD = 40  # change threshold here

def main():
    tp = fp = tn = fn = 0

    print("Per-app diagnostics:\n")
    for app in CANDIDATE_APPS:
        pkg = app["package"]
        true_label = LABELS.get(pkg, 0)
        risk = risk_score(app)
        pred_label = 1 if risk >= THRESHOLD else 0

        print(f"- package={pkg} | risk={risk} | true={true_label} | pred={pred_label}")

        if true_label == 1 and pred_label == 1:
            tp += 1
        elif true_label == 0 and pred_label == 0:
            tn += 1
        elif true_label == 0 and pred_label == 1:
            fp += 1
        elif true_label == 1 and pred_label == 0:
            fn += 1

    print("\nConfusion Matrix:")
    print(f"TP: {tp}, FN: {fn}")
    print(f"FP: {fp}, TN: {tn}")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"Threshold used: {THRESHOLD}")

if __name__ == "__main__":
    main()
