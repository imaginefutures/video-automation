"""Download the Opus 5.5 reference videos and their prompts listed in cases.txt.

The videos and prompts belong to their creators, so this repo ships only the
case list and _META.md. Each user runs this script to pull the files from the
source (jasonzhu.ai data + X video CDN) into this folder.

    python3 video-references/opus-5.5/fetch.py          # download missing cases
    python3 video-references/opus-5.5/fetch.py --new    # list newer full-prompt cases not in cases.txt
    python3 video-references/opus-5.5/fetch.py --only <name> ...   # just these cases

scripts/inserts.py imports fetch_cases() to pull only the 1-3 references it picked for a motion
insert, so a user without the full library still gets the catalog-wide pick.

Stdlib only. Files that already exist are skipped, so it is safe to rerun.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_URL = "https://jasonzhu.ai/data/opus-prompts/index.json"
PROMPT_URL = "https://jasonzhu.ai/data/opus-prompts/{id}.json"
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=120).read()
        except Exception as e:
            err = e
            time.sleep(2 * (attempt + 1))
    raise err


def write_prompt_md(path, name, r, prompt):
    v, p, s = r["video"], r["prompt"], r["stats"]
    group = f"{r['group']['key']} (size {r['group']['size']})" if r.get("group") else "-"
    lines = [
        f"# {r['title']['en']}", "",
        f"- id: {r['id']}",
        f"- video: {name}.mp4 ({v['width']}x{v['height']}, {v['durationSec']}s)",
        f"- author: @{r['author']['handle']} ({r['author']['name']})",
        f"- post: {r['url']}",
        f"- prompt source: {p['source']} ({p.get('sourceUrl', '')})",
        f"- models: {', '.join(r['models'])}",
        f"- category: {r['category']}",
        f"- tools: {', '.join(r.get('tools') or []) or '-'}",
        f"- needs reference assets: {r.get('referenceAssets')}",
        f"- group: {group}",
        f"- stats: views {s['views']}, likes {s['likes']}, bookmarks {s['bookmarks']}",
        f"- posted: {r['postedAt'][:10]}",
        "", "## Prompt", "", "````text", prompt.rstrip(), "````", "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def load_index():
    return {r["id"]: r for r in json.loads(get(INDEX_URL))}


def fetch_one(name, index):
    """Download one case (prompt .md + .mp4) into this folder. Returns None, or why it failed."""
    cid = name.rsplit("__", 1)[1]
    r = index.get(cid)
    if r is None:
        return "gone from source index"
    mp4 = os.path.join(HERE, name + ".mp4")
    md = os.path.join(HERE, name + ".md")
    try:
        if not os.path.exists(md):
            prompt = json.loads(get(PROMPT_URL.format(id=cid)))["prompt"]
            write_prompt_md(md, name, r, prompt)
        if not os.path.exists(mp4) or os.path.getsize(mp4) == 0:
            data = get(r["video"]["mp4"])
            with open(mp4 + ".part", "wb") as f:
                f.write(data)
            os.replace(mp4 + ".part", mp4)
    except Exception as e:
        return f"failed: {e}"
    return None


def fetch_cases(names):
    """{name: None | why it failed} for the given case names (already-present files are skipped)."""
    index = load_index()
    with ThreadPoolExecutor(max(1, len(names))) as ex:  # the source CDN is slow (~2 min per video) - fetch in parallel
        return dict(zip(names, ex.map(lambda n: fetch_one(n, index), names)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", action="store_true", help="list full-prompt Opus 5.5 cases missing from cases.txt")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--only", nargs="+", help="case names to fetch (default: every case in cases.txt)")
    args = ap.parse_args()

    with open(os.path.join(HERE, "cases.txt"), encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]
    # The post id is the last "__" segment of each name.
    wanted = {n.rsplit("__", 1)[1]: n for n in names}

    if args.only:
        wanted = {n.rsplit("__", 1)[1]: n for n in args.only}
    index = load_index()

    if args.new:
        new = [r for r in index.values()
               if "opus-5.5" in (r.get("models") or [])
               and (r.get("prompt") or {}).get("kind") == "full"
               and r["id"] not in wanted]
        for r in new:
            print(f"{r['id']}  {r['category']:<11} {r['title']['en']}")
        print(f"{len(new)} new case(s) not in cases.txt", file=sys.stderr)
        return

    def work(item):
        cid, name = item
        return name, fetch_one(name, index)

    with ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(work, wanted.items()))

    failed = [(n, why) for n, why in results if why]
    print(f"{len(results) - len(failed)}/{len(results)} cases ready in {HERE}")
    for n, why in failed:
        print(f"  {n}: {why}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
