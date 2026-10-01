$ErrorActionPreference = "Stop"

$REPO = "https://github.com/koditra/bodhiScript.git"
$DIR = "$env:USERPROFILE\.bodhiscript"

Write-Host "Installing BodhiScript..."
Write-Host ""

function Find-Git {
    $git = Get-Command git.exe -ErrorAction SilentlyContinue

    if ($git) {
        return $git.Source
    }

    $paths = @(
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles\Git\bin\git.exe",
        "${env:ProgramFiles(x86)}\Git\cmd\git.exe",
        "${env:ProgramFiles(x86)}\Git\bin\git.exe",
        "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe",
        "$env:LOCALAPPDATA\Programs\Git\bin\git.exe"
    )

    foreach ($path in $paths) {
        if (Test-Path $path) {
            return $path
        }
    }

    return $null
}

function Find-Python {
    $py = Get-Command py.exe -ErrorAction SilentlyContinue

    if ($py) {
        return $py.Source
    }

    $python = Get-Command python.exe -ErrorAction SilentlyContinue

    if ($python) {
        return $python.Source
    }

    $paths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe"
    )

    foreach ($path in $paths) {
        if (Test-Path $path) {
            return $path
        }
    }

    return $null
}

$GIT = Find-Git

if (-not $GIT) {
    Write-Host "Git not found."
    Write-Host "Installing Git..."

    if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
        Write-Host "winget is not available."
        Write-Host "Please install Git manually."
        exit 1
    }

    winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements

    $GIT = Find-Git
}

if (-not $GIT) {
    Write-Host ""
    Write-Host "Git was installed, but its executable could not be found."
    Write-Host "Please restart PowerShell and run the installer again."
    exit 1
}

Write-Host "Using Git: $GIT"

$PYTHON = Find-Python

if (-not $PYTHON) {
    Write-Host "Python not found."
    Write-Host "Installing Python..."

    if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
        Write-Host "winget is not available."
        Write-Host "Please install Python 3 manually."
        exit 1
    }

    winget install --id Python.Python.3 -e --source winget --accept-source-agreements --accept-package-agreements

    $PYTHON = Find-Python
}

if (-not $PYTHON) {
    Write-Host ""
    Write-Host "Python was installed, but its executable could not be found."
    Write-Host "Please restart PowerShell and run the installer again."
    exit 1
}

Write-Host "Using Python: $PYTHON"

if (Test-Path $DIR) {
    Write-Host "Removing previous BodhiScript installation..."
    Remove-Item -Recurse -Force $DIR
}

Write-Host "Downloading BodhiScript..."

& $GIT clone -q $REPO $DIR

Write-Host "Installing BodhiScript..."

& $PYTHON -m pip install -q -e $DIR

Write-Host ""
Write-Host "BodhiScript installed!"
Write-Host ""
Write-Host "Run:"
Write-Host "  bodhi your_file.bodhi"