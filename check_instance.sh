#!/bin/bash
# Mozart_R2D2_V5 - Instance Status Checker
# Run this on the instance to see what's already set up

echo "============================================"
echo "🔍 Mozart_R2D2_V5 - Instance Status Check"
echo "============================================"
echo ""

# Check 1: Current directory
echo "📍 Current Location:"
pwd
echo ""

# Check 2: Project directory
echo "📂 Project Directory:"
if [ -d "Mozart_R2D2_V5" ]; then
    echo "✅ Mozart_R2D2_V5 directory EXISTS"
    cd Mozart_R2D2_V5
    echo "   Location: $(pwd)"
    echo "   Git status:"
    git status --short || echo "   (Not a git repo)"
    echo "   Last commit:"
    git log -1 --oneline 2>/dev/null || echo "   (No commits)"
    cd ..
else
    echo "❌ Mozart_R2D2_V5 directory NOT FOUND"
fi
echo ""

# Check 3: Virtual environment
echo "🐍 Virtual Environment:"
if [ -d "Mozart_R2D2_V5/.venv" ]; then
    echo "✅ .venv EXISTS in Mozart_R2D2_V5/"
    echo "   Size: $(du -sh Mozart_R2D2_V5/.venv 2>/dev/null | cut -f1)"
else
    echo "❌ .venv NOT FOUND"
fi
echo ""

# Check 4: Python
echo "🐍 Python:"
which python3 && python3 --version || echo "❌ python3 not found"
which python && python --version || echo "❌ python not found"
echo ""

# Check 5: Model files
echo "🤖 DeepSeek Coder Model:"
MODEL_DIR="Mozart_R2D2_V5/models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct"
if [ -d "$MODEL_DIR" ]; then
    FILE_COUNT=$(ls -1 "$MODEL_DIR" 2>/dev/null | wc -l)
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo "✅ Model EXISTS at $MODEL_DIR"
        echo "   Files: $FILE_COUNT"
        echo "   Size: $(du -sh "$MODEL_DIR" 2>/dev/null | cut -f1)"
        echo "   Contents:"
        ls -lh "$MODEL_DIR" | head -10
    else
        echo "⚠️  Model directory exists but is EMPTY"
    fi
else
    echo "❌ Model NOT FOUND at $MODEL_DIR"
fi
echo ""

# Check 6: GPU/CUDA
echo "🎮 GPU & CUDA:"
if command -v nvidia-smi &> /dev/null; then
    echo "✅ nvidia-smi found"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    echo "❌ nvidia-smi not found"
fi
echo ""

# Check 7: Dependencies
echo "📦 Key Dependencies:"
if [ -d "Mozart_R2D2_V5/.venv" ]; then
    source Mozart_R2D2_V5/.venv/bin/activate 2>/dev/null
    pip list 2>/dev/null | grep -E "torch|gradio|transformers|accelerate" || echo "❌ Dependencies not installed"
    deactivate 2>/dev/null
else
    echo "⚠️  Can't check - no .venv"
fi
echo ""

# Summary
echo "============================================"
echo "📊 SUMMARY"
echo "============================================"
PROJECT_OK="❌"
VENV_OK="❌"
MODEL_OK="❌"
GPU_OK="❌"

[ -d "Mozart_R2D2_V5" ] && PROJECT_OK="✅"
[ -d "Mozart_R2D2_V5/.venv" ] && VENV_OK="✅"
[ -d "$MODEL_DIR" ] && [ "$(ls -A "$MODEL_DIR" 2>/dev/null)" ] && MODEL_OK="✅"
command -v nvidia-smi &> /dev/null && GPU_OK="✅"

echo "$PROJECT_OK Project Repository"
echo "$VENV_OK Virtual Environment"
echo "$MODEL_OK Model Files"
echo "$GPU_OK GPU/CUDA"
echo ""

# Recommendations
echo "💡 RECOMMENDATIONS:"
if [ "$PROJECT_OK" = "❌" ]; then
    echo "   - Clone the repository first"
fi
if [ "$VENV_OK" = "❌" ]; then
    echo "   - Create virtual environment"
fi
if [ "$MODEL_OK" = "❌" ]; then
    echo "   - Download model files (~5GB, 5-10 min)"
fi
if [ "$GPU_OK" = "❌" ]; then
    echo "   - Check GPU drivers/CUDA installation"
fi

if [ "$PROJECT_OK" = "✅" ] && [ "$VENV_OK" = "✅" ] && [ "$MODEL_OK" = "✅" ]; then
    echo "   🎉 Everything looks ready! Just activate venv and run app.py"
fi
echo ""
echo "============================================"

