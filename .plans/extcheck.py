"""Check external URLs from linkcheck.py's JSON output. Prints anything not 2xx/3xx."""
import json, sys, urllib.request, urllib.error, ssl, concurrent.futures as cf

urls = json.load(open(sys.argv[1]))
SKIP = ("twitter.com/share", "linkedin.com/shareArticle", "fonts.googleapis.com", "fonts.gstatic.com", "googletagmanager.com")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def check(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
            with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as r:
                return url, r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 404, 405, 429, 400, 501): continue
            return url, e.code, ""
        except Exception as e:
            if method == "HEAD": continue
            return url, type(e).__name__ + ": " + str(e)[:80], ""

todo = [u for u in urls if not any(s in u for s in SKIP)]
with cf.ThreadPoolExecutor(12) as ex:
    results = list(ex.map(check, todo))
bad = [r for r in results if not (isinstance(r[1], int) and r[1] < 400)]
print(f"checked {len(todo)}  problems {len(bad)}")
for url, status, _ in sorted(bad, key=lambda r: str(r[1])):
    print(f"{status} | {url} | {', '.join(urls[url][:2])}")
