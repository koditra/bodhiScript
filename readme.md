# bodhiScript

bodhiScript is a small programming language inspired by **hindi and sanskrit**. It uses a **java like syntax** (bc I code with java) with `{}`, `()`, and `;` while using hindi/sanskrit-inspired keywords.

The goal is to make programming feel familiar to people who know Hindi or Sanskrit while keeping the syntax easy to learn.

## Setup

bodhiScript has installers for macOS/Linux and Windows.

### macOS / Linux

Run:

```bash
curl -fsSL https://raw.githubusercontent.com/koditra/bodhiScript/main/install.sh | bash
```

The installer checks for Python and Git and only installs them if they are missing.

You can also install manually:

```bash
git clone https://github.com/koditra/bodhiScript.git
cd bodhiScript
python3 -m pip install -e .
```

### Windows

Open PowerShell and run:

```powershell
iwr https://raw.githubusercontent.com/koditra/bodhiScript/main/install.ps1 -UseBasicParsing | iex
```

The Windows installer checks for Python and Git and installs them with `winget` if they are missing.

## Running BodhiScript

After installation, run a `.bodhi` file with:

```bash
bodhi hello.bodhi
```

BodhiScript can also search through folders for the file, so you can run a file by its name without always being in the same directory.

## Browser Terminal

You can also run BodhiScript in a tiny browser-based terminal:

```bash
cd bodhiScript
python3 web.py
```

Then open:

```text
http://localhost:8000
```

The browser editor includes:

- Tab inserts 4 spaces
- pressing Enter inside `{}` adds indentation automatically
- typing `(`, `{`, `[`, and `"` inserts matching pairs
- Ctrl/Cmd + Enter runs the script
- smart block editing for quick testing

## Hello World

```text
likha("Hello, World!");
```

## Variables

Use `maan` or `rakho` to create variables.

```text
maan naam = "Aashvik";
rakho age = 14;

likha(naam);
likha(age);
```

## Conditions

BodhiScript supports `yadi` and `agar` for conditions, and `anyatha` and `warna` for `else`.

```text
maan age = 14;

yadi age >= 13 {
    likha("Teenager");
} anyatha {
    likha("Not a teenager");
}
```

## Loops

BodhiScript supports loops with `jabtak` and `yavyat`.

```text
maan i = 0;

jabtak i < 3 {
    likha(i);
    i = i + 1;
}

yavyat i < 5 {
    likha("still going");
    i = i + 1;
}
```

## Functions

Functions use the `karya` keyword.

```text
karya greet() {
    likha("Namaste!");
}

greet();
```

Functions can also return values with `wapas`.

```text
karya add(a, b) {
    wapas a + b;
}

maan result = add(5, 3);
likha(result);
```

## Keywords

| Keyword | Meaning |
|---|---|
| `maan` | variable |
| `rakho` | variable |
| `likha` | print |
| `yadi` | if |
| `agar` | if |
| `anyatha` | else |
| `warna` | else |
| `satya` | true |
| `asatya` | false |
| `shunya` | none |
| `aur` | and |
| `ya` | or |
| `nahi` | not |
| `wapas` | return |
| `karya` | function |
| `jabtak` | while loop |
| `yavyat` | while loop |

## Syntax

BodhiScript uses semicolons to end normal statements:

```text
maan x = 10;
likha(x);
```

Blocks use curly braces:

```text
yadi x > 5 {
    likha("x is bigger");
}
```

## Current Implementation

BodhiScript currently works as an interpreter that translates BodhiScript code into Python and executes it.

It also includes:

- an installer that checks for and installs dependancies
- a browser playground for quick testing in the browser
- a minimal editor workflow with smart indentation and bracket completion

The current goal is to eventually move beyond this and build a compiler for BodhiScript itself! This could be rlly cool i think.