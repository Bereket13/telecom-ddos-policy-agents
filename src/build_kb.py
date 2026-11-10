"""Build the policy knowledge base (KB) from the PDFs listed in kb/sources.csv.

Method follows the ITU AI for Good reference notebook
(github.com/CrashingGuru/ITUAIReadiness, "Colab Free Tier LLM Notebook"):
  pypdf text extraction -> whitespace normalisation -> ~800-char chunks with
  120-char overlap broken at spaces (chunks < 80 chars dropped) ->
  sentence-transformers/all-MiniLM-L6-v2 (normalised) -> FAISS IndexFlatIP.

Additions for auditability:
  * chunks are made per page, so every retrieved passage carries
    source_id + page number (source attribution in the audit log);
  * metadata is stored as JSON Lines (not pickle) so it is human-readable and
    safe to load;
  * a manifest with SHA-256 of every input document makes the KB reproducible.

Usage:
  python src/build_kb.py --docs <folder with PDFs> --out kb/index
"""
import argparse
import csv
import hashlib
import json
import re
import time
from pathlib import Path

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
MIN_CHUNK_CHARS = 80
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Same splitting rule as the ITU reference notebook: break at spaces."""
    chunks, start, n = [], 0, len(text)
    while start < n:
        end = min(start + size, n)
        if end < n:
            space = text.rfind(" ", start + size // 2, end)
            if space != -1:
                end = space
        piece = text[start:end].strip()
        if len(piece) >= MIN_CHUNK_CHARS:
            chunks.append(piece)
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", required=True, help="folder containing the source PDFs")
    ap.add_argument("--sources", default=str(Path(__file__).resolve().parents[1] / "kb" / "sources.csv"))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "kb" / "index"))
    args = ap.parse_args()

    from pypdf import PdfReader
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer

    docs_dir, out = Path(args.docs), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(args.sources, newline="", encoding="utf-8-sig") as f:
        sources = list(csv.DictReader(f))

    records, manifest = [], []
    for src in sources:
        path = docs_dir / src["file"]
        if not path.exists():
            print(f"[skip] missing {src['file']}")
            continue
        reader = PdfReader(str(path))
        n_chunks = 0
        for page_no, page in enumerate(reader.pages, start=1):
            try:
                text = normalize(page.extract_text())
            except Exception as e:  # damaged page: log and continue
                print(f"[warn] {src['source_id']} p{page_no}: {e}")
                continue
            for piece in chunk_text(text):
                records.append({
                    "chunk_id": len(records),
                    "source_id": src["source_id"],
                    "title": src["title"],
                    "publisher": src["publisher"],
                    "scope": src["scope"],
                    "doc_type": src["doc_type"],
                    "page": page_no,
                    "text": piece,
                })
                n_chunks += 1
        manifest.append({**src, "pages": len(reader.pages), "chunks": n_chunks, "sha256": sha256(path)})
        print(f"[ok] {src['source_id']:4s} pages={len(reader.pages):4d} chunks={n_chunks:5d}  {src['title'][:70]}")

    t0 = time.time()
    model = SentenceTransformer(EMBED_MODEL)
    emb = model.encode([r["text"] for r in records], batch_size=64, show_progress_bar=True,
                       normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)
    faiss.write_index(index, str(out / "faiss.index"))
    with open(out / "chunks.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    config = {"embed_model": EMBED_MODEL, "chunk_size": CHUNK_SIZE, "chunk_overlap": CHUNK_OVERLAP,
              "min_chunk_chars": MIN_CHUNK_CHARS, "index_type": "IndexFlatIP (cosine on normalised vectors)",
              "n_chunks": len(records), "dim": int(emb.shape[1]), "built": time.strftime("%Y-%m-%d %H:%M:%S"),
              "embed_seconds": round(time.time() - t0, 1)}
    (out / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"KB built: {len(records)} chunks from {len(manifest)} documents -> {out}")


if __name__ == "__main__":
    main()
