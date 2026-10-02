$ErrorActionPreference = "Stop"

$REPO = "https://github.com/koditra/bodhiScript.git"
$DIR = "$env:USERPROFILE\.bodhiscript"

Write-Host "Installing BodhiScript..."
Write-Host ""

function Find-Git {
    $paths = @(
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles\Git\bin\git.exe",
        "${env:ProgramFiles(x86)}\Git\cmd\git.exe",
        "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe"
    )

    foreach ($path in $paths) {
        if (Test-Path $path) {
            return $path
        }
    }

    $gitCmd = Get-Command git -ErrorAction SilentlyContinue
    if ($gitCmd) {
        return $gitCmd.Source
    }

    return $null
}

function Find-Python {
    $candidates = @()

    $pyCmd = Get-Command py -ErrorAction SilentlyContinue
    if ($pyCmd) {
        $candidates += $pyCmd.Source
    }

    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $candidates += $pythonCmd.Source
    }

    $paths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python314\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe"
    )

    foreach ($path in $paths + $candidates) {
        if (-not $path) { continue }

        try {
            $output = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $output -match "^Python 3") {
                return $path
            }
        }
        catch {
        }
    }

    return $null
}

$GIT = Find-Git

if (-not $GIT) {
    Write-Host "Git not found."
    Write-Host "Installing Git..."

    winget install --id Git.Git -e --source winget `
        --accept-source-agreements `
        --accept-package-agreements

    $GIT = Find-Git
}

if (-not $GIT) {
    Write-Host "Git installation failed."
    exit 1
}

Write-Host "Using Git: $GIT"

$PYTHON = Find-Python

if (-not $PYTHON) {
    Write-Host "Python not found."
    Write-Host "Installing Python..."

    winget install --id Python.Python.3 -e --source winget `
        --accept-source-agreements `
        --accept-package-agreements

    $PYTHON = Find-Python
}

if (-not $PYTHON) {
    Write-Host ""
    Write-Host "Python could not be found after installation."
    Write-Host "Please restart PowerShell and run the installer again."
    exit 1
}

Write-Host "Using Python: $PYTHON"

Write-Host "Checking Python..."

& $PYTHON --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not working."
    exit 1
}

Write-Host "Checking pip..."

& $PYTHON -m pip --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "pip not found. Installing pip..."
    & $PYTHON -m ensurepip --upgrade
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install pip."
    exit 1
}

if (Test-Path $DIR) {
    Write-Host "Removing previous BodhiScript installation..."
    Remove-Item -Recurse -Force $DIR
}

Write-Host "Downloading BodhiScript..."

& $GIT clone -q $REPO $DIR

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to download BodhiScript."
    exit 1
}

Write-Host "Installing BodhiScript..."

& $PYTHON -m pip install -q -e $DIR

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install BodhiScript."
    exit 1
}

$PythonDirectory = Split-Path $PYTHON
$ScriptsDirectory = Join-Path $PythonDirectory "Scripts"

if (-not (Test-Path $ScriptsDirectory)) {
    Write-Host "Python Scripts directory not found."
    exit 1
}

$env:Path = "$ScriptsDirectory;$env:Path"

$BODHI = Join-Path $ScriptsDirectory "bodhi.exe"
if (-not (Test-Path $BODHI)) {
    $BODHI = Join-Path $ScriptsDirectory "bodhi-script.exe"
}
if (-not (Test-Path $BODHI)) {
    $BODHI = Join-Path $ScriptsDirectory "bodhi-script.py"
}

if (-not (Test-Path $BODHI)) {
    Write-Host "bodhi launcher was not created."
    Write-Host "Please check the Python install and try again."
    exit 1
}

Write-Host ""
Write-Host "BodhiScript installed!"
Write-Host ""
Write-Host "Run:"
Write-Host "  bodhi your_file.bodhi"
Write-Host ""
Write-Host "Location:"
Write-Host "  $BODHI"