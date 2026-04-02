@echo off
echo ==================================================
echo   Le Maison - Auto Start Server ^& Tunnel
echo ==================================================
echo.

:: Get Public IP for Tunnel Password
echo [▶] Fetching your Tunnel Password (IP)...
for /f "delims=" %%i in ('curl -s https://ipv4.icanhazip.com') do set "PUBLIC_IP=%%i"

if "%PUBLIC_IP%"=="" (
    echo [!] Warning: Could not fetch IP automatically.
    echo [!] Make sure you are connected to the internet.
) else (
    echo.
    echo --------------------------------------------------
    echo   YOUR TUNNEL PASSWORD: %PUBLIC_IP%
    echo --------------------------------------------------
    echo.
)

:: Start the Flask app in a new window
echo [▶] Starting Flask Server...
start "Flask Server" cmd /c "flask run"

:: Wait a little bit for flask to spin up
timeout /t 3 /nobreak >nul

:: Keep localtunnel alive in this window
echo [▶] Starting LocalTunnel with subdomain: le-maison-yelo...
:loop
:: Adding --local-host 127.0.0.1 helps prevent the random 503 Tunnel Unavailable errors
lt --port 5000 --local-host 127.0.0.1 --subdomain le-maison-yelo
echo.
echo [!] LocalTunnel disconnected. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
echo.
goto loop
