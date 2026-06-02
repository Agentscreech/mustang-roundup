$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    throw "The local Python environment was not found. Run .\scripts\setup-windows.ps1 first."
}

$port = if ($env:PORT) { $env:PORT } else { "8000" }
$env:MUSTANGROUNDUP_LOCAL_EVENT_MODE = "1"
$env:DJANGO_DEBUG = "1"

Write-Host ""
Write-Host "Mustang Roundup is starting."
Write-Host "Keep this window open while the show is running."
Write-Host ""
Write-Host "Operator dashboard on this computer:"
Write-Host "  http://127.0.0.1:$port/"
Write-Host "Admin setup:"
Write-Host "  http://127.0.0.1:$port/admin/"
Write-Host ""
Write-Host "Judge links for phones on the same Wi-Fi:"

$addresses = @()
try {
    $addresses = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object {
            $_.IPAddress -ne "127.0.0.1" -and
            $_.IPAddress -notlike "169.254.*" -and
            $_.PrefixOrigin -ne "WellKnown"
        } |
        Select-Object -ExpandProperty IPAddress -Unique
} catch {
}

if ($addresses.Count -eq 0) {
    Write-Host "  No local network address was detected yet."
    Write-Host "  Connect this computer to the event Wi-Fi, then restart this script."
} else {
    foreach ($address in $addresses) {
        Write-Host "  http://$address`:$port/judge/login/"
    }
}

Write-Host ""
Write-Host "Press Ctrl+C to stop the server after the event."
Write-Host ""

& ".\.venv\Scripts\python.exe" manage.py runserver "0.0.0.0:$port" --noreload
