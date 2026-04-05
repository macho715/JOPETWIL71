@echo off
setlocal

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\bootstrap-and-start.ps1"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo JPT71 dashboard start failed.
  echo Read the message above, then fix it and run this file again.
  pause
)

exit /b %EXIT_CODE%
