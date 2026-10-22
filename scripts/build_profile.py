"""Build the profile card: an ASCII portrait beside a neofetch-style readout.

Writes dark_mode.svg and light_mode.svg. The GitHub numbers are fetched live
(GitHub REST and GraphQL APIs) every time this runs; a scheduled workflow runs
it daily. Standard library only.

    GITHUB_TOKEN=... python scripts/build_profile.py

Without a token it still works, on the unauthenticated REST limit, and leaves
the one GraphQL-only number (repositories contributed to) out.
"""

import datetime as dt
import json
import os
import time
import urllib.error
import urllib.request
from html import escape
from pathlib import Path

USER = "abhinavtop1G"
ROOT = Path(__file__).resolve().parent.parent
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
# The B.E. began in August 2025 (the résumé gives the month, not the day).
STARTED = dt.date(2025, 8, 1)

# ---------------------------------------------------------------- GitHub data


def request(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-card"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if body else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read()
            return res.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, None


def rest(path):
    return request(f"https://api.github.com{path}")


def owned_repos():
    repos, page = [], 1
    while True:
        status, chunk = rest(f"/users/{USER}/repos?type=owner&per_page=100&page={page}")
        if status != 200 or not chunk:
            break
        repos += chunk
        page += 1
    return [r for r in repos if not r.get("fork")]


def contributor_stats(full_name):
    """Commits and lines added/removed by USER on the default branch. The
    endpoint answers 202 while GitHub computes the numbers, so retry."""
    for _ in range(8):
        status, data = rest(f"/repos/{full_name}/stats/contributors")
        if status == 200 and isinstance(data, list):
            for entry in data:
                if (entry.get("author") or {}).get("login", "").lower() == USER.lower():
                    weeks = entry.get("weeks", [])
                    return entry.get("total", 0), sum(w["a"] for w in weeks), sum(w["d"] for w in weeks)
            return 0, 0, 0
        if status == 202:
            time.sleep(3)
            continue
        return 0, 0, 0  # 204 (empty repository) or an error
    return 0, 0, 0


def contributed_count():
    if not TOKEN:
        return None
    query = (
        "query($login:String!){user(login:$login){repositoriesContributedTo("
        "contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY],includeUserRepositories:true){totalCount}}}"
    )
    status, data = request("https://api.github.com/graphql", {"query": query, "variables": {"login": USER}})
    try:
        return data["data"]["user"]["repositoriesContributedTo"]["totalCount"]
    except (TypeError, KeyError):
        return None


def github_stats():
    repos = owned_repos()
    _, user = rest(f"/users/{USER}")
    commits = added = deleted = 0
    for r in repos:
        c, a, d = contributor_stats(r["full_name"])
        commits += c
        added += a
        deleted += d
    return {
        "repos": len(repos),
        "contributed": contributed_count(),
        "stars": sum(r.get("stargazers_count", 0) for r in repos),
        "followers": (user or {}).get("followers", 0),
        "commits": commits,
        "added": added,
        "deleted": deleted,
    }


def uptime(today=None):
    today = today or dt.date.today()
    months = (today.year - STARTED.year) * 12 + today.month - STARTED.month - (today.day < STARTED.day)
    years, months = divmod(max(0, months), 12)
    plural = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return ", ".join(p for p in [plural(years, "year") if years else "", plural(months, "month")] if p)


# ---------------------------------------------------------------- the readout

WIDTH = 60  # characters in the readout column


def kv(key, value):
    """'. Key: ..... value', dot leaders filling the line to WIDTH."""
    head = f". {key}:"
    dots = WIDTH - len(head) - len(value) - 2
    return [("cc", ". "), ("key", f"{key}:"), ("cc", " " + "." * max(1, dots) + " "), ("value", value)]


def pair(k1, v1, w1, k2, v2):
    """Two short fields on one line, like 'Repos: .. 9 | Stars: .. 3'."""
    left = f". {k1}: " + "." * max(1, w1 - len(k1) - len(v1) - 4) + f" {v1}"
    right_dots = WIDTH - len(left) - len(f" | {k2}: ") - len(v2) - 1
    return [
        ("cc", ". "),
        ("key", f"{k1}:"),
        ("cc", " " + "." * max(1, w1 - len(k1) - len(v1) - 4) + " "),
        ("value", v1),
        ("cc", " | "),
        ("key", f"{k2}:"),
        ("cc", " " + "." * max(1, right_dots) + " "),
        ("value", v2),
    ]


def rule(title):
    if not title:
        return [("cc", ".")]
    head = f"- {title} "
    return [("cc", "- "), ("head", title), ("cc", " " + "—" * (WIDTH - len(head) - 1) + "-")]


def lines(s):
    n = lambda v: f"{v:,}"
    contributed = f" {{Contributed: {s['contributed']}}}" if s["contributed"] is not None else ""
    loc = s["added"] - s["deleted"]
    return [
        [("head", "abhinav@saini"), ("cc", " " + "—" * (WIDTH - 15) + "-")],
        kv("OS", "Windows 11, Linux"),
        kv("Uptime (B.E.)", uptime()),
        kv("Host", "Thapar Institute, Patiala"),
        kv("Kernel", "Deep learning, machine learning"),
        kv("IDE", "VS Code, Jupyter"),
        rule(""),
        kv("Languages.Programming", "Python, C++"),
        kv("Languages.ML", "PyTorch, TensorFlow, scikit-learn"),
        kv("Languages.Models", "Transformers, YOLO, XGBoost"),
        kv("Focus", "Training, fine-tuning, RAG"),
        rule(""),
        kv("Hobbies.Board", "Chess, state level, 1700+"),
        kv("Recognition", "HackOWASP finalist, 150+ teams"),
        rule(""),
        rule("Projects"),
        kv("BarrierX", "Safety-report triage, DeBERTa"),
        kv("UPI Scam Detection", "GRU + XGBoost, p95 60.9 ms"),
        kv("VeriFEarth", "NLP x Sentinel-2, 0.95 F1"),
        kv("Kaggle S6E8", "3-model blend, 0.96561 AUC"),
        kv("Vehicle Detection", "Real-time YOLO, on-device"),
        rule(""),
        rule("Contact"),
        kv("Email", "abhinavsaini.ml@gmail.com"),
        kv("Portfolio", "abhinav-saini-portfolio.vercel.app"),
        kv("LinkedIn", "abhinav-saini"),
        rule(""),
        rule("GitHub Stats"),
        pair("Repos", f"{s['repos']}{contributed}", 27, "Stars", n(s["stars"])),
        pair("Commits", n(s["commits"]), 27, "Followers", n(s["followers"])),
        [
            ("cc", ". "),
            ("key", "Lines of Code on GitHub:"),
            ("cc", " " + "." * max(1, WIDTH - 30 - len(n(loc)) - len(n(s["added"])) - len(n(s["deleted"])) - 10) + " "),
            ("value", n(loc)),
            ("cc", " ( "),
            ("add", f"{n(s['added'])}++"),
            ("cc", ", "),
            ("del", f"{n(s['deleted'])}--"),
            ("cc", " )"),
        ],
    ]


# ---------------------------------------------------------------- the SVG

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "edge": "#30363d",
        "head": "#f0f6fc",
        "key": "#e2cb9f",
        "value": "#c9d1d9",
        "cc": "#484f58",
        "add": "#3fb950",
        "del": "#f85149",
        "tones": ["#6b5d45", "#b09c76", "#f3e6c8"],
        "scan": "#e2cb9f",
        "cursor": "#e2cb9f",
    },
    "light": {
        "bg": "#f6f8fa",
        "edge": "#d0d7de",
        "head": "#1f2328",
        "key": "#8a6223",
        "value": "#1f2328",
        "cc": "#b1bac4",
        "add": "#1a7f37",
        "del": "#cf222e",
        "tones": ["#b9ab90", "#7a6338", "#2b2416"],
        "scan": "#8a6223",
        "cursor": "#8a6223",
    },
}

