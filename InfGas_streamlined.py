#!/usr/bin/env python3
"""
InfGas_streamlined.py (updated)
- Better handling for extracted_tokens.txt (dedup, .json suffix trimming)
- Uses the first valid credential it finds when watching and ignores duplicates
- Saves credentials optionally to credentials.json
- Same gas loop behavior as before

IMPORTANT: Use only in closed / authorized test environments.
"""

import time
import requests
import json
import os
import re
from pathlib import Path

# --- Configuration ---
SUCCESS_DELAY = 23.0
MAX_BACKOFF = 300.0
FAIL_DELAY = 5.0

CREDENTIALS_FILE = "credentials.json"        # saved credentials (optional)
EXTRACTED_FILE = "extracted_tokens.txt"      # file written by mitmproxy addon
POLL_INTERVAL = 2.0                          # seconds when waiting for extracted file

# --- Helpers ---
def save_credentials(player_id: str, token: str):
    data = {"player_id": player_id, "token": token}
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"[+] Saved credentials to {CREDENTIALS_FILE}")

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        pid = data.get("player_id")
        tok = data.get("token")
        if pid and tok:
            return pid.strip(), tok.strip()
    except Exception as e:
        print(f"[!] Failed to load saved credentials: {e}")
    return None

def parse_extracted_line(line: str):
    """
    Expect lines like:
    [YYYY-MM-DD HH:MM:SS] USERID=<id> TOKEN=<token> URL=<...>
    This returns (userid, token) or (None, None) if not found.
    It will trim a trailing .json from the userid if present.
    """
    uid_m = re.search(r"USERID=([A-Za-z0-9\-_\.]+)", line)
    tok_m = re.search(r"TOKEN=([A-Za-z0-9\-_\.]+)", line)
    uid = uid_m.group(1) if uid_m else None
    tok = tok_m.group(1) if tok_m else None
    if uid and uid.endswith(".json"):
        uid = uid[:-5]
    return uid, tok

def tail_latest_credentials_from_file(path: str):
    """Return the latest parsed (player_id, token) from the extracted file, or (None, None)."""
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        # iterate from the end to find first parseable line
        for ln in reversed(lines):
            pid, tok = parse_extracted_line(ln)
            if pid and tok:
                return pid, tok
    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    return None, None

# --- Main gas loop (unchanged logic, moved into function) ---
def gas_loop(player_id: str, token: str):
    url = f"https://api.tournaments.kube-prod-us.us-east-1.general.prod.wildlife.io/players/{player_id}/ads"
    payload = ""
    headers = {
        "Accept": "application/vnd.topfreegames.com; version=1.6, application/json",
        "Accept-Language": "en-US;q=1, ja-US;q=0.9, ar-US;q=0.8, ko-US;q=0.7",
        "Connection": "keep-alive",
        "Token": token,
        "User-Agent": "moto/8.6.1 (iPhone; iOS 18.3.1; Scale/3.00)",
        "X-Oauth-User": f"{player_id}"
    }

    backoff = SUCCESS_DELAY

    print(f"[+] Starting gas loop for USERID={player_id} ... (Ctrl+C to stop)")
    while True:
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=15)
            sc = response.status_code

            if sc == 204:
                print("Added Gas")
                backoff = SUCCESS_DELAY
                time.sleep(SUCCESS_DELAY)
            elif sc == 429:
                ra = response.headers.get("Retry-After")
                try:
                    ra_val = float(ra) if ra is not None else 0.0
                except ValueError:
                    ra_val = 0.0
                wait_s = max(ra_val, backoff)
                print(f"Rate limited (429). Waiting {wait_s:.1f}s")
                time.sleep(wait_s)
                backoff = min(backoff * 1.5, MAX_BACKOFF)
            elif sc == 422:
                print("Gas full (422). Waiting 23.0s")
                time.sleep(SUCCESS_DELAY)
            else:
                body = response.text[:300] + ("..." if len(response.text) > 300 else "")
                print(f"Failed To Add Gas | Status {sc} | {body}")
                time.sleep(FAIL_DELAY)

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}. Retrying in {backoff:.1f}s")
            time.sleep(backoff)
            backoff = min(backoff * 1.5, MAX_BACKOFF)

# --- Interactive flow ---
def interactive_choose_credentials():
    print("=== InfGas Credential Options ===")
    print("1) Load saved credentials (credentials.json)")
    print("2) Wait and auto-detect credentials from mitmproxy output (extracted_tokens.txt)")
    print("3) Enter credentials manually")
    print("4) Quit")
    choice = input("Choose an option (1-4): ").strip()
    return choice

def main():
    print("InfGas (streamlined) — Authorized use only in private/test environments.")
    # 1) offer to load saved credentials
    creds = load_credentials()
    if creds:
        pid, tok = creds
        print(f"[+] Found saved credentials for USERID={pid}")
        use = input("Load and use saved credentials? (Y/n): ").strip().lower() or "y"
        if use.startswith("y"):
            if input("Run gas loop now with saved credentials? (Y/n): ").strip().lower().startswith("y"):
                gas_loop(pid, tok)
                return
        # else fall through to menu
    while True:
        c = interactive_choose_credentials()
        if c == "1":
            creds = load_credentials()
            if not creds:
                print("[!] No saved credentials found.")
                continue
            pid, tok = creds
            if input(f"Use saved credentials for USERID={pid}? (Y/n): ").strip().lower().startswith("y"):
                gas_loop(pid, tok)
                return
            else:
                continue
        elif c == "2":
            print(f"[i] Watching for credentials in {EXTRACTED_FILE}. Make sure mitmproxy addon is running and writing to that file.")
            print("[i] It will use the first unique credentials detected and then stop watching. Press Ctrl+C to cancel watching and return to menu.")
            seen = set()
            try:
                while True:
                    pid, tok = tail_latest_credentials_from_file(EXTRACTED_FILE)
                    if pid and tok and (pid, tok) not in seen:
                        seen.add((pid, tok))
                        print(f"[+] Detected credentials: USERID={pid}")
                        yn = input("Use these credentials? (Y/n): ").strip().lower() or "y"
                        if yn.startswith("y"):
                            if input("Save these credentials for future runs? (Y/n): ").strip().lower().startswith("y"):
                                save_credentials(pid, tok)
                            gas_loop(pid, tok)
                            return
                        else:
                            print("[i] Ignoring these credentials and continuing to watch for newer ones...")
                    time.sleep(POLL_INTERVAL)
            except KeyboardInterrupt:
                print("\n[i] Stopped watching for credentials. Returning to menu.")
                continue
        elif c == "3":
            pid = input("Paste your ID Here: ").strip()
            tok = input("Paste your Token Here: ").strip()
            if not pid or not tok:
                print("[!] Both ID and Token are required.")
                continue
            if input("Save these credentials for future runs? (Y/n): ").strip().lower().startswith("y"):
                save_credentials(pid, tok)
            gas_loop(pid, tok)
            return
        elif c == "4":
            print("Goodbye.")
            return
        else:
            print("[!] Invalid option. Choose 1-4.")

if __name__ == "__main__":
    main()
