# InfGas — Private Server Session Helper

> **IMPORTANT:** This tool is for **private, authorized testing only**. Only use this on servers or networks you own or where you have explicit permission to test. Tokens and credentials are sensitive — treat them like passwords.

---

## 📥 Download (Pre‑Built Version)
You **do not** need to build anything yourself. Download the ready‑to‑use ZIP from the latest release:

👉 **https://github.com/nincaleb/Inf-Gas/releases/latest**

Extract the ZIP, then follow the steps below.

---

## Table of Contents
- [Prerequisites — Get PC IP & Install mitmproxy (DO THIS FIRST)](#prerequisites--get-pc-ip--install-mitmproxy-do-this-first)
- [One‑click usage (no terminal required)](#one-click-usage-no-terminal-required)
  - [First time setup](#first-time-setup)
  - [Future runs (easy mode)](#future-runs-easy-mode)
  - [No mitmproxy mode](#no-mitmproxy-mode)
- [How automatic capture works](#how-automatic-capture-works)
- [Security & cleanup (IMPORTANT)](#security--cleanup-important)
- [Troubleshooting](#troubleshooting)
- [License & contact](#license--contact)

---

## Prerequisites — Get PC IP & Install mitmproxy (DO THIS FIRST)

### 1) Find your PC's local IP address (PC_IP)
Your PC and your phone must be on the **same Wi‑Fi network**.

**Windows:**
```
ipconfig
```
Find **IPv4 Address** (ex: `192.168.0.146`). This is your `PC_IP`.

**macOS:**
```
ipconfig getifaddr en0
```
or
```
ifconfig | grep "inet "
```

**Linux:**
```
hostname -I
```
or
```
ip addr show
```

---

### 2) Install mitmproxy (only required for automatic credential capture)
If you want InfGas to **auto‑detect** USERID and token, install mitmproxy. Otherwise skip to the phone proxy step or use Manual mode later.

Install with pip (recommended):
```
pip install mitmproxy
```
Verify:
```
mitmweb --version
```

Or download from: https://mitmproxy.org

---

### 3) Phone Proxy Setup + Certificate (essential for HTTPS interception)
1. Set phone Wi‑Fi proxy → **Manual**  
   - **Server:** `PC_IP` (from step 1)  
   - **Port:** `8080`

2. On the phone, visit: **http://mitm.it**  
   - Install the certificate (choose *Android* or *iOS*).  
   - **iOS extra step:** Settings → General → VPN & Device Management (or Profiles) → **Trust** the installed profile.

If the page doesn’t load, confirm the phone proxy and ensure mitmweb is running (the launcher can open it if installed). Allow the Windows Firewall prompt if it appears.

---

## One‑click usage (no terminal required)

### First time setup
1. **Download and extract** the ZIP from **Releases**: https://github.com/nincaleb/Inf-Gas/releases/latest  
2. Double‑click **`run_all.bat`**.  
   - If mitmproxy is installed and on PATH, this opens mitmweb and then starts InfGas.  
3. On your phone, open the game to trigger the API call (e.g., open a tournament).  
4. In InfGas, choose **“Wait and auto‑detect credentials.”** When detected, confirm and (optionally) **save** them.  
5. The loop starts; the console will show `Added Gas` or status messages.

> After saving credentials once, you typically don’t need mitmweb again unless your token changes.

### Future runs (easy mode)
Double‑click **`run_infgas.bat`**. If `credentials.json` exists, InfGas can load it and start immediately.

### No mitmproxy mode
- Double‑click `run_infgas.bat`  
- Choose **Manual Entry** and paste your USERID + Token  
- Optionally save them for next time

---

## How automatic capture works
- `extract_tokens.py` (mitmproxy addon) watches requests through mitmweb.  
- When it sees the tournaments API, it writes a line with `USERID=... TOKEN=...` to `extracted_tokens.txt`.  
- InfGas (watch mode) detects that line, prompts to use/save, and starts the loop.

---

## Security & cleanup (IMPORTANT)
| File | Share it? | Notes |
|---|---|---|
| `credentials.json` | ❌ **No** | Contains your token; keep private. |
| `extracted_tokens.txt` | ❌ **No** | Delete after first setup; contains raw token. |
| Release ZIP | ✅ **Yes** | Safe to share with other authorized users. |

Run this tool **only** on networks/devices you control. Intercepting traffic without authorization is illegal and unethical.

---

## Troubleshooting
| Problem | Fix |
|---|---|
| `http://mitm.it` won’t load | Re‑check phone proxy (`PC_IP:8080`), ensure mitmweb is running, allow firewall prompt. |
| InfGas never detects token | Open a tournament screen in the game so the players API call happens. |
| mitmweb doesn’t start | Install mitmproxy (`pip install mitmproxy`) or add to PATH. |
| Saved creds not loading | Ensure `credentials.json` is in the same folder as the EXE. |

---

## License & contact
This project is distributed under the **MIT License** (see `LICENSE` in the repo).  
For questions or support, contact me on Discord: **nincaleb**.
