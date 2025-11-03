#!/bin/bash
# Mozart R2D2 V5 - ONE-COMMAND STARTUP
# Just run: ./start.sh

set -e

echo "=========================================="
echo "🎵 Mozart R2D2 - Starting Up..."
echo "=========================================="
echo ""

# Go to workspace
cd /workspace/Mozart_R2D2_V5

# Update code
echo "📥 Updating code..."
git pull || true
echo ""

# Link model if not already linked
MODEL_DIR="models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct"
if [ ! -L "$MODEL_DIR" ]; then
    echo "🔗 Linking model..."
    mkdir -p models/DeepSeek-Coder-1.3b-instruct
    ln -sf /workspace/models/deepseek-coder-1.3b-instruct "$MODEL_DIR"
    echo "✅ Model linked"
else
    echo "✅ Model already linked"
fi
echo ""

# Install/update dependencies (quiet mode)
echo "📦 Checking dependencies..."
pip install -q gradio torch transformers accelerate 2>/dev/null || pip install gradio torch transformers accelerate
echo "✅ Dependencies ready"
echo ""

# Kill any existing instance
pkill -9 -f "python app.py" 2>/dev/null || true

# Launch
echo "=========================================="
echo "🚀 Launching Mozart R2D2..."
echo "=========================================="
echo ""
echo "💡 TIP: After launch, run './get_url.sh' to quickly find the public URL"
echo ""
python app.py

