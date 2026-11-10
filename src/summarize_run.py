"""Compute audit metrics for a run folder and write metrics.json + summary.md.

Usage: python src/summarize_run.py outputs/<run_folder>
"""
import json
import sys
from collections import Counter
from pathlib import Path


def norm(s):
    return " ".join(str(s).lower().split())[:80]


def main(run_dir):
    run = Path(run_dir)
    recs = [json.loads(l) for l in open(run / "audit_log.jsonl", encoding="utf-8")]
    calls = [r for r in recs if r["type"] in ("agent_decision", "coordinator_brief")]
    tools = [r for r in recs if r["type"] == "tool_call"]
    cites = [c for r in calls for c in r.get("citation_check", [])]
    status = Counter(c["status"] for c in cites)
    sources_cited = Counter(c["ref"].split()[0] for c in cites if c["status"] == "verified")
    gaps = []
    for r in calls:
        p = r.get("parsed") or {}
        gaps += [norm(g) for g in (p.get("gaps") or []) if isinstance(g, str)]
        gaps += [norm(g.get("gap")) for g in (p.get("policy_gaps") or []) if isinstance(g, dict) and g.get("gap")]
    routed = sum(len(r.get("inbox", [])) for r in calls if r["type"] == "agent_decision")
    lat = [r["llm"]["latency_s"] for r in calls]
    m = {
        "run": run.name,
        "llm_calls": len(calls),
        "agent_decisions": sum(r["type"] == "agent_decision" for r in calls),
        "coordinator_briefs": sum(r["type"] == "coordinator_brief" for r in calls),
        "tool_calls": len(tools),
        "valid_json": sum(r.get("parsed") is not None for r in calls),
        "messages_routed_between_agents": routed,
        "citations_total": len(cites),
        "citations_by_status": dict(status),
        "citation_verified_rate": round(status.get("verified", 0) / len(cites), 3) if cites else None,
        "distinct_sources_cited_verified": dict(sources_cited),
        "gap_statements_total": len(gaps),
        "gap_statements_distinct": len(set(gaps)),
        "mean_latency_s": round(sum(lat) / len(lat), 1) if lat else None,
        "total_llm_minutes": round(sum(lat) / 60, 1),
    }
    (run / "metrics.json").write_text(json.dumps(m, indent=2), encoding="utf-8")
    lines = [f"# Run summary: {run.name}", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in m.items() if k != "run"]
    (run / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(m, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
