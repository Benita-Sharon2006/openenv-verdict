def calculate_reward(
    cases, evidence_list, witnesses, courtroom,
    support, advanced, step, max_steps
) -> float:
    """
    12-dimensional reward signal, clamped to [0.01, 0.99].
    """
    from app.systems.case_management import get_case_score
    from app.systems.evidence_locker import get_evidence_score
    from app.systems.witness_management import get_witness_score
    from app.systems.courtroom import get_courtroom_score
    from app.systems.support_systems import get_support_score
    from app.systems.advanced_systems import get_advanced_score

    case_score      = get_case_score(cases)
    evidence_score  = get_evidence_score(evidence_list)
    witness_score   = get_witness_score(witnesses)
    courtroom_score = get_courtroom_score(courtroom)
    support_score   = get_support_score(support)
    advanced_score  = get_advanced_score(advanced)

    reputation    = support.get("firm_reputation", 0.5)
    client_trust  = support.get("client_trust", 0.5)
    media         = support.get("media_sentiment", 0.5)
    judge_mood    = courtroom.get("judge_mood", 0.5)
    jury_sentiment = courtroom.get("jury_sentiment", 0.5)
    efficiency    = max(0.0, 1.0 - step / max_steps)

    weighted = (
        case_score      * 0.20 +
        evidence_score  * 0.15 +
        witness_score   * 0.12 +
        courtroom_score * 0.12 +
        support_score   * 0.10 +
        advanced_score  * 0.08 +
        reputation      * 0.06 +
        client_trust    * 0.06 +
        media           * 0.04 +
        judge_mood      * 0.03 +
        jury_sentiment  * 0.02 +
        efficiency      * 0.02
    )

    sla_breaches = sum(1 for c in cases if c.get("expired") and not c["closed"])
    penalty = sla_breaches * 0.04

    final = weighted - penalty
    return round(max(0.01, min(0.99, final)), 4)