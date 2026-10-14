#!/usr/bin/env python3
"""
Multi-engine discovery of free movie & TV directories that use
StreamTape / DoodStream / MixDrop / LuluStream / VOE / FileMoon / etc.

Expanded scope: full movies, series, episodes, softcore/erotic, R-rated.
"""

import time
import json
from collections import defaultdict
from urllib.parse import urlparse

from duckduckgo_search import DDGS

try:
    from brave import Brave
    BRAVE_AVAILABLE = True
except ImportError:
    BRAVE_AVAILABLE = False
    print("Note: brave-search not installed — Brave results will be skipped.")

# ---------------------------------------------------------------------------
# Config — expanded for movies + TV
# ---------------------------------------------------------------------------

HOSTS = [
    "streamtape",
    "doodstream",
    "mixdrop",
    "lulustream",
    "voe.sx",
    "filemoon",
    "vidara",
    "streamsb",
    "streamwish",
    "dropload",
    "filelions",
]

QUERY_TEMPLATES = [
    # Movies
    '"{host}" ("full movie" OR "watch movie" OR "stream movie") (free OR online) -forum -reddit',
    '"{host}" ("movie" OR "film") ("embed" OR "player" OR "stream") (doodstream OR mixdrop OR streamtape)',
    # TV / Series
    '"{host}" ("episode" OR "series" OR "season" OR "TV show" OR "full episode") (stream OR watch) -forum',
    '"{host}" ("s01e01" OR "s1e1" OR "season 1" OR "episode 1") (stream OR embed)',
    # Softcore / erotic / R-rated overlap
    '"{host}" ("softcore" OR "erotic" OR "R rated" OR "uncensored") (movie OR series OR episode)',
    # General free streaming patterns
    '"{host}" ("free streaming" OR "watch online free") (movie OR series OR episode) -porn -xxx',
    '"{host}" (xtapes OR pandamovies OR "watch free" OR "full movies" OR "tv series")',
]

# Known / seed domains that often use these hosts for movies & TV
SEED_DOMAINS = [
    "xtapes.me", "xtapes.tw",
    "pandamovies.org", "pandamovies.pw",
    "watchpornfree.info",          # still relevant for softcore/erotic
    "freeomovie.info",
    "fullxxxmovies.me",
    # Broader free streaming examples (add more as you discover them)
    "fmovies", "soap2day", "123movies", "putlocker",
    "vidsrc", "embed", "multiembed",
]

NEGATIVE_KEYWORDS = [
    "forum", "reddit", "twitter", "discord", "telegram",
    "download only", "torrent", "magnet",
]

# ---------------------------------------------------------------------------
# Search backends
# ---------------------------------------------------------------------------

def search_ddg(query: str, max_results: int = 12) -> list[dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href") or r.get("link", ""),
                    "snippet": r.get("body", ""),
                    "engine": "duckduckgo",
                })
    except Exception as e:
        print(f"  DDG error: {e}")
    return results


def search_brave(query: str, max_results: int = 12) -> list[dict]:
    if not BRAVE_AVAILABLE:
        return []
    results = []
    try:
        brave = Brave()
        search_results = brave.search(q=query, count=max_results)
        for r in search_results.web.results:
            results.append({
                "title": r.title or "",
                "url": r.url or "",
                "snippet": r.description or "",
                "engine": "brave",
            })
    except Exception as e:
        print(f"  Brave error: {e}")
    return results


def search_bing_fallback(query: str, max_results: int = 8) -> list[dict]:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(f"!b {query}", max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href") or r.get("link", ""),
                    "snippet": r.get("body", ""),
                    "engine": "bing-via-ddg",
                })
    except Exception:
        pass
    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_domain(url: str) -> str | None:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        skip = ["google.", "bing.", "duckduckgo.", "brave.", "reddit.", "twitter.",
                "facebook.", "youtube.", "wikipedia.", "imdb."]
        if any(x in domain for x in skip):
            return None
        return domain
    except Exception:
        return None


