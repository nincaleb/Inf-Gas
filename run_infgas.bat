@echo off
REM Simple launcher: opens a console and runs InfGas_streamlined.exe (keeps window open)
set "EXE=InfGas_streamlined.exe"
if exist "%~dp0%EXE%" (
  start "InfGas" cmd /k "%~dp0%EXE%"
) else (
  echo ERROR: %EXE% not found in the current folder: %~dp0
  pause
)
