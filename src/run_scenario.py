"""Run a chunked, multi-agent incident scenario with full audit logging.

Coordination protocol (one round):
  1. The scenario releases new events to specific agents only (information asymmetry).
  2. Tools requested by the scenario run first; their results are added to that agent's events.
  3. Each agent with new events or messages retrieves policy passages from its own KB slice,
     then returns a structured JSON decision (assessment, reasoning steps, actions, cited
     policy references, requests to other agents, gaps).
  4. Requests are routed to the addressed agents' inboxes for the next round.
  5. The Policy & Legal Adviser reads all outputs, retrieves from the full KB, and publishes a
     brief (conflicts, unclear responsibilities, policy and standards gaps). The brief is
     broadcast to all agents in the next round.
Every LLM call is written to audit_log.jsonl with inputs, retrieved sources, prompt hash,
raw output, parsed output and a citation check.

Usage:
  python src/run_scenario.py --kb kb/index --model <path to .gguf> \
      --scenario scenarios/ddos_mobile_operator.json --out outputs
"""
import argparse
import hashlib
import json
import time
from pathlib import Path

from agents import ROLES, ADVISER, ADVISER_THEMES, FOCUS, agent_messages, adviser_messages, check_citations
from kb import KnowledgeBase
from llm import LLM, parse_json
from tools import TOOLS


