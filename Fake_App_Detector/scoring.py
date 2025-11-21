from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)

def risk_score(app):
    name_sim = name_similarity(app)
    pkg_sim = package_similarity(app)
    pub_ok = publisher_match(app)
    text_score = text_suspicion_score(app)
    perm_score = permission_suspicion_score(app)

    score = 0.0

    score += 0.20 * (100 - name_sim)
    score += 0.20 * (100 - pkg_sim)
    score += 0.30 * text_score
    score += 0.30 * perm_score

    if pub_ok:
        score -= 40

    score = max(0, min(100, score))
    return round(score, 2)
