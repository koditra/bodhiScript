#!/bin/bash

set -e

REPO="https://github.com/koditra/bodhiScript.git"
DIR="$HOME/.bodhiscript"

echo "Installing BodhiScript..."

rm -rf "$DIR"
git clone -q "$REPO" "$DIR"

cd "$DIR"
python3 -m pip install -q -e .

echo "BodhiScript installed!"
echo "Run: bodhi your_file.bodhi"