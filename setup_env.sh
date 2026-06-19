#!/bin/bash
# setup_env.sh - Automates installation of manga-image-translator-gradio in molab/Colab containers

# Change directory to the script's directory to resolve relative paths correctly
cd "$(dirname "$0")"

echo "============================================================"
echo " Setup Manga Image Translator (Gradio Edition) in Molab"
echo "============================================================"

# 1. Create a virtual environment using Python 3.11 (safe version for all wheels)
echo "[1/5] Creating Python 3.11 virtual environment..."
uv venv --clear --python 3.11 .venv
source .venv/bin/activate

# 2. Temporarily comment out the malformed rusty-manga-image-translator package
echo "[2/5] Preparing requirements.txt..."
sed -i 's/^rusty-manga-image-translator/# &/' requirements.txt
echo source .venv/bin/activate
echo uv pip --python /marimo/manga-image-translator-gradio/.venv/bin/python install -r requirements.txt
echo pip --python /marimo/manga-image-translator-gradio/.venv/bin/python install --extra-index-url https://frederik-uni.github.io/manga-image-translator-rust/python/wheels/simple/ rusty-manga-image-translator
echo uv pip install --python /marimo/manga-image-translator-gradio/.venv/bin/python gradio
echo "============================================================"
echo " SETUP SUCCESSFUL!"
echo "============================================================"
echo "To start the Gradio server, run:"
echo "  PYTHONPATH= .venv/bin/python gradio_app.py"
echo "============================================================"
