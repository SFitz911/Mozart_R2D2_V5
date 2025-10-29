# PowerShell script to launch Mozart_R2D2_V5 DeepSeek app
$venvPath = "./.venv"

# Create venv if it doesn't exist
if (-Not (Test-Path $venvPath)) {
    python -m venv .venv
}

# Activate venv
$env:VIRTUAL_ENV = (Resolve-Path .venv).Path
$env:PATH = "$env:VIRTUAL_ENV\Scripts;" + $env:PATH

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Kill any process on port 8080
$port = 8080
$netstat = netstat -ano | Select-String ":$port"
foreach ($line in $netstat) {
    $pid = ($line -split '\s+')[-1]
    if ($pid -match '\d+') {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
}

# Start the app in background
Start-Process -NoNewWindow -FilePath python -ArgumentList "app.py" -RedirectStandardOutput "./server.out.log" -RedirectStandardError "./server.err.log"

Start-Sleep -Seconds 5

# Print Gradio link from log
Get-Content ./server.out.log -Tail 50 | Select-String "http"