#!/bin/bash

set -e

REPO="https://github.com/koditra/bodhiScript.git"
DIR="$HOME/.bodhiscript"

echo "Installing BodhiScript..."

OS="$(uname -s)"

if [ "$OS" != "Darwin" ] && [ "$OS" != "Linux" ]; then
    echo "This installer only supports macOS and Linux."
    exit 1
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    echo "Python not found."

    if [ "$OS" = "Darwin" ]; then
        if ! command -v brew >/dev/null 2>&1; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi

        brew install python
        PYTHON="python3"

    elif [ "$OS" = "Linux" ]; then
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
            PYTHON="python3"

        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y python3 python3-pip
            PYTHON="python3"

        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -Sy --noconfirm python python-pip
            PYTHON="python"

        else
            echo "Could not find a supported Linux package manager."
            echo "Please install Python 3 manually."
            exit 1
        fi
    fi
fi

echo "Using Python: $PYTHON"

if command -v git >/dev/null 2>&1; then
    echo "Git found."
else
    echo "Git not found."

    if [ "$OS" = "Darwin" ]; then
        if command -v brew >/dev/null 2>&1; then
            echo "Installing Git with Homebrew..."
            brew install git
        else
            echo "Installing Git..."
            xcode-select --install
        fi

    elif [ "$OS" = "Linux" ]; then
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y git

        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y git

        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -Sy --noconfirm git

        else
            echo "Could not find a supported Linux package manager."
            echo "Please install Git manually."
            exit 1
        fi
    fi
fi

if [ -d "$DIR" ]; then
    echo "Removing previous BodhiScript installation..."
    rm -rf "$DIR"
fi

echo "Downloading BodhiScript..."

git clone -q "$REPO" "$DIR"

cd "$DIR"

echo "Installing BodhiScript..."

"$PYTHON" -m pip install -q -e .

echo ""
echo "BodhiScript installed!"
echo ""
echo "Run:"
echo "  bodhi your_file.bodhi"