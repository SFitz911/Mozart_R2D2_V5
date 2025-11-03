#!/bin/bash
# Mozart R2D2 V5 - Quick Deploy Script for Instance
# This shows you what's happening at each step

echo "============================================"
echo "🚀 Mozart R2D2 V5 - Instance Deployment"
echo "============================================"
echo ""

# Check current location
echo "📍 STEP 1: Checking current directory..."
pwd
echo ""

# List what's here
echo "📂 STEP 2: Listing files..."
ls -la
echo ""

# Check if project exists
if [ -d "Mozart_R2D2_V5" ]; then
    echo "✅ Found existing Mozart_R2D2_V5 directory"
    echo "📥 STEP 3: Updating from GitHub..."
    cd Mozart_R2D2_V5
    git pull
else
    echo "📥 STEP 3: Cloning from GitHub..."
    git clone https://github.com/SFitz911/Mozart_R2D2_V5.git
    cd Mozart_R2D2_V5
fi
echo ""

# Check for venv
echo "🐍 STEP 4: Checking Python environment..."
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "🔨 Creating virtual environment..."
    python3 -m venv .venv
fi
echo ""

# Activate venv
echo "⚡ STEP 5: Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Check Python and pip
echo "🔍 STEP 6: Checking Python version..."
python --version
pip --version
echo ""

# Install dependencies
echo "📦 STEP 7: Installing/Updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Check for model
echo "🤖 STEP 8: Checking for DeepSeek Coder model..."
MODEL_DIR="models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct"
if [ -d "$MODEL_DIR" ] && [ "$(ls -A $MODEL_DIR)" ]; then
    echo "✅ Model already exists at $MODEL_DIR"
    ls -lh "$MODEL_DIR"
else
    echo "⬇️  Downloading DeepSeek Coder model (this may take 5-10 minutes)..."
    pip install huggingface_hub
    mkdir -p models/DeepSeek-Coder-1.3b-instruct
    huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct \
        --local-dir "$MODEL_DIR" \
        --local-dir-use-symlinks False
    echo "✅ Model downloaded!"
fi
echo ""

# Check CUDA
echo "🎮 STEP 9: Checking GPU/CUDA availability..."
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" 2>/dev/null || echo "⚠️  Torch not yet installed"
echo ""

# Launch app
echo "============================================"
echo "🎵 STEP 10: Launching Mozart R2D2!"
echo "============================================"
echo ""
echo "⏳ Starting Gradio interface..."
echo "🌐 Watch for the PUBLIC URL below:"
echo "============================================"
echo ""

python app.py

