"""Small LLM wrapper.

Backends:
  * "llamacpp": local GGUF model through llama-cpp-python (same runtime as the
    ITU reference notebook; runs on a laptop CPU or the free Colab tier).
  * "openai": any OpenAI-compatible endpoint (llama.cpp server, Ollama, or the
    ITU AI for Good sandbox if it exposes one). Uses only the standard library.
"""
import json
import os
import time
import urllib.request


class LLM:
    def __init__(self, backend="llamacpp", model_path=None, n_ctx=8192, temperature=0.2,
                 max_tokens=700, seed=42, base_url=None, model_name=None, api_key=None):
        self.backend, self.temperature, self.max_tokens, self.seed = backend, temperature, max_tokens, seed
        self.model_id = model_name or (os.path.basename(model_path) if model_path else "unknown")
        if backend == "llamacpp":
            from llama_cpp import Llama
            self.llm = Llama(model_path=model_path, n_ctx=n_ctx, n_threads=os.cpu_count(),
                             n_gpu_layers=-1, seed=seed, verbose=False)
        elif backend == "openai":
            self.base_url = base_url.rstrip("/")
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "none")
        else:
            raise ValueError(backend)

    def chat(self, messages, json_mode=True, max_tokens=None):
        t0 = time.time()
        max_tokens = max_tokens or self.max_tokens
        if self.backend == "llamacpp":
            kw = dict(messages=messages, temperature=self.temperature, max_tokens=max_tokens, seed=self.seed)
            if json_mode:
                kw["response_format"] = {"type": "json_object"}
            out = self.llm.create_chat_completion(**kw)
        else:
            body = {"model": self.model_id, "messages": messages, "temperature": self.temperature,
                    "max_tokens": max_tokens, "seed": self.seed}
            if json_mode:
                body["response_format"] = {"type": "json_object"}
            req = urllib.request.Request(self.base_url + "/chat/completions", data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": f"Bearer {self.api_key}"})
            with urllib.request.urlopen(req, timeout=600) as r:
                out = json.loads(r.read())
        text = out["choices"][0]["message"]["content"]
        meta = {"latency_s": round(time.time() - t0, 1), "usage": out.get("usage", {}),
                "model": self.model_id, "temperature": self.temperature, "seed": self.seed}
        return text, meta


def parse_json(text):
    """Parse model output; tolerate code fences or text around the JSON object."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e > s:
            try:
                return json.loads(text[s:e + 1]), None
            except json.JSONDecodeError as err:
                return None, str(err)
        return None, "no JSON object found"
