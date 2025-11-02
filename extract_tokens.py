from mitmproxy import ctx, http
import re, json, time
from urllib.parse import parse_qs

# Corrected regex (must be a string literal)
TARGET_HOST_RE = re.compile(r"tournaments\.kube-prod-us\.us-east-1\.general\.prod\.wildlife\.io", re.I)
PLAYER_PATH_RE = re.compile(r"/players/([^/?#]+)", re.I)

OUTPUT_FILE = "extracted_tokens.txt"

def log_to_file(line: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {line}\n")

class ExtractTokens:
    def __init__(self):
        ctx.log.info("extract_tokens addon loaded; writing results to: %s" % OUTPUT_FILE)

    def request(self, flow: http.HTTPFlow):
        try:
            req = flow.request
            # Some mitmproxy versions expose host as req.host, others via req.pretty_host
            host = getattr(req, "host", None) or getattr(req, "pretty_host", "") or ""
            path = getattr(req, "path", "") or ""
            full_url = getattr(req, "pretty_url", None) or (req.scheme + "://" + host + path)

            # Only inspect requests to the target host and path containing /players/
            if not TARGET_HOST_RE.search(host):
                return
            m = PLAYER_PATH_RE.search(path)
            if not m:
                return

            userid = m.group(1)

            # Attempt to find token in headers first
            headers = {k.lower(): v for k, v in req.headers.items()}
            token = None
            for h in ("token", "authorization", "x-oauth-user", "x-oauth-token", "x-token", "authorizationtoken"):
                if h in headers:
                    token = headers[h]
                    break

            # If not in headers, try JSON body (application/json)
            if not token:
                ctype = headers.get("content-type", "")
                try:
                    body_text = req.get_text(strict=False) or ""
                except Exception:
                    body_text = ""
                if "application/json" in ctype or (body_text and body_text.strip().startswith("{")):
                    try:
                        j = json.loads(body_text)
                        for key in ("token", "auth_token", "authorization", "access_token"):
                            if key in j:
                                token = j.get(key)
                                break
                    except Exception:
                        pass

            # If not, try urlencoded/form body
            if not token:
                if "application/x-www-form-urlencoded" in headers.get("content-type", "") and body_text:
                    qs = parse_qs(body_text)
                    for key in ("token", "auth_token", "access_token"):
                        if key in qs:
                            token = qs[key][0]
                            break

            # Additional fallback: search the entire URL or body with a heuristic (alphanumeric long strings)
            if not token:
                search_text = (full_url + " " + (body_text or ""))[:4000]
                token_match = re.search(r'([A-Za-z0-9\-_\.]{20,200})', search_text)
                if token_match:
                    candidate = token_match.group(1)
                    token = candidate

            if token:
                if isinstance(token, bytes):
                    token = token.decode("utf-8", errors="ignore")
                token = token.strip()
                out = f"USERID={userid} TOKEN={token} URL={full_url}"
                ctx.log.info("Extracted: " + out)
                log_to_file(out)
            else:
                ctx.log.info(f"Hit player endpoint but token not auto-detected. USERID={userid} URL={full_url}")
                log_to_file(f"USERID={userid} TOKEN=NOT_FOUND URL={full_url}")

        except Exception as e:
            ctx.log.error(f"extract_tokens error: {e}")

addons = [
    ExtractTokens()
]
