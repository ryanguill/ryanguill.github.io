"""Check internal links/assets/anchors in a built Jekyll _site; collect external URLs."""
import sys, os, json
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

SITE = sys.argv[1]
HOSTS = {"ryanguill.com", "www.ryanguill.com"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and "name" in a: self.ids.add(a["name"])
        if tag == "link" and a.get("rel") in ("preconnect", "canonical", "alternate"): return
        for k in ("href", "src"):
            if a.get(k): self.refs.append((tag, k, a[k]))

pages = {}
for root, _, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(root, f)
            parser = P(); parser.feed(open(p, encoding="utf-8", errors="replace").read())
            pages[os.path.relpath(p, SITE)] = parser

def resolve(path):
    path = unquote(path)
    full = os.path.join(SITE, path.lstrip("/"))
    if os.path.isfile(full): return os.path.relpath(full, SITE)
    if os.path.isdir(full) and os.path.isfile(os.path.join(full, "index.html")):
        return os.path.relpath(os.path.join(full, "index.html"), SITE)
    if os.path.isfile(full + ".html"): return os.path.relpath(full + ".html", SITE)
    return None

broken, external = [], {}
for page, parser in sorted(pages.items()):
    base = "/" + os.path.dirname(page)
    for tag, attr, url in parser.refs:
        u = urlparse(url)
        if u.scheme in ("mailto", "javascript", "data", "tel"): continue
        if u.scheme in ("http", "https") or url.startswith("//"):
            host = u.netloc
            if host in HOSTS:
                path = u.path or "/"
            else:
                external.setdefault(url if u.scheme else "https:" + url, set()).add(page); continue
        elif url.startswith("#"):
            if url[1:] and unquote(url[1:]) not in parser.ids: broken.append((page, url, "missing anchor"))
            continue
        else:
            path = u.path if u.path.startswith("/") else os.path.normpath(os.path.join(base, u.path))
        target = resolve(path)
        if not target:
            broken.append((page, url, "not found")); continue
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            broken.append((page, url, "missing anchor"))

print(f"pages: {len(pages)}  broken internal: {len(broken)}  external urls: {len(external)}")
for b in broken: print("BROKEN", *b, sep=" | ")
json.dump({k: sorted(v) for k, v in external.items()}, open(sys.argv[2], "w"), indent=1)
