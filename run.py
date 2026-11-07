"""NyayaVault local server entrypoint.

Run:
    python3 run.py
Then open http://localhost:8000/ in a browser.

Stdlib only. No key is read from any file — the BharatCode key comes
from the BHARATCODE_API_KEY environment variable, and without it the
app runs in clearly labelled [mock] mode.
"""

from __future__ import annotations

import os

from nyayavault.agent import LegalAgent
from nyayavault.config import config_from_env
from nyayavault.web import serve

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_ROOT = os.path.join(BASE_DIR, "corpus")
SAMPLES_ROOT = os.path.join(BASE_DIR, "samples")


def main() -> None:
    config = config_from_env(CORPUS_ROOT)
    agent = LegalAgent(config)
    print(f"NyayaVault: {len(agent.provisions)} provisions loaded.")
    print(f"Mode: {'real BharatCode API' if not config.mock_mode else '[mock] offline stand-in'}")
    serve(agent, config, SAMPLES_ROOT)


if __name__ == "__main__":
    main()
