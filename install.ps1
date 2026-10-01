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
    $commands = @(
        "py.exe",
        "python.exe"
    )

    foreach ($command in $commands) {
        $result = Get-Command $command -ErrorAction SilentlyContinue

        if ($result) {
            $path = $result.Source

            if ($path -notlike "*\WindowsApps\*") {
                try {
                    & $path --version 2>$null

                    if ($LASTEXITCODE -eq 0) {
                        return $path
                    }
                } catch {
                }
            }
        }
    }

    $paths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "$env:ProgramFiles\Python310\python.exe"
    )

    foreach ($path in $paths) {
        if (Test-Path $path) {
            try {
                & $path --version 2>$null

                if ($LASTEXITCODE -eq 0) {
                    return $path
                }
            } catch {
            }
        }
    }

    return $null
}

function Add-To-Current-Path {
    param (
        [string]$PathToAdd
    )

    if (-not ($env:Path -split ";" | Where-Object { $_ -eq $PathToAdd })) {
        $env:Path = "$PathToAdd;$env:Path"
    }
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
    Write-Host "Git could not be found after installation."
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
    Write-Host "Python could not be found after installation."
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

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to download BodhiScript."
    exit 1
}

Write-Host "Installing BodhiScript..."

& $PYTHON -m pip install -q -e $DIR

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Failed to install BodhiScript."
    exit 1
}

$PythonDirectory = Split-Path $PYTHON

$ScriptsDirectory = Join-Path $PythonDirectory "Scripts"

if (Test-Path $ScriptsDirectory) {
    Add-To-Current-Path $ScriptsDirectory
}

$Bodhi = Get-Command bodhi.exe -ErrorAction SilentlyContinue

if (-not $Bodhi) {
    $PossibleBodhiPaths = @(
        "$ScriptsDirectory\bodhi.exe",
        "$env:APPDATA\Python\Python313\Scripts\bodhi.exe",
        "$env:APPDATA\Python\Python312\Scripts\bodhi.exe",
        "$env:APPDATA\Python\Python311\Scripts\bodhi.exe"
    )

    foreach ($path in $PossibleBodhiPaths) {
        if (Test-Path $path) {
            $Bodhi = $path
            Add-To-Current-Path (Split-Path $path)
            break
        }
    }
}

if (-not $Bodhi) {
    Write-Host ""
    Write-Host "BodhiScript was installed, but the bodhi command could not be found."
    Write-Host "Try restarting PowerShell and running 'bodhi' again."
    exit 1
}

Write-Host ""
Write-Host "BodhiScript installed!"
Write-Host ""
Write-Host "Run:"
Write-Host "  bodhi your_file.bodhi"