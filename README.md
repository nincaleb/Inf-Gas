# InfGas — Private Server Session Helper

> **IMPORTANT:** This tool is for **private, authorized testing only**. Only use this on servers or networks you own or where you have explicit permission. Tokens and credentials are sensitive — treat them like passwords.

---

## Table of Contents
- [Prerequisites — Get PC IP & Install mitmproxy (DO THIS FIRST)](#prerequisites--get-pc-ip--install-mitmproxy-do-this-first)
- [One‑click usage (no terminal required)](#one-click-usage-no-terminal-required)
  - [First time (one click)](#first-time-one-click)
  - [Everyday use (one click)](#everyday-use-one-click)
  - [Manual entry (no mitmproxy)](#manual-entry-no-mitmproxy)
- [How the automatic capture works](#how-the-automatic-capture-works)
- [Security & cleanup (must read)](#security--cleanup-must-read)
- [Troubleshooting tips](#troubleshooting-tips)
- [License & contact](#license--contact)

---

## Prerequisites — Get PC IP & Install mitmproxy (DO THIS FIRST)

**You must complete these steps before running the launchers.**

### 1) Find your PC's local IP address (PC_IP)
You need your PC's IPv4 address while the PC and phone are on the **same Wi‑Fi**.

- **Windows (Command Prompt / PowerShell):**
  1. Open Command Prompt or PowerShell.
  2. Run:
     ```
     ipconfig
     ```
  3. Look for **IPv4 Address** under your active Wi‑Fi / Ethernet adapter (example `192.168.1.100`). This is `PC_IP`.

- **macOS (Terminal):**
  ```
  ipconfig getifaddr en0
  ```
  or
  ```
  ifconfig | grep "inet "
  ```
  Use the `inet` address for your active interface (not `127.0.0.1`).

- **Linux (Terminal):**
  ```
  hostname -I
  ```
  or
  ```
  ip addr show
  ```
  Use the address for your active interface (e.g., `wlan0`).

Write down `PC_IP` — you will enter it on the phone as the proxy host.

---

### 2) Install mitmproxy (only if you want automatic credential capture)
You only need mitmproxy if you want InfGas to **auto-detect** USERID and token. If you prefer manual entry, skip this.

**Install with pip (recommended):**
1. Ensure Python and pip are installed.
2. Install:
   ```
   pip install mitmproxy
   ```
3. Verify installation:
   ```
   mitmweb --version
   ```

**Alternative:** Download official installers from https://mitmproxy.org and follow platform instructions.

---

### 3) Phone proxy & certificate setup (essential for HTTPS interception)
After mitmproxy is installed and mitmweb is running (the launcher will start it), do this on your phone:

1. **Set phone Wi‑Fi proxy**  
   - **Android:** Settings → Wi‑Fi → long‑press your network → Modify network → Advanced → Proxy → Manual → Hostname = `PC_IP`, Port = `8080`. Save.  
   - **iOS:** Settings → Wi‑Fi → tap the `i` next to your network → HTTP Proxy → Manual → Server = `PC_IP`, Port = `8080`. Save.

2. **Install mitmproxy certificate**  
   - On the phone, open a browser and go to: `http://mitm.it`  
   - Choose your platform (Android or iOS) and follow install steps.  
   - **iOS extra:** After installing, go to Settings → General → VPN & Device Management (or Profiles) and **Trust** the installed profile.

If `http://mitm.it` does not load, double-check the phone proxy and that mitmweb is running on the PC. Allow firewall access for mitmweb on the PC if prompted.

---

## One‑click usage (no terminal required)

### First time (one click)
1. Place the package folder on the PC that will act as the proxy machine.  
2. Double‑click **`run_all.bat`**.  
   - If **mitmproxy/mitmweb** is installed and on PATH, `run_all.bat` will open mitmweb and then open InfGas in a separate window.  
   - If mitmweb is not installed, the launcher will warn you and still open InfGas so you can enter credentials manually.  
3. On the phone, set proxy to `PC_IP:8080` and install the mitm certificate (`http://mitm.it`).  
4. In the InfGas window choose **"Wait and auto-detect credentials"**. When the addon captures the USERID and token, InfGas will prompt you to use and optionally save them. Once confirmed, InfGas will start the loop and display status messages.

> After credentials are saved once, you typically do not need mitmweb again unless you need to refresh the token.

### Everyday use (one click)
- Double‑click **`run_infgas.bat`**. If `credentials.json` exists, InfGas can load saved credentials and start the loop without additional setup.

### Manual entry (no mitmproxy)
1. Double‑click `run_infgas.bat`.  
2. Choose **"Enter credentials manually"** and paste the USERID and token when prompted.  
3. Optionally save credentials for future runs.

---

## How the automatic capture works
- `extract_tokens.py` is a mitmproxy addon that watches requests made through mitmweb.  
- When it sees a request to the tournaments API, it writes a timestamped line with `USERID=... TOKEN=...` to `extracted_tokens.txt`.  
- InfGas (when in watch mode) monitors `extracted_tokens.txt`, detects credentials, and prompts you to use/save them.

---

## Security & cleanup (must read)
- **Delete** `extracted_tokens.txt` immediately after capturing and saving credentials — it contains raw tokens.  
- **Do not share** `credentials.json`. If you save credentials locally, protect that file or request encryption.  
- Only run this tool on networks and machines you control. Intercepting traffic without authorization is illegal and unethical.

---

## Troubleshooting tips
- **Launcher warns mitmweb not found:** install mitmproxy and add it to PATH, or run mitmweb manually.  
- **`http://mitm.it` won’t load:** verify phone proxy (PC_IP:8080) and that mitmweb is running on the PC. Check firewall.  
- **InfGas doesn’t detect credentials:** open mitmweb UI (launcher opens it) and inspect captured requests. If token is stored in a nonstandard header or body field, the addon can be adjusted.

---

## License & contact
This project is distributed under the **MIT License** (LICENSE file included in this repository). For questions or support, contact me on Discord: **nincaleb**.
