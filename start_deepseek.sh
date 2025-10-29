#!/bin/bash
# Activate your environment (edit this line if you use conda)
source /workspace/venv/main/bin/activate

# Install all dependencies
pip install -r /workspace/Mozart_R2D2/requirements.txt

# Kill any process on port 8080
fuser -k 8080/tcp || true

# Start the app
nohup python /workspace/Mozart_R2D2/deploy/deepseek_source/app.py > /tmp/deepseek.log 2>&1 &

# Print the Gradio link
sleep 5
tail -n 50 /tmp/deepseek.log | grep 'http'