def is_likely_directory(title: str, snippet: str, url: str) -> bool:
    text = (title + " " + snippet + " " + url).lower()
    positive = [
        "full movie", "watch online", "stream", "episode", "series", "season",
        "tv show", "embed", "player", "free streaming", "watch free",
        "softcore", "erotic", "duration", "studio",
    ]
    if any(n in text for n in NEGATIVE_KEYWORDS):
        return False
    return any(p in text for p in positive)


def discover(max_per_query: int = 10, delay: float = 1.1) -> dict:
    domain_data = defaultdict(lambda: {
        "urls": set(),
        "titles": set(),
        "hosts": set(),
        "engines": set(),
        "snippets": [],
    })

    engines = [
        ("DuckDuckGo", search_ddg),
        ("Brave", search_brave),
        ("Bing (via DDG)", search_bing_fallback),
    ]

    for host in HOSTS:
        print(f"\n=== Host: {host} ===")
        for template in QUERY_TEMPLATES:
            query = template.format(host=host)
            print(f"  {query[:90]}...")

            for engine_name, search_fn in engines:
                hits = search_fn(query, max_results=max_per_query)
                for hit in hits:
                    url = hit.get("url", "")
                    domain = extract_domain(url)
                    if not domain or not is_likely_directory(hit.get("title", ""), hit.get("snippet", ""), url):
                        continue

                    domain_data[domain]["urls"].add(url)
                    domain_data[domain]["titles"].add(hit.get("title", "")[:140])
                    domain_data[domain]["hosts"].add(host)
                    domain_data[domain]["engines"].add(engine_name)
                    if hit.get("snippet"):
                        domain_data[domain]["snippets"].append(hit["snippet"][:200])

                time.sleep(delay)

    # Seed known domains
    for domain in SEED_DOMAINS:
        domain_data[domain]["hosts"].add("seed")
        domain_data[domain]["engines"].add("manual")

    return domain_data


def rank_and_export(domain_data: dict, top_n: int = 60) -> list[dict]:
    ranked = []
    for domain, meta in domain_data.items():
        score = (
            len(meta["hosts"]) * 4 +
            len(meta["engines"]) * 2 +
            len(meta["urls"]) +
            (5 if "seed" in meta["hosts"] else 0)
        )
        ranked.append({
            "domain": domain,
            "score": score,
            "hosts": sorted(meta["hosts"]),
            "engines": sorted(meta["engines"]),
            "example_url": next(iter(meta["urls"]), ""),
            "example_title": next(iter(meta["titles"]), ""),
            "snippet_sample": meta["snippets"][0] if meta["snippets"] else "",
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]


def main():
    print("Discovering movie & TV directories using common hosts...\n")
    data = discover(max_per_query=8, delay=1.0)
    ranked = rank_and_export(data, top_n=60)

    print("\n" + "=" * 80)
    print(f"TOP {len(ranked)} CANDIDATE DOMAINS (movies + TV)")
    print("=" * 80)

    for i, item in enumerate(ranked, 1):
        print(f"\n{i:2d}. {item['domain']}  (score={item['score']})")
        print(f"    Hosts: {', '.join(item['hosts'])}")
        print(f"    Engines: {', '.join(item['engines'])}")
        if item["example_url"]:
            print(f"    URL: {item['example_url']}")
        if item["example_title"]:
            print(f"    Title: {item['example_title']}")

    export = {
        "scope": "movies + television + softcore/erotic",
        "hosts_searched": HOSTS,
        "candidates": ranked,
    }
    with open("/workspace/artifacts/resolver_candidates_movies_tv.json", "w") as f:
        json.dump(export, f, indent=2)

    print("\nExported to /workspace/artifacts/resolver_candidates_movies_tv.json")


if __name__ == "__main__":
    main()