FONT = 14
CW = 8.4  # monospace advance at 14px
LH = 17
PAD_X, PAD_Y = 24, 30
GAP = 3  # columns between portrait and readout
# The portrait is set smaller than the readout, so it has the rows a face needs.
P_FONT = 9  # px, and also the distance between its rows
P_CW = P_FONT * 0.6
ROW_STEP = 0.045  # s between one portrait row and the one above it
ROW_FADE = 0.7  # s for each row to fade in
SCAN_H = 64  # px, the glow that leads the reveal up the portrait


def render(theme, readout, portrait):
    t = THEMES[theme]
    cols, rows = portrait["cols"], portrait["rows"]
    pw, ph = cols * P_CW, rows * P_FONT
    readout_x = PAD_X + pw + GAP * CW
    width = round(readout_x + WIDTH * CW + PAD_X)
    height = round(PAD_Y + len(readout) * LH + PAD_Y - LH / 2)
    # Centre the portrait on the readout's block of text.
    block_top, block_h = PAD_Y - FONT * 0.8, (len(readout) - 1) * LH + FONT
    py = block_top + (block_h - ph) / 2
    reveal = rows * ROW_STEP

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'Courier New\',monospace" '
        f'width="{width}px" height="{height}px" font-size="{FONT}px" role="img" '
        f'aria-label="Abhinav Saini: an ASCII portrait beside a terminal-style readout of skills, projects, contact and live GitHub stats">',
        "<style>",
        "@font-face{src:local('Consolas'),local('Consolas Bold');font-family:'ConsolasFallback';font-display:swap;"
        "-webkit-size-adjust:109%;size-adjust:109%;}",
        "text,tspan{white-space:pre;}",
        f".head{{fill:{t['head']};font-weight:bold}}.key{{fill:{t['key']}}}.value{{fill:{t['value']}}}"
        f".cc{{fill:{t['cc']}}}.add{{fill:{t['add']}}}.del{{fill:{t['del']}}}",
        *[f".t{j}{{fill:{c}}}" for j, c in enumerate(t["tones"])],
        # The portrait fades in once, row by row, from the bottom up, led by a scan line.
        f".pr{{font-size:{P_FONT}px;opacity:0;animation:rise {ROW_FADE}s ease-out forwards}}",
        "@keyframes rise{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:none}}",
        f".scan{{opacity:0;animation:scan {reveal:.2f}s linear .3s forwards}}",
        f"@keyframes scan{{0%{{opacity:0;transform:none}}8%{{opacity:1}}88%{{opacity:1}}"
        f"100%{{opacity:0;transform:translateY(-{ph:.0f}px)}}}}",
        # The readout types itself in, line by line, once.
        ".ln{opacity:0;animation:type .35s ease-out forwards}",
        "@keyframes type{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}",
        f".cursor{{fill:{t['cursor']};animation:blink 1.1s step-end infinite}}",
        "@keyframes blink{50%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.pr,.ln{animation:none;opacity:1}.scan{display:none}.cursor{animation:none}}",
        "</style>",
        f'<rect width="{width}px" height="{height}px" fill="{t["bg"]}" stroke="{t["edge"]}" rx="15"/>',
        "<defs>",
        f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["scan"]}" stop-opacity="0"/>'
        f'<stop offset=".12" stop-color="{t["scan"]}" stop-opacity=".45"/><stop offset="1" stop-color="{t["scan"]}" stop-opacity="0"/></linearGradient>',
        "</defs>",
    ]

    # One group per row, each tone its own layer of text; rows start from the bottom.
    for r in range(rows):
        chars, bands = portrait[theme]["chars"][r], portrait[theme]["bands"][r]
        if not chars.strip():
            continue
        y = py + r * P_FONT + P_FONT * 0.8
        delay = (rows - 1 - r) * ROW_STEP + 0.3
        out.append(f'<g class="pr" style="animation-delay:{delay:.3f}s">')
        for j in range(len(t["tones"])):
            layer = "".join(ch if b == str(j) else " " for ch, b in zip(chars, bands)).rstrip()
            if layer.strip():
                out.append(f'<text class="t{j}" x="{PAD_X}" y="{y:.1f}">{escape(layer)}</text>')
        out.append("</g>")
    out.append(
        f'<rect class="scan" x="{PAD_X - 8}" y="{py + ph - SCAN_H * 0.12:.1f}" width="{pw + 16:.1f}" height="{SCAN_H}" fill="url(#scan)"/>'
    )

    for i, parts in enumerate(readout):
        y = PAD_Y + i * LH
        spans = "".join(f'<tspan class="{cls}">{escape(txt)}</tspan>' for cls, txt in parts)
        out.append(f'<text class="ln" x="{readout_x:.1f}" y="{y:.1f}" style="animation-delay:{0.15 + i * 0.045:.3f}s">{spans}</text>')
    last_len = sum(len(txt) for _, txt in readout[-1])
    cy = PAD_Y + (len(readout) - 1) * LH
    out.append(f'<rect class="cursor" x="{readout_x + (last_len + 1) * CW:.1f}" y="{cy - FONT + 3:.1f}" width="{CW:.1f}" height="{FONT:.1f}"/>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    portrait = json.loads((ROOT / "scripts" / "portrait.json").read_text())
    stats = github_stats()
    print(json.dumps(stats))
    readout = lines(stats)
    for theme in THEMES:
        (ROOT / f"{theme}_mode.svg").write_text(render(theme, readout, portrait), encoding="utf-8")
    print("wrote dark_mode.svg and light_mode.svg")


if __name__ == "__main__":
    main()
