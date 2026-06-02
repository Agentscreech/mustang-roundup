$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

function Find-Python {
    $candidates = @(
        @{ Exe = "py"; Args = @("-3.12") },
        @{ Exe = "py"; Args = @("-3") },
        @{ Exe = "python"; Args = @() }
    )

    foreach ($candidate in $candidates) {
        try {
            & $candidate.Exe @($candidate.Args + @("--version")) *> $null
            if ($LASTEXITCODE -eq 0) {
                return $candidate
            }
        } catch {
        }
    }

    throw "Python was not found. Install Python 3.12 from https://www.python.org/downloads/ and check 'Add python.exe to PATH'."
}

function ConvertFrom-SecureStringPlainText {
    param([Security.SecureString] $SecureString)
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

$python = Find-Python
$env:MUSTANGROUNDUP_LOCAL_EVENT_MODE = "1"
$env:DJANGO_DEBUG = "1"

if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    Write-Host "Creating local Python environment..."
    & $python.Exe @($python.Args + @("-m", "venv", ".venv"))
}

Write-Host "Installing app requirements..."
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "Preparing the local event database..."
& ".\.venv\Scripts\python.exe" manage.py migrate

$adminUser = Read-Host "Admin username [admin]"
if ([string]::IsNullOrWhiteSpace($adminUser)) {
    $adminUser = "admin"
}

do {
    $passwordOne = ConvertFrom-SecureStringPlainText (Read-Host "Admin password, 8+ characters" -AsSecureString)
    $passwordTwo = ConvertFrom-SecureStringPlainText (Read-Host "Type the admin password again" -AsSecureString)
    if ($passwordOne.Length -lt 8) {
        Write-Host "Password must be at least 8 characters."
        $passwordsMatch = $false
    } elseif ($passwordOne -ne $passwordTwo) {
        Write-Host "Passwords did not match."
        $passwordsMatch = $false
    } else {
        $passwordsMatch = $true
    }
} until ($passwordsMatch)

& ".\.venv\Scripts\python.exe" manage.py ensure_admin --username $adminUser --password $passwordOne

Write-Host ""
Write-Host "Setup complete."
Write-Host "Start the app with: .\scripts\start-server.ps1"
