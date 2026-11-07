"""NyayaVault configuration: legal-corpus paths, models, budgets.

Honest status: the BharatCode model API is wired behind the same
interface as the mock provider, but no key is invented and none is
in the repo. Without ``BHARATCODE_API_KEY`` the app runs in clearly
labelled [mock] mode.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_MODEL = "qwen-3.8-27b"
FALLBACK_MODEL = "deepseek-v4.1-flash"
DAILY_CALL_CAP = 10
MODELS = (DEFAULT_MODEL, FALLBACK_MODEL)


@dataclass(frozen=True)
class NyayaVaultConfig:
    """Values the app reads from the environment (or defaults)."""

    corpus_root: str
    base_url: str = "https://bharatcode.ai"
    api_key: str = ""
    model: str = DEFAULT_MODEL
    fallback_model: str = FALLBACK_MODEL
    daily_call_cap: int = DAILY_CALL_CAP
    mock_mode: bool = True
    port: int = 8000
    host: str = "0.0.0.0"


def config_from_env(corpus_root: str) -> NyayaVaultConfig:
    """Build the config from the environment.

    The key is read from ``BHARATCODE_API_KEY`` only. An empty key
    means mock mode — the app never invents a key.
    """
    key = os.environ.get("BHARATCODE_API_KEY", "").strip()
    model = os.environ.get("BHARATCODE_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    fallback = (
        os.environ.get("BHARATCODE_FALLBACK_MODEL", FALLBACK_MODEL).strip()
        or FALLBACK_MODEL
    )
    return NyayaVaultConfig(
        corpus_root=corpus_root,
        base_url=os.environ.get("BHARATCODE_BASE_URL", "https://bharatcode.ai").rstrip("/"),
        api_key=key,
        model=model,
        fallback_model=fallback,
        daily_call_cap=int(os.environ.get("NYAYAVAULT_DAILY_CALL_CAP", str(DAILY_CALL_CAP))),
        mock_mode=not key,
        port=int(os.environ.get("PORT", "8000")),
        host=os.environ.get("HOST", "0.0.0.0"),
    )
