#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.12+ is required. Install it first."
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "WARNING: Git not found. Install Git before publishing this project."
fi

if ! command -v ollama >/dev/null 2>&1; then
  case "$(uname -s)" in
    Darwin)
      if command -v brew >/dev/null 2>&1; then
        brew install --cask ollama || true
      else
        echo "Install Ollama from https://ollama.com/download and rerun agent-economy doctor."
      fi
      ;;
    Linux)
      echo "Install Ollama with: curl -fsSL https://ollama.com/install.sh | sh"
      ;;
    *)
      echo "Install Ollama from https://ollama.com/download"
      ;;
  esac
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"

if [ ! -f config.yaml ]; then
  cp config.example.yaml config.yaml
fi

agent-economy setup
agent-economy doctor

if command -v ollama >/dev/null 2>&1; then
  ollama list >/dev/null 2>&1 || true
  ollama pull qwen2.5:7b || ollama pull llama3.2:3b || true
fi

echo "Ready. Run: . .venv/bin/activate && agent-economy demo"
