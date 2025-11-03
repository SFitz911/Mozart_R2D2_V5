#!/bin/bash
# DeepSeek Coder Remote Setup Script for CUDA 12.9 (RTX 5090)
# This script will:
# 1. Uninstall existing torch/torchvision/torchaudio and gradio
# 2. Install CUDA 12.1 PyTorch (works for CUDA 12.9)
# 3. Install compatible Gradio version
# 4. Install all requirements from requirements.txt
# 5. Verify CUDA and Gradio installation

set -e

# 1. Uninstall existing packages
echo "Uninstalling existing torch, torchvision, torchaudio, and gradio..."
pip uninstall -y torch torchvision torchaudio gradio || true

# 2. Install CUDA 12.1 PyTorch (compatible with CUDA 12.9)
echo "Installing PyTorch (CUDA 12.1 wheel, works for CUDA 12.9)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. Install compatible Gradio version
echo "Installing Gradio 3.41.2..."
pip install gradio==3.41.2

# 4. Install all requirements
echo "Installing requirements.txt..."
pip install -r requirements.txt

# 5. Verify CUDA and Gradio installation
echo "Verifying CUDA availability in torch:"
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
echo "Verifying Gradio version:"
python -c "import gradio; print('Gradio version:', gradio.__version__)"

echo "\nAll done! You are ready to launch DeepSeek Coder."
