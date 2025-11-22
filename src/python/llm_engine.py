# llm_engine.py
import os
from typing import Dict, Any, Optional

# Try to import 'requests' but provide a minimal urllib-based fallback when it's not available.
try:
    import requests  # type: ignore
except Exception:
    import json as _json
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    class _SimpleResponse:
        def __init__(self, resp, status_code=None):
            # resp may be an HTTPError or a file-like object from urlopen()
            self._resp = resp
            self.status_code = status_code if status_code is not None else getattr(resp, "getcode", lambda: None)()
            try:
                self.text = resp.read().decode("utf-8") if hasattr(resp, "read") else str(resp)
            except Exception:
                self.text = str(resp)

        def raise_for_status(self):
            if isinstance(self.status_code, int) and self.status_code >= 400:
                raise HTTPError(None, self.status_code, self.text, None, None)

        def json(self):
            return _json.loads(self.text)

    class requests:  # minimal drop-in replacement for requests.post used in this module
        @staticmethod
        def post(url, headers=None, json=None, timeout=None):
            body = _json.dumps(json).encode("utf-8") if json is not None else None
            req = Request(url, data=body, headers=headers or {}, method="POST")
            if body is not None and "Content-Type" not in (headers or {}):
                req.add_header("Content-Type", "application/json")
            try:
                resp = urlopen(req, timeout=timeout)
                return _SimpleResponse(resp)
            except HTTPError as e:
                return _SimpleResponse(e, status_code=e.code)
            except URLError as e:
                # re-raise to keep behavior similar to requests (caller will see an exception)
                raise

HF_INFERENCE_URL = "https://api-inference.huggingface.co/models"
HF_API_KEY = os.environ.get("HF_API_KEY")  # set in your environment

if not HF_API_KEY:
    # we allow running without HF key for local tests but many features need it
    print("WARNING: HF_API_KEY not set — LLM calls will fail unless provided.")

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

def call_hf_model(model_repo: str, inputs: str, params: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
    """
    Generic HF Inference API call (text generation / text2text).
    Returns the parsed JSON or raises an error.
    """
    url = f"{HF_INFERENCE_URL}/{model_repo}"
    payload = {"inputs": inputs}
    if params:
        payload["parameters"] = params

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)
    resp.raise_for_status()
    # HF returns JSON or array-of-tokens depending on model
    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}

def parse_with_llm(prompt: str, model: str = "google/flan-t5-large", max_length: int = 512) -> str:
    """
    Simple helper: call HF text2text model and return the text result.
    Default model is an instruction-tuned T5; change if you host a different model.
    """
    out = call_hf_model(model, prompt, params={"max_new_tokens": 256, "temperature": 0.2})
    # HF returns list of dicts sometimes
    if isinstance(out, list):
        # sometimes it's [{"generated_text": "..."}]
        if "generated_text" in out[0]:
            return out[0]["generated_text"]
        # else join
        return " ".join([str(x) for x in out])
    if isinstance(out, dict) and out.get("generated_text"):
        return out["generated_text"]
    # fallback raw
    return str(out)
