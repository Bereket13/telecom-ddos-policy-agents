"""Institutional agents and the Policy & Legal Adviser (coordinator).

Each agent has its own mandate, its own slice of the knowledge base, and its own
inbox. Agents never see each other's raw information: they only see (a) the
events delivered to them, (b) messages addressed to them, and (c) the
coordinator's brief from the previous round. This reproduces the information
asymmetry of real incidents.
"""
import json
import re

ROLES = {
    "SOC": {
        "name": "Operator Security Operations Centre (SOC) agent",
        "mandate": ("You represent the mobile network operator's security operations centre. You keep the "
                    "network and emergency calls available, run the AI-based DDoS detector, mitigate attacks, "
                    "and must report significant incidents to the authorities."),
        "sources": ["G01", "G03", "G07", "G08", "G09", "G05"],
    },
    "REGULATOR": {
        "name": "National Telecom Regulator agent",
        "mandate": ("You represent the national telecommunications regulator. You protect service continuity, "
                    "quality of service, emergency access and consumers, and you supervise operators' incident "
                    "reporting. You may also be the data-protection supervisor in some countries."),
        "sources": ["G05", "G03", "G02", "U01", "G13", "G12", "E02"],
    },
    "DPA": {
        "name": "Data-Protection Authority agent",
        "mandate": ("You represent the personal-data protection authority. You handle personal-data breaches, "
                    "notification of authorities and affected people, lawful processing and cross-border "
                    "transfers of personal data."),
        "sources": ["G12", "G05", "G04", "G10", "G08", "G13"],
    },
    "CERT": {
        "name": "National Cybersecurity Agency / CERT agent",
        "mandate": ("You represent the national CERT / cybersecurity agency. You coordinate national incident "
                    "response, share threat intelligence, handle cybercrime evidence, and lead cross-border "
                    "cooperation with foreign CERTs and law enforcement."),
        "sources": ["E01", "E02", "G12", "G09", "G07", "G05", "G03"],
    },
}

ADVISER = {
    "name": "Policy & Legal Adviser agent (coordinator)",
    "mandate": ("You coordinate the institutional agents. You compare their assessments, detect conflicts and "
                "unclear responsibilities, and identify policy and standards gaps, each backed by a global "
                "policy example from the knowledge base. You focus on domain-specific (telecom / AI security) "
                "gaps, not on judging any specific country."),
    "sources": None,  # full knowledge base
}

AGENT_SCHEMA = """Return ONLY one JSON object with these keys:
{
  "assessment": "2-3 sentences: what is happening and why it matters for your mandate",
  "reasoning": ["short step 1", "short step 2", "short step 3"],
  "actions": [{"action": "...", "owner": "SOC|REGULATOR|DPA|CERT|other", "deadline": "e.g. within 1 hour"}],
  "policy_refs": [{"ref": "source_id p.page, e.g. G05 p.40", "point": "what that passage requires or recommends"}],
  "requests": [{"to": "SOC|REGULATOR|DPA|CERT", "request": "information you need from them"}],
  "gaps": ["a rule, responsibility or standard that is missing or unclear"],
  "confidence": "low|medium|high"
}"""

ADVISER_SCHEMA = """Return ONLY one JSON object with these keys:
{
  "summary": "3 sentences on the state of the response",
  "conflicts": ["conflict between agents' actions or objectives"],
  "unclear_responsibilities": ["who should do X is unclear because ..."],
  "policy_gaps": [{"gap": "...", "global_example": "quote or paraphrase of the cited passage", "ref": "ONE tag, e.g. G05 p.50", "recommendation": "..."}],
  "standards_gaps": ["technical standard or evaluation practice that is missing"],
  "priorities_next_round": ["..."]
}
Give 3 policy_gaps that are DIFFERENT from each other and from gaps already listed in earlier rounds, each about a
different checklist item, each with exactly one ref whose passage really supports the global_example."""

# Themes used to retrieve diverse global policy examples for the coordinator
ADVISER_THEMES = [
    "incident notification early warning deadline competent authority CSIRT",
    "personal data breach notification transfer of personal data to third country authorisation",
    "AI system accuracy robustness human oversight record-keeping logs high-risk",
    "test evaluation validation verification of AI models before deployment measure",
    "international cooperation cybercrime mutual assistance cross-border",
    "machine learning sandbox model selection policy node pipeline",
]

