$ErrorActionPreference = "Stop"

$REPO = "https://github.com/koditra/bodhiScript.git"
$DIR = "$env:USERPROFILE\.bodhiscript"

Write-Host "Installing BodhiScript..."
Write-Host ""

function Refresh-Path {
    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")

    $env:Path = "$machinePath;$userPath"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found."

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Installing Git..."
        winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements

        Refresh-Path
    } else {
        Write-Host "winget is not available."
        Write-Host "Please install Git manually."
        exit 1
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git was installed, but PowerShell could not find it."
    Write-Host "Please restart PowerShell and run the installer again."
    exit 1
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    $PYTHON = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PYTHON = "python"
} else {
    Write-Host "Python not found."

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Installing Python..."
        winget install --id Python.Python.3 -e --source winget --accept-source-agreements --accept-package-agreements

        Refresh-Path

        if (Get-Command py -ErrorAction SilentlyContinue) {
            $PYTHON = "py"
        } elseif (Get-Command python -ErrorAction SilentlyContinue) {
            $PYTHON = "python"
        } else {
            Write-Host "Python was installed, but PowerShell could not find it."
            Write-Host "Please restart PowerShell and run the installer again."
            exit 1
        }
    } else {
        Write-Host "winget is not available."
        Write-Host "Please install Python 3 manually."
        exit 1
    }
}

Write-Host "Using Python: $PYTHON"

if (Test-Path $DIR) {
    Write-Host "Removing previous BodhiScript installation..."
    Remove-Item -Recurse -Force $DIR
}

Write-Host "Downloading BodhiScript..."

git clone -q $REPO $DIR

Write-Host "Installing BodhiScript..."

& $PYTHON -m pip install -q -e $DIR

Write-Host ""
Write-Host "BodhiScript installed!"
Write-Host ""
Write-Host "Run:"
Write-Host "  bodhi your_file.bodhi"