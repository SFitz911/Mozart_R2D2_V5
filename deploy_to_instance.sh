#!/bin/bash
# Mozart_R2D2_V5 - Smart Remote Instance Deployment Script
# This script checks what's already set up and only does what's needed

set -e

echo "============================================"
echo "🚀 Mozart_R2D2_V5 - Smart Deployment"
echo "============================================"
echo ""

# Step 1: Clone/Update Repository
echo "[1/6] Checking repository..."
if [ ! -d "Mozart_R2D2_V5" ]; then
    echo "   📥 Cloning repository from GitHub..."
    git clone https://github.com/SFitz911/Mozart_R2D2_V5.git
    cd Mozart_R2D2_V5
    echo "   ✅ Repository cloned"
else
    echo "   ✅ Repository exists, updating..."
    cd Mozart_R2D2_V5
    git fetch
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "unknown")
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo "   ✅ Already up to date"
    else
        git pull
        echo "   ✅ Repository updated"
    fi
fi
echo ""

# Step 2: Create virtual environment
echo "[2/6] Checking virtual environment..."
if [ ! -d ".venv" ]; then
    echo "   🔨 Creating virtual environment..."
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi
echo ""

# Step 3: Activate virtual environment
echo "[3/6] Activating virtual environment..."
source .venv/bin/activate 2>/dev/null || . .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
echo "   ✅ Virtual environment activated"
echo "   🐍 Python: $(python --version)"
echo ""

# Step 4: Check and install requirements
echo "[4/6] Checking dependencies..."
DEPS_MISSING=false
python -c "import torch, gradio, transformers" 2>/dev/null || DEPS_MISSING=true

if [ "$DEPS_MISSING" = true ]; then
    echo "   📦 Installing dependencies (this may take a few minutes)..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt
    echo "   ✅ Dependencies installed"
else
    echo "   ✅ Core dependencies already installed"
    echo "   📦 Updating to latest versions..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --upgrade --quiet
    echo "   ✅ Dependencies updated"
fi
echo ""

# Step 5: Check and download model if needed
echo "[5/6] Checking DeepSeek Coder model..."
MODEL_DIR="models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct"
if [ -d "$MODEL_DIR" ] && [ "$(ls -A $MODEL_DIR 2>/dev/null | wc -l)" -gt 5 ]; then
    MODEL_SIZE=$(du -sh "$MODEL_DIR" 2>/dev/null | cut -f1)
    echo "   ✅ Model already exists ($MODEL_SIZE)"
    echo "   📁 Location: $MODEL_DIR"
    echo "   ⏭️  Skipping download"
else
    echo "   ⬇️  Downloading DeepSeek Coder model..."
    echo "   ⏳ This will take 5-10 minutes (~5GB download)"
    pip install huggingface_hub --quiet
    mkdir -p models/DeepSeek-Coder-1.3b-instruct
    huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct \
        --local-dir "$MODEL_DIR" \
        --local-dir-use-symlinks False
    echo "   ✅ Model downloaded successfully!"
fi
echo ""

# Step 6: Final checks and launch
echo "[6/6] Pre-launch checks..."
echo "   🎮 Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader)
    echo "   ✅ GPU detected: $GPU_NAME"
    python -c "import torch; print(f'   ✅ PyTorch CUDA: {torch.cuda.is_available()}')"
else
    echo "   ⚠️  No GPU detected (will use CPU - slower)"
fi
echo ""

echo "============================================"
echo "🎵 Launching Mozart_R2D2_V5..."
echo "============================================"
echo ""
echo "🌐 Starting Gradio interface..."
echo "📡 Watch for the PUBLIC URL below!"
echo ""
echo "   The URL will look like:"
echo "   https://xxxxxxxx.gradio.live"
echo ""
echo "   Open that URL in your browser to access"
echo "   your AI coding assistant from anywhere!"
echo ""
echo "============================================"
echo ""

# Run the app (it will display the Gradio public URL)
python app.py

# Note: The script will keep running while the app is active
# Press Ctrl+C to stop the server

