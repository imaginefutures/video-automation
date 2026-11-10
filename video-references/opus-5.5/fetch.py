"""Download the Opus 5.5 reference videos and their prompts listed in cases.txt.

The videos and prompts belong to their creators, so this repo ships only the
case list and _META.md. Each user runs this script to pull the files from the
source (jasonzhu.ai data + X video CDN) into this folder.

    python3 video-references/opus-5.5/fetch.py          # download missing cases
    python3 video-references/opus-5.5/fetch.py --new    # list newer full-prompt cases not in cases.txt
    python3 video-references/opus-5.5/fetch.py --sync   # add those to cases.txt, download them, list missing catalog entries
    python3 video-references/opus-5.5/fetch.py --only <name> ...   # just these cases

scripts/inserts.py imports fetch_cases() to pull only the 1-3 references it picked for a motion
insert, so a user without the full library still gets the catalog-wide pick.

Stdlib only (cases from the second source also need the yt-dlp binary). Files that already exist are skipped, so it is safe to rerun.
How a sync works end to end (selection rule, naming, catalog writing, log) is in _SYNC.md.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = HERE  # where .mp4/.md land; --dir points it elsewhere (e.g. the main checkout while cases.txt is edited in a worktree)
INDEX_URL = "https://jasonzhu.ai/data/opus-prompts/index.json"
PROMPT_URL = "https://jasonzhu.ai/data/opus-prompts/{id}.json"
UA = {"User-Agent": "Mozilla/5.0"}
# Second source for ids missing from INDEX_URL: the middle "__" segment of the name is a slug in this
# repo's videos.json. It has no video files, so the video comes from the X post via yt-dlp.
# Its rows are selected by new_extra_cases(); it stopped updating on 2026-10-12.
EXTRA_URL = "https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/main/data/videos.json"


# Cases picked by hand from sources that have no data file (prompt-motion.com, 2026-11-10): manual.json keeps each
# case's page and video URL. Only these listed cases are fetched from there - --sync does not look for new ones.
MANUAL_PATH = os.path.join(HERE, "manual.json")


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


def case_name(r):
    """<category>__<title slug, 60 chars max>__<post id> - the naming rule of every jasonzhu case in cases.txt."""
    slug = re.sub(r"[^a-z0-9]+", "-", r["title"]["en"].lower()).strip("-")[:60].strip("-")
    return f"{r['category']}__{slug}__{r['id']}"


def skipped_ids():
    """Post ids in skip.txt (one per line, "# why" allowed): cases --sync must never add again (video gone, etc.)."""
    path = os.path.join(HERE, "skip.txt")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {line.split("#")[0].strip() for line in f} - {""}


def new_cases(index, have_ids):
    """Index rows that pass the selection rule (Opus 5.5 among the models + full prompt) and are not in cases.txt yet."""
    return [r for r in index.values()
            if "opus-5.5" in (r.get("models") or [])
            and (r.get("prompt") or {}).get("kind") == "full"
            and r["id"] not in have_ids]


def new_extra_cases(have_ids):
    """awesome-opus5-5-videos rows that pass its selection rule (whole prompt, 1000+ chars - shorter ones are
    one-liners with no structure to borrow) and whose X post is not in cases.txt yet. Returns case names."""
    out = []
    for v in json.loads(get(EXTRA_URL)):
        m = re.search(r"status(?:es)?/(\d+)", v.get("post_url") or "")
        if m and m.group(1) not in have_ids and not v.get("prompt_partial") and len(v.get("prompt") or "") >= 1000:
            out.append(f"{v['category']}__{v['slug']}__{m.group(1)}")
    return out


def missing_catalog(names):
    """Case names that have no `name` entry in _META.md section 5 yet."""
    with open(os.path.join(HERE, "_META.md"), encoding="utf-8") as f:
        meta = f.read()
    return [n for n in names if f"`{n}`" not in meta]


def load_index():
    return {r["id"]: r for r in json.loads(get(INDEX_URL))}


_extra = {}


def fetch_extra(name):
    """Download one awesome-opus5-5-videos case (prompt .md + .mp4 from the X post). Returns None, or why it failed."""
    try:
        if not _extra:
            _extra.update({v["slug"]: v for v in json.loads(get(EXTRA_URL))})
    except Exception as e:
        return f"failed: {e}"
    v = _extra.get(name.split("__")[1])
    if v is None:
        return "gone from source index"
    md = os.path.join(DATA, name + ".md")
    mp4 = os.path.join(DATA, name + ".mp4")
    if not os.path.exists(md):
        with open(md, "w", encoding="utf-8") as f:
            f.write(f"# {v['slug']}\n\n- 작성자: @{v['author']}\n- 게시물: {v['post_url']}\n"
                    f"- 카테고리: {v['category']} · 기술: {', '.join(v['tech_tags']) or '-'}\n"
                    f"- 출처: yihui-dev/awesome-opus5-5-videos (콘텐츠 권리는 각 크리에이터)\n\n"
                    f"## 프롬프트\n\n{v['prompt']}\n")
    if not os.path.exists(mp4) or os.path.getsize(mp4) == 0:
        if not shutil.which("yt-dlp"):
            return "failed: yt-dlp not installed (brew install yt-dlp)"
        r = subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", "best[ext=mp4]/best",
                            "--merge-output-format", "mp4", "-o", mp4, v["post_url"]],
                           capture_output=True, text=True)
        if r.returncode:
            return "failed: " + (r.stderr.strip().splitlines() or ["yt-dlp"])[-1]
    return None


def page_prompt(html):
    """The prompt on a prompt-motion.com case page. Next.js streams the page data as self.__next_f.push([1, "..."])
    chunks; a long prompt is a "$<hex>" reference to a "<hex>:T<byte length>,<text>" record in that stream."""
    stream = "".join(json.loads(f'"{p}"') for p in re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.S))
    m = re.search(r'"prompt":"((?:[^"\\]|\\.)*)"', stream)
    if not m:
        raise ValueError("no prompt on the page")
    value = json.loads(f'"{m.group(1)}"')
    if re.fullmatch(r"\$[0-9a-f]+", value):
        head, body = stream[stream.index(value[1:] + ":T"):].split(",", 1)
        value = body.encode()[:int(head.split(":T")[1], 16)].decode(errors="ignore")
    return value


def fetch_manual(m):
    """Download one manual.json case (prompt .md from its page + .mp4 from the site's own media). None, or why it failed."""
    md = os.path.join(DATA, m["name"] + ".md")
    mp4 = os.path.join(DATA, m["name"] + ".mp4")
    try:
        if not os.path.exists(md):
            prompt = page_prompt(get(m["page"]).decode("utf-8"))
            with open(md, "w", encoding="utf-8") as f:
                f.write(f"# {m['title']}\n\n- 작성자: @{m['author']}\n- 게시물: https://x.com/{m['author']}/status/{m['name'].rsplit('__', 1)[1]}\n"
                        f"- 게시일: {m['posted']}\n- 출처: {m['source']} ({m['page']}, 콘텐츠 권리는 각 크리에이터)\n\n"
                        f"## Prompt\n\n````text\n{prompt.rstrip()}\n````\n")
        if not os.path.exists(mp4) or os.path.getsize(mp4) == 0:
            with open(mp4 + ".part", "wb") as f:
                f.write(get(m["video"]))
            os.replace(mp4 + ".part", mp4)
    except Exception as e:
        return f"failed: {e}"
    return None


def load_manual():
    if not os.path.exists(MANUAL_PATH):
        return {}
    with open(MANUAL_PATH, encoding="utf-8") as f:
        return {m["name"]: m for m in json.load(f)}


def fetch_one(name, index):
    """Download one case (prompt .md + .mp4) into this folder. Returns None, or why it failed."""
    manual = load_manual().get(name)
    if manual:
        return fetch_manual(manual)
    cid = name.rsplit("__", 1)[1]
    r = index.get(cid)
    if r is None or r.get("prompt") is None:  # not on jasonzhu, or listed there without a prompt: second source
        return fetch_extra(name)
    mp4 = os.path.join(DATA, name + ".mp4")
    md = os.path.join(DATA, name + ".md")
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
    ap.add_argument("--new", action="store_true", help="list cases from both sources that pass the selection rule and are missing from cases.txt")
    ap.add_argument("--sync", action="store_true",
                    help="append those cases to cases.txt, download them, list cases missing a _META.md entry")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--dir", help="download into this folder instead of next to this script")
    ap.add_argument("--only", nargs="+", help="case names to fetch (default: every case in cases.txt)")
    args = ap.parse_args()
    global DATA
    if args.dir:
        DATA = os.path.abspath(args.dir)

    with open(os.path.join(HERE, "cases.txt"), encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]
    # The post id is the last "__" segment of each name.
    wanted = {n.rsplit("__", 1)[1]: n for n in names}

    if args.only:
        wanted = {n.rsplit("__", 1)[1]: n for n in args.only}
    index = load_index()

    if args.new or args.sync:
        known = set(wanted) | skipped_ids()
        new = new_cases(index, known)
        for r in new:
            print(f"{r['id']}  {r['category']:<11} {r['title']['en']}")
        print(f"{len(new)} new case(s) not in cases.txt", file=sys.stderr)
        extra = new_extra_cases(known | {r["id"] for r in new})
        for n in extra:
            print(f"{n.rsplit('__', 1)[1]}  extra       {n.split('__')[1]}")
        print(f"{len(extra)} new awesome-opus5-5-videos case(s) not in cases.txt", file=sys.stderr)
        if args.new:
            return
        added = [case_name(r) for r in new] + extra
        with open(os.path.join(HERE, "cases.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(set(names) | set(added))) + "\n")
        wanted = {n.rsplit("__", 1)[1]: n for n in added}

    def work(item):
        cid, name = item
        return name, fetch_one(name, index)

    with ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(work, wanted.items()))

    failed = [(n, why) for n, why in results if why]
    print(f"{len(results) - len(failed)}/{len(results)} cases ready in {DATA}")
    for n, why in failed:
        print(f"  {n}: {why}")
    if args.sync:
        todo = missing_catalog(sorted(set(names) | set(wanted.values())))
        print(f"{len(todo)} case(s) still need a _META.md catalog entry (see _SYNC.md step 3):")
        for n in todo:
            print(f"  {n}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
