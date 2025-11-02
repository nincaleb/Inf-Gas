@echo off
REM One-click launcher for InfGas + mitmproxy.
REM Place this file in the same folder as InfGas_streamlined.exe and extract_tokens.py.
REM It will open mitmweb (if mitmweb is in PATH) in a new window and then open the InfGas exe in another window.

setlocal
set "MITM_SCRIPT=extract_tokens.py"
set "EXE=InfGas_streamlined.exe"

REM Check for mitmweb
where mitmweb >nul 2>&1
if %errorlevel%==0 (
  echo Starting mitmweb with addon "%MITM_SCRIPT%"...
  start "mitmweb" cmd /k "mitmweb -s \"%~dp0%MITM_SCRIPT%\" --listen-host 0.0.0.0 --listen-port 8080"
) else (
  echo WARNING: mitmweb not found in PATH.
  echo If you want the launcher to start mitmweb automatically, install mitmproxy and make sure "mitmweb" is on your PATH.
  echo You can still run InfGas only; press any key to continue.
  pause >nul
)

REM Give mitmweb a few seconds to start (adjust if needed)
timeout /t 3 >nul

REM Start InfGas exe
if exist "%~dp0%EXE%" (
  echo Launching %EXE%...
  start "InfGas" cmd /k "%~dp0%EXE%"
) else (
  echo ERROR: %EXE% not found in the current folder: %~dp0
  echo Place %EXE% in the same folder as this launcher.
  pause
)
endlocal
