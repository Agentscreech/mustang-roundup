$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$env:MUSTANGROUNDUP_LOCAL_EVENT_MODE = "1"
$env:DJANGO_DEBUG = "1"

& ".\.venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000 --noreload