def call_llm(llm, messages, retries=1, max_tokens=None):
    raw, meta = llm.chat(messages, json_mode=True, max_tokens=max_tokens)
    parsed, err = parse_json(raw)
    attempts = 1
    while parsed is None and attempts <= retries:
        raw, meta = llm.chat(messages + [{"role": "assistant", "content": raw[:1500]},
                                         {"role": "user", "content": "Your answer was not valid JSON (possibly too long). Return only a shorter, complete JSON object."}],
                             max_tokens=max_tokens)
        parsed, err = parse_json(raw)
        attempts += 1
    meta["attempts"], meta["parse_error"] = attempts, err
    return raw, parsed, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--backend", default="llamacpp", choices=["llamacpp", "openai"])
    ap.add_argument("--model", help="path to .gguf (llamacpp) or model name (openai)")
    ap.add_argument("--base-url", help="OpenAI-compatible endpoint for --backend openai")
    ap.add_argument("--top-k", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=700)
    ap.add_argument("--rounds", type=int, default=0, help="run only the first N rounds (0 = all)")
    args = ap.parse_args()

    scenario = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    run_id = time.strftime("run_%Y%m%d_%H%M%S")
    out = Path(args.out) / run_id
    out.mkdir(parents=True, exist_ok=True)

    kb = KnowledgeBase(args.kb)
    if args.backend == "llamacpp":
        llm = LLM("llamacpp", model_path=args.model, max_tokens=args.max_tokens)
    else:
        llm = LLM("openai", base_url=args.base_url, model_name=args.model, max_tokens=args.max_tokens)

    run_config = {"run_id": run_id, "scenario": scenario["id"], "backend": args.backend, "model": llm.model_id,
                  "temperature": llm.temperature, "seed": llm.seed, "top_k": args.top_k,
                  "kb_config": kb.config, "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    (out / "run_config.json").write_text(json.dumps(run_config, indent=2), encoding="utf-8")

    audit = open(out / "audit_log.jsonl", "w", encoding="utf-8")
    transcript = [f"# Transcript: {scenario['title']}\n", f"Run `{run_id}` · model `{llm.model_id}` · "
                  f"KB {kb.config['n_chunks']} chunks\n", f"_Setting:_ {scenario['setting']}\n"]
    inboxes = {k: [] for k in ROLES}
    brief = None
    all_briefs, earlier_gaps = [], []
    rounds = scenario["rounds"][: args.rounds or None]

    def log(rec):
        audit.write(json.dumps(rec, ensure_ascii=False) + "\n")
        audit.flush()

    for r_idx, rnd in enumerate(rounds, start=1):
        sim_time = rnd["sim_time"]
        transcript.append(f"\n## Round {r_idx} ({sim_time})\n")
        round_outputs = {}
        for role in ROLES:
            events = list(rnd.get("events", {}).get(role, []))
            tool_spec = rnd.get("tool_calls", {}).get(role)
            if tool_spec:
                result = TOOLS[tool_spec["tool"]](**tool_spec["args"])
                log({"run_id": run_id, "round": r_idx, "sim_time": sim_time, "agent": role, "type": "tool_call",
                     "tool": tool_spec["tool"], "args": tool_spec["args"], "result": result,
                     "ts": time.strftime("%H:%M:%S")})
                events.append(f"TOOL {tool_spec['tool']}: {result['verdict']}")
            inbox = inboxes[role]
            if not events and not inbox:
                continue
            # retrieval query = round theme + the agent's mandate focus + what it just learned
            query = " ".join([rnd.get("query_hint", ""), FOCUS[role]] + events + [m["text"] for m in inbox])
            hits = kb.search(query, top_k=args.top_k, allowed_sources=ROLES[role]["sources"])
            messages = agent_messages(role, sim_time, events, inbox, brief, hits)
            raw, parsed, meta = call_llm(llm, messages)
            citations = check_citations(parsed, hits)
            log({"run_id": run_id, "round": r_idx, "sim_time": sim_time, "agent": role, "type": "agent_decision",
                 "events_received": events, "inbox": inbox, "brief_received": bool(brief),
                 "retrieval_query": query,
                 "retrieved": [{k: h[k] for k in ("source_id", "page", "score", "chunk_id")} for h in hits],
                 "prompt_sha256": hashlib.sha256(json.dumps(messages).encode()).hexdigest(),
                 "llm": meta, "raw_output": raw, "parsed": parsed, "citation_check": citations,
                 "ts": time.strftime("%H:%M:%S")})
            print(f"[R{r_idx} {sim_time}] {role:9s} {meta['latency_s']:6.1f}s  parsed={parsed is not None}  "
                  f"cites={[c['status'][:8] for c in citations]}")
            round_outputs[role] = parsed or {"unparsed_output": raw}
            # transcript
            transcript.append(f"\n### {ROLES[role]['name']}\n")
            transcript.append("**Received:** " + " | ".join(events + [f"msg from {m['from']}: {m['text']}" for m in inbox]) + "\n")
            transcript.append("**Retrieved:** " + ", ".join(f"{h['source_id']} p.{h['page']} ({h['score']})" for h in hits) + "\n")
            transcript.append("```json\n" + json.dumps(parsed or raw, indent=2, ensure_ascii=False) + "\n```\n")
            transcript.append("**Citation check:** " + (", ".join(f"{c['ref']} → {c['status']}" for c in citations) or "no citations") + "\n")

        # route requests to next round inboxes
        inboxes = {k: [] for k in ROLES}
        for sender, o in round_outputs.items():
            for req in (o.get("requests") or []) if isinstance(o, dict) else []:
                to = str(req.get("to", "")).upper() if isinstance(req, dict) else ""
                if to in inboxes and to != sender and req.get("request"):
                    inboxes[to].append({"from": sender, "text": str(req["request"])})

        # coordinator
        # coordinator retrieval: agents' gaps + one passage per policy theme (diverse global examples)
        gap_text = " ".join(" ".join(map(str, (o.get("gaps") or []))) for o in round_outputs.values() if isinstance(o, dict))
        hits, seen = [], set()
        for q in [gap_text + " " + rnd.get("query_hint", "")] + ADVISER_THEMES:
            for h in kb.search(q, top_k=2, max_per_source=1):
                if h["chunk_id"] not in seen:
                    hits.append(h)
                    seen.add(h["chunk_id"])
                    break
        messages = adviser_messages(sim_time, round_outputs, hits, earlier_gaps)
        raw, parsed, meta = call_llm(llm, messages, max_tokens=1200)
        for g in ((parsed or {}).get("policy_gaps") or []):
            if isinstance(g, dict) and g.get("gap"):
                earlier_gaps.append(str(g["gap"])[:200])
        citations = check_citations(parsed, hits)
        log({"run_id": run_id, "round": r_idx, "sim_time": sim_time, "agent": "ADVISER", "type": "coordinator_brief",
             "inputs_from": list(round_outputs),
             "retrieved": [{k: h[k] for k in ("source_id", "page", "score", "chunk_id")} for h in hits],
             "prompt_sha256": hashlib.sha256(json.dumps(messages).encode()).hexdigest(),
             "llm": meta, "raw_output": raw, "parsed": parsed, "citation_check": citations,
             "ts": time.strftime("%H:%M:%S")})
        print(f"[R{r_idx} {sim_time}] ADVISER   {meta['latency_s']:6.1f}s  parsed={parsed is not None}  "
              f"cites={[c['status'][:8] for c in citations]}")
        brief = json.dumps({k: (parsed or {}).get(k) for k in ("summary", "conflicts", "priorities_next_round")},
                           ensure_ascii=False) if parsed else raw[:1500]
        all_briefs.append({"round": r_idx, "sim_time": sim_time, "brief": parsed or raw, "citation_check": citations})
        transcript.append(f"\n### {ADVISER['name']}\n")
        transcript.append("**Retrieved:** " + ", ".join(f"{h['source_id']} p.{h['page']} ({h['score']})" for h in hits) + "\n")
        transcript.append("```json\n" + json.dumps(parsed or raw, indent=2, ensure_ascii=False) + "\n```\n")
        transcript.append("**Citation check:** " + (", ".join(f"{c['ref']} → {c['status']}" for c in citations) or "no citations") + "\n")

    audit.close()
    (out / "coordinator_briefs.json").write_text(json.dumps(all_briefs, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "transcript.md").write_text("\n".join(transcript), encoding="utf-8")
    print(f"Done. Outputs in {out}")


if __name__ == "__main__":
    main()