FOCUS = {
    "SOC": "incident detection response containment monitoring network services AI system robustness validation",
    "REGULATOR": "significant incident reporting obligation notification competent authority service continuity",
    "DPA": "personal data breach notification supervisory authority data subject transfer consent processing",
    "CERT": "CSIRT national coordination information sharing cross-border cooperation cybercrime evidence",
}

ADVISER_CHECKLIST = ("Check in particular: (1) who must notify whom and by when; (2) sharing of traffic or personal "
                     "data with third parties or abroad versus privacy; (3) reliability, validation and human "
                     "oversight of the AI detector and of any retrained model; (4) which authority leads when one "
                     "incident is at the same time a telecom outage, a cyber attack and a personal-data breach; "
                     "(5) cross-border cooperation; (6) reuse of an AI system in another sector.")

RULES = ("Rules: use ONLY the POLICY CONTEXT passages for policy claims. Cite ONLY passages that are relevant to "
         "the decision (ignore irrelevant ones), using their exact tag, e.g. G05 p.40. In 'point', quote or "
         "paraphrase the relevant sentence of that passage. If the context does not cover something, write "
         "'not covered by KB' instead of inventing a law. Stay inside your mandate. Be concise.")


def format_context(hits):
    return "\n".join(f"[{h['source_id']} p.{h['page']}] ({h['title'][:60]}) {h['text']}" for h in hits)


def agent_messages(role_key, sim_time, events, inbox, brief, hits):
    r = ROLES[role_key]
    system = f"You are the {r['name']}. {r['mandate']}\n{RULES}\n{AGENT_SCHEMA}"
    ev = "\n".join(f"- {e}" for e in events) or "- (no new information for you this round)"
    ib = "\n".join(f"- from {m['from']}: {m['text']}" for m in inbox) or "- (none)"
    user = (f"SIMULATION TIME: {sim_time}\n\nNEW INFORMATION YOU RECEIVED:\n{ev}\n\n"
            f"MESSAGES ADDRESSED TO YOU:\n{ib}\n\nCOORDINATOR BRIEF FROM LAST ROUND:\n{brief or '(none yet)'}\n\n"
            f"POLICY CONTEXT:\n{format_context(hits)}\n\nRespond now with the JSON object.")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def adviser_messages(sim_time, round_outputs, hits, earlier_gaps=None):
    system = f"You are the {ADVISER['name']}. {ADVISER['mandate']}\n{ADVISER_CHECKLIST}\n{RULES}\n{ADVISER_SCHEMA}"
    body = "\n\n".join(f"### {k}\n{json.dumps(v, ensure_ascii=False)}" for k, v in round_outputs.items())
    earlier = "\n".join(f"- {g}" for g in (earlier_gaps or [])) or "- (none)"
    user = (f"SIMULATION TIME: {sim_time}\n\nGAPS ALREADY LISTED IN EARLIER ROUNDS (do not repeat):\n{earlier}\n\n"
            f"AGENT OUTPUTS THIS ROUND:\n{body}\n\n"
            f"POLICY CONTEXT:\n{format_context(hits)}\n\nRespond now with the JSON object.")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


REF_RE = re.compile(r"\b([GUE]\d{2})\b(?:[^0-9]{0,6}(\d{1,4}))?")


def check_citations(parsed, hits):
    """Audit: are the cited (source, page) pairs actually among the retrieved passages?"""
    retrieved = {(h["source_id"], h["page"]) for h in hits}
    retrieved_src = {h["source_id"] for h in hits}
    refs = []
    for key in ("policy_refs", "policy_gaps"):
        for item in (parsed or {}).get(key, []) or []:
            if isinstance(item, dict) and item.get("ref"):
                refs.append(str(item["ref"]))
    results = []
    for ref in refs:
        tags = REF_RE.findall(ref)
        if not tags:
            results.append({"ref": ref, "status": "no-source-id"})
            continue
        seen = set()
        for sid, page in tags:  # a ref string may contain several tags: check each one
            page = int(page) if page else None
            if (sid, page) in seen:
                continue
            seen.add((sid, page))
            if (sid, page) in retrieved:
                status = "verified"
            elif sid in retrieved_src:
                status = "source-retrieved-page-mismatch"
            else:
                status = "NOT-IN-RETRIEVED-CONTEXT"
            results.append({"ref": f"{sid} p.{page}" if page else sid, "status": status})
    return results
