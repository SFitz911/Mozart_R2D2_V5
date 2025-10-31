#!/bin/bash
# Clean, minimal DeepSeek Coder launch script
cd "$(dirname "$0")/project"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
	python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Kill any process on port 8090
fuser -k 8090/tcp || true

# Start the app
nohup python app.py > /tmp/deepseek.log 2>&1 &

# Print the Gradio link
sleep 5
tail -n 50 /tmp/deepseek.log | grep 'http'
