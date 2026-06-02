$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location -LiteralPath $repoRoot
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string] $FilePath,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        Invoke-Checked py -3 -m venv .venv
    } else {
        Invoke-Checked python -m venv .venv
    }
}

Invoke-Checked ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller
Invoke-Checked ".\.venv\Scripts\python.exe" -m PyInstaller --noconfirm "packaging\windows\MustangRoundup.spec"

$isccCandidates = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

if ($iscc) {
    Invoke-Checked $iscc "packaging\windows\MustangRoundup.iss"
    Write-Host "Installer created: dist\installer\MustangRoundup-Setup.exe"
} else {
    New-Item -ItemType Directory -Force -Path "dist\installer" | Out-Null
    Compress-Archive -Force -Path "dist\MustangRoundup\*" -DestinationPath "dist\installer\MustangRoundup-Portable.zip"
    Write-Host "Inno Setup was not found, so a portable zip was created instead:"
    Write-Host "dist\installer\MustangRoundup-Portable.zip"
    Write-Host "Install Inno Setup 6 and run this script again to create MustangRoundup-Setup.exe."
}
