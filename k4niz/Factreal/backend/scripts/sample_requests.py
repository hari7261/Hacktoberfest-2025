"""Minimal client to exercise the FactReal API endpoints."""
from __future__ import annotations

import json
import time
from typing import Any

import requests


BASE = "http://127.0.0.1:8000"


def pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def main() -> None:
    # Wait briefly in case server just started
    time.sleep(0.3)

    text = "Elections are always rigged and the media hides the truth."
    r = requests.post(f"{BASE}/classify", json={"text": text})
    print("/classify =>", r.status_code)
    print(pretty(r.json()))

    r2 = requests.post(f"{BASE}/explain", json={"text": text, "label": "propaganda"})
    print("/explain =>", r2.status_code)
    print(pretty(r2.json()))


if __name__ == "__main__":
    main()
