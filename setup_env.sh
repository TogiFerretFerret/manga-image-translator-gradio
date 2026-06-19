#!/bin/bash
# setup_env.sh - Automates installation of manga-image-translator-gradio in molab/Colab containers

echo "============================================================"
echo " Setup Manga Image Translator (Gradio Edition) in Molab"
echo "============================================================"

# 1. Create a virtual environment using Python 3.11 (safe version for all wheels)
echo "[1/5] Creating Python 3.11 virtual environment..."
uv venv --python 3.11 .venv
source .venv/bin/activate

# 2. Temporarily comment out the malformed rusty-manga-image-translator package
echo "[2/5] Preparing requirements.txt..."
sed -i 's/^rusty-manga-image-translator/# &/' requirements.txt

# 3. Use uv to install the 149 standard packages at lightning speed
echo "[3/5] Installing dependencies with uv..."
uv pip install -r requirements.txt

# 4. Use standard pip to install the malformed rusty-manga-image-translator package
echo "[4/5] Installing rusty-manga-image-translator with standard pip..."
.venv/bin/pip install --extra-index-url https://frederik-uni.github.io/manga-image-translator-rust/python/wheels/simple/ rusty-manga-image-translator

# 5. Install gradio
echo "[5/5] Installing gradio..."
uv pip install gradio

# 6. Restore requirements.txt
sed -i 's/^# \(rusty-manga-image-translator\)/\1/' requirements.txt

echo "============================================================"
echo " SETUP SUCCESSFUL!"
echo "============================================================"
echo "To start the Gradio server, run:"
echo "  PYTHONPATH= .venv/bin/python gradio_app.py"
echo "============================================================"
