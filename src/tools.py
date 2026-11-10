"""Deterministic tools available to agents (outputs are logged in the audit trail)."""


def detector_consistency_check(traffic_ratio, kpi_drop_pct, detector_attack_share,
                               ratio_threshold=5.0, kpi_threshold=10.0, attack_share_floor=0.01):
    """Flag a *silent failure* of an AI intrusion detector.

    Idea from the author's MSc thesis: a DDoS detector with MCC 0.9996 on
    CIC-IDS2017 caught only 23 of 479,497 DDoS flows when applied zero-shot to
    CIC-DDoS2019, and gave no warning. A detector should be cross-checked
    against independent network KPIs: if traffic and service KPIs clearly show an
    anomaly while the detector reports (almost) nothing, the detector's output
    should not be trusted and humans must be alerted.
    """
    anomaly = traffic_ratio >= ratio_threshold or kpi_drop_pct >= kpi_threshold
    silent = detector_attack_share < attack_share_floor
    if anomaly and silent:
        verdict = ("ALERT: possible silent failure of the AI detector. Network KPIs show a major anomaly "
                   f"(traffic x{traffic_ratio:g}, KPI drop {kpi_drop_pct:g}%) but the detector labels only "
                   f"{detector_attack_share:.4%} of flows as attacks. Likely distribution shift or unseen attack "
                   "type. Do not rely on the detector; switch to manual/rule-based mitigation and escalate.")
    elif anomaly:
        verdict = "Detector output is consistent with the network anomaly."
    else:
        verdict = "No network-level anomaly; detector output not contradicted."
    return {"anomaly": anomaly, "detector_silent": silent, "verdict": verdict,
            "inputs": {"traffic_ratio": traffic_ratio, "kpi_drop_pct": kpi_drop_pct,
                       "detector_attack_share": detector_attack_share}}


TOOLS = {"detector_consistency_check": detector_consistency_check}
