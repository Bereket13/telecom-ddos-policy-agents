# PolicyShield: policy-grounded agents for telecom DDoS response when the AI detector fails

Submission to the **ITU AI for Good Lab Hackathon: United Arab Emirates (2026)**, from Team PolicyShield (individual: Bereket Teklew Kibret, Addis Ababa, Ethiopia).

AI intrusion detectors are judged by benchmark accuracy, but they can fail silently on real traffic. In the author's MSc thesis, an XGBoost DDoS detector scored MCC 0.9996 on CIC-IDS2017. Applied zero-shot to CIC-DDoS2019, it caught only 23 of 479,497 DDoS flows, and it gave no warning. PolicyShield simulates what institutions must do when this happens during a live attack on a mobile network. Each agent reasons from a policy knowledge base, and every decision is auditable.

## What it does
| Requirement (hackathon) | Where |
|---|---|
| Knowledge base of policies, regulations and strategies (ITU reference method) | `src/build_kb.py`, `kb/sources.csv`, `kb/index/` (14 documents, 3,114 passages, FAISS + all-MiniLM-L6-v2) |
| Agents with roles: application agent, institutional participants, policy and legal adviser, multi-agent coordination | `src/agents.py`: SOC, Regulator, Data-Protection Authority, CERT, plus the Policy & Legal Adviser as coordinator |
| Interactive error scenarios with chunked events released progressively to different agents | `scenarios/ddos_mobile_operator.json` (4 rounds, T+0h to T+6h); `src/run_scenario.py` |
| Audit logging and chain-of-thought tracing with source attribution | `outputs/run_*/audit_log.jsonl`: events received, retrieval query, retrieved source and page, prompt SHA-256, raw output, parsed decision (with reasoning steps), automatic citation check |
| Alignment with ITU-T Y.3172 and the AI Readiness Framework 2.0 | Technical report, section 4 (mapping table) |

### Coordination protocol (one round)
1. The scenario releases new events **only to the agents concerned**. No agent sees the full picture.
2. Tools run first. `detector_consistency_check` flags a silent failure when network KPIs show a major anomaly but the AI detector reports almost no attacks.
3. Each agent retrieves passages from **its own KB slice** (its mandate) and returns a JSON decision with these fields:
   - assessment
   - reasoning steps
   - actions (each with an owner and a deadline)
   - cited policy references (`source_id p.page`)
   - requests to other agents
   - gaps
   - confidence
4. Requests are routed to the inboxes of the agents they address, for the next round.
5. The **Policy & Legal Adviser** reads all outputs, retrieves from the full KB, and publishes a brief. The brief covers conflicts, unclear responsibilities, policy gaps (each with a global example) and standards gaps. It is broadcast to all agents.

## Run it
**Laptop (CPU, about 16 GB RAM):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install faiss-cpu pypdf sentence-transformers huggingface_hub
pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
# optional: rebuild the KB (the prebuilt index is included)
python src/download_sources.py docs
python src/build_kb.py --docs docs --out kb/index
# model: bartowski/Qwen2.5-3B-Instruct-GGUF, file Qwen2.5-3B-Instruct-Q4_K_M.gguf (1.9 GB)
cd src
python run_scenario.py --kb ../kb/index --model <path>/Qwen2.5-3B-Instruct-Q4_K_M.gguf \
    --scenario ../scenarios/ddos_mobile_operator.json --out ../outputs
```
**Google Colab (free tier):** `notebooks/PolicyShield_Colab.ipynb`.

**Any OpenAI-compatible endpoint** (llama.cpp server, Ollama, or a sandbox LLM): `--backend openai --base-url <url>/v1 --model <name>`.

## Outputs of the submitted run
There are two full runs, both of the 4-round scenario, on a laptop CPU (Qwen2.5-3B-Instruct Q4_K_M, temperature 0.2, seed 42). Each run folder holds `audit_log.jsonl`, `transcript.md`, `coordinator_briefs.json`, `metrics.json` and `run_config.json`.

| Metric | v1 baseline (`outputs/v1_baseline_run_20261110_151713`) | v2: coordinator memory + theme-diverse retrieval (`outputs/run_20261110_165815`) |
|---|---|---|
| LLM calls (agent decisions + coordinator briefs) | 15 (11 + 4) | 15 (11 + 4) |
| Valid JSON | 14/15 | 15/15 |
| Messages routed between agents | 9 | 7 |
| Citations that point to a retrieved passage | 33/36 (92%) | 39/45 (87%) |
| Gap statements (distinct) | 17 (11) | 23 (11) |
| Mean time per LLM call | 157 s | 156 s |

Findings, all traceable in the audit logs:
- **Round 1, both runs.** The consistency tool flagged the AI detector's silent failure. The SOC switched to manual mitigation and asked the CERT about the unseen attack. The regulator demanded a preliminary assessment within 1 hour.
- **Round 2, v1.** The SOC agent decided to redirect all traffic and share full packet captures with a foreign scrubbing provider. The data-protection agent was never told. This shows information asymmetry producing a legally risky action, and it is why the design needs a human approval gate in the Y.3172 policy node.
- **Round 3, v1.** The SOC agent refused unvalidated redeployment of the retrained detector and asked for validation and a rollback plan.
- **Agent behaviour.** In both runs the coordinator's broadcast anchored the agents (herding). In v2 this took the form of a "who notifies whom" clarification loop, which crowded out the privacy and retraining decisions. Next step: cap repeated requests and give each round an explicit decision agenda.

## Knowledge base
See `kb/sources.csv` for titles, publishers, scope and URLs, and `kb/index/manifest.json` for page counts, chunk counts and SHA-256 of each source PDF.
- Global: ITU-T Y.3172; ITU AI Ready 2.0; ITU-T X.1056; NIST CSF 2.0; NIST AI RMF 1.0; NIST SP 800-61r3; OECD AI Recommendation.
- Regional: EU AI Act; EU NIS2; AU Malabo Convention; AU Continental AI Strategy.
- National: UAE National AI Strategy 2031; Ethiopia Computer Crime Proclamation 958/2016 (via ARTICLE 19's analysis with English translation); Council of Europe Octopus cybercrime legal profile of Ethiopia.

The KB method follows the ITU reference notebook ([CrashingGuru/ITUAIReadiness](https://github.com/CrashingGuru/ITUAIReadiness)): pypdf text extraction, 800-character chunks with 120 overlap, normalised MiniLM embeddings, and a FAISS inner-product index. It adds per-page attribution, JSONL metadata (no pickle) and a SHA-256 manifest.

## Limitations (honest)
- A 3B-parameter local model was used, so that the whole system runs free on a laptop. Its legal reasoning is shallow, and it sometimes cites passages that were retrieved but are only loosely relevant. The citation check verifies that a cited passage was actually retrieved, not that the legal interpretation is correct. Human review stays essential.
- The scenario is fictional. It is modelled on public frameworks and does not describe a real incident or country.
- Some national texts are missing from the KB because no official English text could be downloaded in time: Ethiopia's Personal Data Protection Proclamation 1321/2024 and the UAE's PDPL. These are the next additions.

## Author
Bereket Teklew Kibret: MSc Electrical and Computer Engineering (AASTU, 2026), ITU AI for Good Scholar 2025. bereketteklew@gmail.com

AI coding tools assisted the development. The research idea, the thesis results it builds on, and the final review are the author's.
