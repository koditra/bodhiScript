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

    $command = Get-Command git.exe -ErrorAction SilentlyContinue

    if ($command) {
        return $command.Source
    }

    return $null
}

function Find-Python {
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

    foreach ($path in $paths) {
        if (Test-Path $path) {
            try {
                $version = & $path --version 2>&1

                if ($LASTEXITCODE -eq 0 -and $version -match "Python") {
                    return $path
                }
            } catch {
            }
        }
    }

    $py = Get-Command py.exe -ErrorAction SilentlyContinue

    if ($py -and $py.Source -notlike "*WindowsApps*") {
        try {
            & $py.Source --version 2>&1

            if ($LASTEXITCODE -eq 0) {
                return $py.Source
            }
        } catch {
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

    winget install --id Python.Python.3.14 -e --source winget `
        --accept-source-agreements `
        --accept-package-agreements

    $PYTHON = Find-Python
}

if (-not $PYTHON) {
    Write-Host ""
    Write-Host "Python was installed, but the installer could not find python.exe."
    Write-Host ""
    Write-Host "Please restart PowerShell and run the installer again."
    exit 1
}

Write-Host "Using Python: $PYTHON"

Write-Host "Checking pip..."

& $PYTHON -m pip --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing pip..."
    & $PYTHON -m ensurepip --upgrade
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

if (Test-Path $ScriptsDirectory) {
    $env:Path = "$ScriptsDirectory;$env:Path"
}

$BODHI = Join-Path $ScriptsDirectory "bodhi.exe"

if (-not (Test-Path $BODHI)) {
    $BODHI = Join-Path $ScriptsDirectory "bodhi-script.exe"
}

if (-not (Test-Path $BODHI)) {
    Write-Host ""
    Write-Host "BodhiScript installed, but bodhi.exe was not found."
    Write-Host "Python location: $PYTHON"
    Write-Host "Scripts location: $ScriptsDirectory"
    exit 1
}

Write-Host ""
Write-Host "BodhiScript installed!"
Write-Host ""
Write-Host "Run:"
Write-Host "  bodhi your_file.bodhi"
Write-Host ""
Write-Host "BodhiScript location:"
Write-Host "  $BODHI"