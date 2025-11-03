#!/bin/bash
# Mozart R2D2 V5 - Quick Setup and Launch Script
# Handles model download, dependencies, and app launch

set -e

echo "🚀 Mozart R2D2 V5 - DeepSeek Coder Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="$PROJECT_DIR/models/deepseek-coder-1.3b-instruct"
VENV_DIR="$PROJECT_DIR/.venv"

# Functions
log_step() {
    echo -e "${BLUE}[*]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found. Please install Python 3.10+"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    log_success "Python $PYTHON_VERSION found"
}

check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        log_step "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        log_success "Virtual environment created"
    else
        log_success "Virtual environment exists"
    fi
}

activate_venv() {
    log_step "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    log_success "Virtual environment activated"
}

install_requirements() {
    log_step "Installing dependencies..."
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt"
    log_success "Dependencies installed"
}

download_model() {
    if [ -d "$MODEL_DIR" ] && [ -f "$MODEL_DIR/config.json" ]; then
        log_success "Model already downloaded"
        return
    fi
    
    log_step "Downloading DeepSeek Coder model (1.3B)..."
    log_warning "This may take a few minutes (~2.6GB)"
    
    huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct \
        --local-dir "$MODEL_DIR"
    
    if [ $? -eq 0 ]; then
        log_success "Model downloaded successfully"
    else
        log_error "Failed to download model"
        exit 1
    fi
}

check_gpu() {
    log_step "Checking GPU availability..."
    python3 -c "import torch; print('GPU available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')" || log_warning "Could not check GPU (PyTorch may not be installed)"
}

launch_app() {
    local interface=$1
    
    case $interface in
        chat)
            log_step "Launching Modern Chat Interface..."
            python3 "$PROJECT_DIR/chat_app.py"
            ;;
        simple)
            log_step "Launching Simple Text Interface..."
            python3 "$PROJECT_DIR/app.py"
            ;;
        gui)
            log_step "Launching GUI Launcher..."
            python3 "$PROJECT_DIR/launcher.py"
            ;;
        *)
            log_error "Unknown interface: $interface"
            exit 1
            ;;
    esac
}

# Main script
main() {
    echo ""
    log_step "Starting setup..."
    
    check_python
    check_venv
    activate_venv
    install_requirements
    download_model
    check_gpu
    
    echo ""
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
    echo "Choose interface to launch:"
    echo "  1) gui       - GUI Launcher (recommended)"
    echo "  2) chat      - Modern Chat Interface"
    echo "  3) simple    - Simple Text Interface"
    echo ""
    
    if [ $# -eq 0 ]; then
        read -p "Enter choice (1-3): " choice
    else
        choice=$1
    fi
    
    case $choice in
        1|gui)
            launch_app "gui"
            ;;
        2|chat)
            launch_app "chat"
            ;;
        3|simple)
            launch_app "simple"
            ;;
        *)
            log_error "Invalid choice"
            exit 1
            ;;
    esac
}

main "$@"
