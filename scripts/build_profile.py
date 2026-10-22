"""Build the profile card: a turning ASCII Earth beside a neofetch-style readout.

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
        "contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY],includeUserRepositories:false){totalCount}}}"
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
        "land": "#d8c49b",
        "sea": "#3a4b63",
        "orbit": "#55657c",
        "home": "#ff7b72",
        "sats": ["#e2cb9f", "#d9907e", "#a9c29b", "#93a3d6", "#e4b06a"],
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
        "land": "#6e5a33",
        "sea": "#a9b7c6",
        "orbit": "#8d9aab",
        "home": "#cf222e",
        "sats": ["#9a7a3c", "#b3563f", "#4f7a45", "#4459a0", "#a8691b"],
        "cursor": "#8a6223",
    },
}

FONT = 14
CW = 8.4  # monospace advance at 14px
LH = 17
PAD_X, PAD_Y = 24, 30
GAP = 3  # columns between globe and readout


def render(theme, readout, globe):
    t = THEMES[theme]
    cols, rows, frames = globe["cols"], globe["rows"], globe["frames"]
    readout_x = PAD_X + (cols + GAP) * CW
    width = round(readout_x + WIDTH * CW + PAD_X)
    height = round(PAD_Y + len(readout) * LH + PAD_Y - LH / 2)
    globe_y = PAD_Y + (len(readout) * LH - rows * LH) / 2
    period = len(frames) * 0.5
    step = 100 / len(frames)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'Courier New\',monospace" '
        f'width="{width}px" height="{height}px" font-size="{FONT}px" role="img" '
        f'aria-label="Abhinav Saini: an ASCII Earth turning beside a terminal-style readout of skills, projects, contact and live GitHub stats">',
        "<style>",
        "@font-face{src:local('Consolas'),local('Consolas Bold');font-family:'ConsolasFallback';font-display:swap;"
        "-webkit-size-adjust:109%;size-adjust:109%;}",
        "text,tspan{white-space:pre;}",
        f".head{{fill:{t['head']};font-weight:bold}}.key{{fill:{t['key']}}}.value{{fill:{t['value']}}}"
        f".cc{{fill:{t['cc']}}}.add{{fill:{t['add']}}}.del{{fill:{t['del']}}}",
        f".land{{fill:{t['land']}}}.sea{{fill:{t['sea']}}}.orbit{{fill:{t['orbit']}}}"
        f".home{{fill:{t['home']};font-weight:bold}}",
        *[f".sat{j}{{fill:{c};font-weight:bold}}" for j, c in enumerate(t["sats"])],
        # The planet turns: one frame shown at a time, half a second each.
        f".frame{{opacity:0;animation:spin {period}s step-end infinite}}",
        f"@keyframes spin{{0%{{opacity:1}}{step:.4f}%{{opacity:0}}100%{{opacity:0}}}}",
        # The readout types itself in, line by line, once.
        ".ln{opacity:0;animation:type .35s ease-out forwards}",
        "@keyframes type{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}",
        f".cursor{{fill:{t['cursor']};animation:blink 1.1s step-end infinite}}",
        "@keyframes blink{50%{opacity:0}}",
        "@media (prefers-reduced-motion:reduce){.frame{animation:none}.f0{opacity:1}.ln{animation:none;opacity:1}.cursor{animation:none}}",
        "</style>",
        f'<rect width="{width}px" height="{height}px" fill="{t["bg"]}" stroke="{t["edge"]}" rx="15"/>',
    ]

    for k, f in enumerate(frames):
        delay = k * 0.5 - period
        out.append(f'<g class="frame f{k}" style="animation-delay:{delay:.1f}s">')
        for layer in ("sea", "orbit", "land"):
            out.append(f'<text class="{layer}">')
            for r, row in enumerate(f[layer]):
                if row.strip():
                    out.append(f'<tspan x="{PAD_X}" y="{globe_y + r * LH:.1f}">{escape(row)}</tspan>')
            out.append("</text>")
        for m in f["marks"]:
            x = PAD_X + m["c"] * CW
            y = globe_y + m["r"] * LH
            out.append(f'<text class="{m["kind"]}" x="{x:.1f}" y="{y:.1f}">{escape(m["ch"])}</text>')
        out.append("</g>")

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
    globe = json.loads((ROOT / "scripts" / "globe.json").read_text())
    stats = github_stats()
    print(json.dumps(stats))
    readout = lines(stats)
    for theme in THEMES:
        (ROOT / f"{theme}_mode.svg").write_text(render(theme, readout, globe), encoding="utf-8")
    print("wrote dark_mode.svg and light_mode.svg")


if __name__ == "__main__":
    main()
