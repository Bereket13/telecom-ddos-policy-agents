"""Read-only access to the FAISS knowledge base built by build_kb.py."""
import json
from pathlib import Path


class KnowledgeBase:
    def __init__(self, index_dir):
        import faiss
        from sentence_transformers import SentenceTransformer

        index_dir = Path(index_dir)
        self.config = json.loads((index_dir / "config.json").read_text(encoding="utf-8"))
        self.index = faiss.read_index(str(index_dir / "faiss.index"))
        with open(index_dir / "chunks.jsonl", encoding="utf-8") as f:
            self.chunks = [json.loads(line) for line in f]
        self.embedder = SentenceTransformer(self.config["embed_model"])

    def search(self, query, top_k=4, allowed_sources=None, max_per_source=2, pool=80):
        """Cosine search; optionally restrict to an agent's mandate-relevant sources.

        Returns a list of dicts with source_id, page, score, chunk_id, title, text.
        """
        q = self.embedder.encode([query], normalize_embeddings=True, convert_to_numpy=True).astype("float32")
        scores, ids = self.index.search(q, min(pool, len(self.chunks)))
        hits, per_source = [], {}
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            c = self.chunks[idx]
            if allowed_sources and c["source_id"] not in allowed_sources:
                continue
            if per_source.get(c["source_id"], 0) >= max_per_source:
                continue
            per_source[c["source_id"]] = per_source.get(c["source_id"], 0) + 1
            hits.append({"source_id": c["source_id"], "page": c["page"], "score": round(float(score), 4),
                         "chunk_id": c["chunk_id"], "title": c["title"], "text": c["text"]})
            if len(hits) >= top_k:
                break
        return hits
