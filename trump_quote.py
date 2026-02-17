"""Récupérer une citation aléatoire (ou personnalisée) depuis
l'API "What Does Trump Think".

Usage:
  python trump_quote.py           # affiche une citation aléatoire
  python trump_quote.py <sujet>   # affiche une citation personnalisée

Cette implémentation n'utilise que la bibliothèque standard (urllib).
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

BASE_URL = "https://api.whatdoestrumpthink.com/api/v1/quotes"


def _fetch_json(path: str, timeout: int = 5) -> dict:
    url = urllib.parse.urljoin(BASE_URL + '/', path.lstrip('/'))
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} - {e.reason}: {e.read().decode(errors='ignore')}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON response: {e}")


def get_random_quote() -> str:
    """Retourne une citation TRUMP aléatoire (message seulement)."""
    data = _fetch_json("/random")
    return data.get("message", "")


def get_personalized_quote(subject: str) -> str:
    """Retourne une citation personnalisée à propos de `subject`."""
    # l'API attend la query `q=`
    q = urllib.parse.urlencode({"q": subject})
    data = _fetch_json(f"/personalized?{q}")
    # l'API retourne `message` et parfois `nickname`/`nlp_attributes`
    return data.get("message", "")


def _cli(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    try:
        if not argv:
            quote = get_random_quote()
        else:
            quote = get_personalized_quote(" ".join(argv))
        print(quote)
        return 0
    except Exception as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(_cli())
