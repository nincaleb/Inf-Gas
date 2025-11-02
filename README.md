# README.md — Capture Bike Race `USERID` & `token` (single-file guide)

> **IMPORTANT:** Only use this guide in a closed environment on servers and devices you own or are explicitly authorized to test. Intercepting traffic for services you do **not** own or have permission to test is unethical and may be illegal.

---

## What this does
This guide shows how to capture the `USERID` and `token` used by the Bike Race tournaments API so you can run `InfGas.exe` on your PC in a closed/test environment. The tool `mitmproxy` (mitmweb) will run on your PC and the phone will use your PC as an HTTP(S) proxy so the request to:

```
https://api.tournaments.kube-prod-us.us-east-1.general.prod.wildlife.io/players/[USERID]
```

can be inspected. After you copy the `USERID` and `token`, you can stop proxying and run `InfGas.exe` locally.

---

## Prerequisites
- PC and phone connected to the **same local network / Wi-Fi**.  
- `mitmproxy` installed on the PC (download from https://mitmproxy.org or install via `pip install mitmproxy`).  
- `InfGas.exe` already built and available on the PC.  
- A terminal / command prompt on the PC.

---

## 1) Find your PC’s local IP address
You will need the PC’s IPv4 address (example: `192.168.1.100`). Run the appropriate command:

- **Windows (Command Prompt):**
  ```cmd
  ipconfig
  ```
  Look for `IPv4 Address` under the active Wi-Fi / Ethernet adapter.

- **macOS (Terminal):**
  ```bash
  ipconfig getifaddr en0
  ```
  or
  ```bash
  ifconfig | grep "inet "
  ```
  (Use the `inet` address for the active interface; ignore `127.0.0.1`.)

- **Linux (Terminal):**
  ```bash
  hostname -I
  ```
  or
  ```bash
  ip addr show
  ```

Write down the IPv4 address — we will call it `PC_IP` in the steps below.

---

## 2) Start mitmweb on the PC
Open a terminal on the PC and run mitmweb so it listens for connections from other devices:

```bash
mitmweb --listen-host 0.0.0.0 --listen-port 8080
```

Notes:
- `--listen-host 0.0.0.0` allows other devices on the LAN to connect.  
- `--listen-port 8080` sets the proxy port.  
- If Windows firewall prompts, allow mitmproxy or allow traffic on port `8080`.

mitmweb provides a web UI for inspecting requests (usually available at `http://127.0.0.1:8081` on the PC).

---

## 3) Set your phone to use the PC as a proxy
On the phone, configure the Wi-Fi network to use `PC_IP` and port `8080` as the HTTP proxy.

- **Android:** Settings → Wi-Fi → long-press current network → Modify network → Advanced options → Proxy → Manual → Hostname = `PC_IP`, Port = `8080`. Save.
- **iOS:** Settings → Wi-Fi → tap the `i` next to your network → HTTP Proxy → Manual → Server = `PC_IP`, Port = `8080`. Save.

---

## 4) Install mitmproxy certificate on the phone (HTTPS)
On the phone, open a browser and go to:

```
http://mitm.it
```

Choose your platform (Android or iOS) and follow the install instructions:

- **Android:** Download and install the certificate (Settings → Security → Install from storage). On newer Android versions you may need to install as a user certificate; some apps may ignore user certs.
- **iOS:** Tap the iOS certificate, install the profile, then go to Settings → General → VPN & Device Management (or Profiles & Device Management) and **Trust** the installed profile.

If mitm.it does not load, recheck the proxy settings and that mitmweb is running.

---

## 5) Capture the Bike Race request and copy USERID + token
1. On the phone, open Bike Race and enter or open a tourney so the app makes a request.  
2. On the PC, open mitmweb’s UI (usually `http://127.0.0.1:8081`) and inspect the captured requests.  
3. Find the request with a URL containing:
   ```
   https://api.tournaments.kube-prod-us.us-east-1.general.prod.wildlife.io/players/
   ```
4. Click that request in the list:
   - **USERID**: copy the value from the URL path after `/players/` (this is the user id).  
   - **token**: look under **Request Headers** or **Request Body** for a header named `Token`, `Authorization`, or similar. Copy the token string (it will be a long alphanumeric value). The token might also appear under other header names — inspect headers and JSON bodies.

Store the `USERID` and `token` securely (do not share them).

---

## 6) Turn off the proxy on the phone
After you have noted the `USERID` and `token`, disable the Wi-Fi proxy on the phone (set proxy back to None / Automatic). You no longer need mitmproxy.

---

## 7) Run `InfGas.exe` and paste the credentials
On the PC, open a terminal and run the executable from the folder where it is saved:

- **Windows Command Prompt:**
  ```cmd
  cd C:\path\to\folder
  InfGas.exe
  ```

- **Linux / macOS (if applicable):**
  ```bash
  ./InfGas
  ```

When prompted:
```
Paste your ID Here:
Paste your Token Here:
```
Paste the `USERID` and `token` you copied.

If the script prints `Added Gas` or similar messages, it is working. The infinite gas effect continues only while the script runs.

---

## Troubleshooting
- **No requests in mitmweb:** confirm phone and PC are on the same Wi-Fi, proxy set correctly to `PC_IP:8080`, mitmweb running, and firewall allowed.
- **mitm.it won’t load on phone:** check proxy settings and that mitmweb is reachable.
- **No token found:** inspect both request headers and request body (JSON). The token could be in a header like `Token`, `Authorization`, or `X-Oauth-User`, or in the JSON body.
- **App doesn’t show requests (certificate pinning):** some apps use certificate pinning and cannot be intercepted with mitmproxy.
- **InfGas.exe fails to start on Windows:** you may need the Microsoft Visual C++ Redistributable on some systems—test on a clean VM to confirm.

---

## Security & ethical notes
- Treat tokens like passwords. Do **not** share them publicly.  
- This procedure is only for your closed/test environment and servers you own or are authorized to test.  
- Intercepting or tampering with traffic for services you do not control is unethical and often illegal.

---

## Quick checklist (one-page)
1. Install mitmproxy on PC.  
2. Find `PC_IP` (PC local IPv4).  
3. Run `mitmweb --listen-host 0.0.0.0 --listen-port 8080`.  
4. Set phone Wi-Fi proxy to `PC_IP:8080`.  
5. On phone go to `http://mitm.it` and install/trust the certificate.  
6. Open Bike Race and a tourney.  
7. In mitmweb find request to `.../players/[USERID]` and copy `USERID` + `token`.  
8. Turn phone proxy off.  
9. Run `InfGas.exe`, paste `USERID` and `token`.  
10. Enjoy — script runs while active.

---

If you want a shorter printable checklist or a version with step-by-step screenshots, tell me what platform (Windows/macOS/Linux) you want screenshots for and I’ll add them.


---

## Distribution & Quick Start (recommended files to include)

To make this easy for recipients, include only the necessary runtime files below. **Do not** include files that contain captured tokens, saved credentials, or build artifacts.

**Keep these files (recommended package):**
- `InfGas_streamlined.exe` — the main executable (already compiled with PyInstaller).  
- `extract_tokens.py` — mitmproxy addon for automatic credential capture (optional; only if you want auto-capture).  
- `run_all.bat` — one-click launcher: starts mitmweb (if installed) and runs the EXE (use this the first time).  
- `run_infgas.bat` — simple launcher for everyday use (use this on future runs).  
- `README.md` (this file) — usage instructions and safety notes.  
- `LICENSE` (optional) — license you choose for the repo.

**Remove / do not distribute these files:**
- `extracted_tokens.txt` — contains captured USERID/token. **Delete before distribution.**  
- `credentials.json` — contains saved credentials. **Do not distribute**; create it locally on recipient machines only.  
- `dist/`, `build/`, `__pycache__/`, `*.spec` — build folders and spec files (not needed for users).  
- `InfGas_streamlined.py` (optional) — you can include source if you want transparency, but not required for runtime distribution.

### Quick Start for recipients (one-click)
1. **First time only:** Double-click `run_all.bat`.  
   - If `mitmproxy`/`mitmweb` is installed and on PATH, this will open mitmweb and the InfGas console.  
   - Follow the README's mitmproxy steps to set phone proxy and install the certificate (`http://mitm.it`) if you want auto-capture.  
2. **Everyday use:** After initial setup and saving credentials, double-click `run_infgas.bat` to launch the InfGas console directly.  
3. **Security:** After you capture credentials once and save them, delete `extracted_tokens.txt` to avoid leaving tokens on disk.

---

