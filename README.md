# 🎵 Mozart R2D2 V5 - AI Coding Assistant

**Cursor-style interface powered by DeepSeek Coder**

---

## 📑 Table of Contents

1. [Quick Start](#-quick-start) - Get running in 30 seconds
2. [Decision Tree](#-decision-tree) - Which method to use?
3. [Features](#-features) - What you get
4. [Usage Guide](#-usage-guide) - How to use the interface
5. [Project Structure](#-project-structure) - File organization
6. [Manual Setup](#-manual-setup) - Step-by-step if needed
7. [Troubleshooting](#-troubleshooting) - Common issues
8. [Commands Reference](#-commands-reference) - Quick commands

---

## ⚡ Quick Start

### On Your Instance (Fastest Method):

```bash
cd /workspace/Mozart_R2D2_V5
./start.sh
```

**That's it!** Open the public URL in your browser.

---

## 🌳 Decision Tree

```
┌─────────────────────────────────────┐
│   Are you on the instance already?  │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
       YES           NO
        │             │
        │             └──> SSH into instance:
        │                  ssh -p 18785 root@172.219.157.164
        │                  (or use Jupyter terminal)
        │                  │
        │                  └──> Continue below
        │
        ▼
┌─────────────────────────────────────┐
│  cd /workspace/Mozart_R2D2_V5       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Does start.sh exist and is         │
│  executable?                         │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
       YES           NO
        │             │
        │             └──> Run: git pull
        │                  Run: chmod +x start.sh
        │
        ▼
┌─────────────────────────────────────┐
│  Run: ./start.sh                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Watch for:                          │
│  "Running on public URL: https://..." │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Copy URL & open in browser         │
│  🎉 START CODING!                   │
└─────────────────────────────────────┘
```

---

## ✨ Features

### Chat-Based Interface
- 💬 **Conversational AI** - Ask questions naturally
- 🔄 **Context Aware** - Remembers your conversation
- 📝 **Multi-turn Dialogue** - Ask follow-up questions
- 🎨 **Cursor-Style Dark Theme** - Beautiful, modern UI

### Code Generation
- 🤖 **Optimized for Code** - Temperature: 0.2, 512 tokens
- 🎯 **High Quality** - Focused, accurate responses
- 📋 **One-Click Copy** - Copy any response instantly
- 🔍 **Syntax Highlighting** - Easy-to-read code blocks

### Smart Features
- 🚀 **8 Example Prompts** - Get started quickly
- 💡 **Tips & Guide** - Built-in help accordion
- ⚡ **Fast Startup** - One command to launch
- 🔗 **Auto Model Linking** - No manual setup needed

---

## 🎯 Usage Guide

### What You Can Ask:

**Write Code:**
- "Write a Python function to implement quicksort"
- "Create a REST API with Flask and JWT authentication"
- "Build a React todo list component with TypeScript"

**Explain Concepts:**
- "Explain how async/await works in Python with examples"
- "What's the difference between var, let, and const in JavaScript?"
- "How does database indexing improve query performance?"

**Debug & Fix:**
- "Debug this code: [paste your code]"
- "Why is this SQL query slow?"
- "Fix the memory leak in this function"

**Refactor & Improve:**
- "Refactor this function to be more efficient"
- "Add error handling to this API endpoint"
- "Make this code more readable"

**Generate Tests:**
- "Write unit tests for this authentication service"
- "Create pytest fixtures for a database connection"
- "Generate test cases for edge conditions"

### Using the Interface:

1. **Type your question** in the chat input
2. **Press Enter** or click 🚀 Send
3. **View the response** with syntax highlighting
4. **Click copy** to grab the code
5. **Ask follow-ups** - it remembers context!
6. **Clear chat** anytime with 🗑️ button

---

## 📁 Project Structure

```
Mozart_R2D2_V5/
├── app.py                 # Main application (Cursor-style chat)
├── start.sh               # ONE-COMMAND startup script ⭐
├── requirements.txt       # Python dependencies
├── remote_setup.sh        # CUDA setup helper (optional)
├── check_instance.sh      # Status checker
├── deploy_to_instance.sh  # Deployment script
├── quick_deploy.sh        # Verbose deployment
├── .gitignore            # Git ignore rules
└── models/               # Model symlinks (auto-created)
    └── DeepSeek-Coder-1.3b-instruct/
        └── deepseek-coder-1.3b-instruct/  # Symlink to /workspace/models/
```

### Key Files:

| File | Purpose |
|------|---------|
| `start.sh` | ⭐ **USE THIS** - One-command startup |
| `app.py` | Main Gradio application with chat interface |
| `requirements.txt` | gradio, torch, transformers, accelerate |
| `check_instance.sh` | Check what's installed on instance |
| `deploy_to_instance.sh` | Smart deployment with progress |
| `remote_setup.sh` | CUDA 12.x PyTorch installation helper |

---

## 🔧 Manual Setup

*Only needed if `start.sh` doesn't work or you want manual control*

### 1. Install Dependencies
```bash
pip install gradio torch transformers accelerate
```

### 2. Link Model
```bash
mkdir -p models/DeepSeek-Coder-1.3b-instruct
ln -s /workspace/models/deepseek-coder-1.3b-instruct \
      models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct
```

### 3. Launch Application
```bash
python app.py
```

### 4. Get Public URL
Watch for:
```
* Running on public URL: https://xxxxx.gradio.live
```

---

## 🔍 Troubleshooting

### App Won't Start

**Check if model exists:**
```bash
ls -la /workspace/models/deepseek-coder-1.3b-instruct/
```
Should show files like `model.safetensors`, `config.json`, etc.

**Check symlink:**
```bash
ls -la models/DeepSeek-Coder-1.3b-instruct/
```
Should show the symlinked directory.

**Recreate symlink:**
```bash
rm -rf models/DeepSeek-Coder-1.3b-instruct
mkdir -p models/DeepSeek-Coder-1.3b-instruct
ln -s /workspace/models/deepseek-coder-1.3b-instruct \
      models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct
```

### Port Already in Use

```bash
pkill -9 -f "python app.py"
./start.sh
```

### Dependencies Missing

```bash
pip install --upgrade pip
pip install gradio torch transformers accelerate
```

### GPU Not Detected

**Check CUDA:**
```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

**If False:** App works on CPU (slower). See `remote_setup.sh` for CUDA setup.

### Can't Connect via SSH

**Direct connection:**
```bash
ssh -p 18785 root@172.219.157.164
```

**Alternative (proxy):**
```bash
ssh -p 39979 root@ssh6.vast.ai
```

**Or use:** Jupyter terminal in browser

### Can't Find Public URL

**Quick method:**
```bash
./get_url.sh
```

**Or check these files:**
```bash
# Check gradio_url.txt
cat gradio_url.txt

# Search server.out.log for URL
grep "PUBLIC_URL_START" -A 1 server.out.log

# Or just look for the gradio.live URL
grep "gradio.live" server.out.log
```

**The URL is saved in multiple places:**
- `gradio_url.txt` - Clean URL only
- `server.out.log` - Between PUBLIC_URL_START/END markers
- Console output - Prominently displayed with ===== borders

### Gradio URL Not Showing

**Check logs:**
```bash
tail -f server.out.log  # Real-time logs
cat server.err.log      # Errors only
```

**Restart:**
```bash
pkill -f "python app.py"
./start.sh
```

### Model Download Slow

- ✅ Normal! ~5GB takes 5-10 minutes
- ✅ Only happens once
- ✅ Subsequent starts are fast (30-60 sec)

---

## 📝 Commands Reference

### Start/Stop
```bash
# Start (preferred method)
./start.sh

# Get public URL (if you lost it)
./get_url.sh

# Stop
pkill -f "python app.py"
# or press Ctrl+C

# Restart
pkill -f "python app.py" && ./start.sh
```

### Update
```bash
cd /workspace/Mozart_R2D2_V5
git pull
./start.sh
```

### Check Status
```bash
# Check if running
ps aux | grep "python app.py"

# Check GPU
nvidia-smi

# Check CUDA in Python
python -c "import torch; print(torch.cuda.is_available())"

# View logs
tail -f server.out.log
cat server.err.log
```

### Debug
```bash
# Check model
ls -la /workspace/models/deepseek-coder-1.3b-instruct/

# Check symlink
ls -la models/DeepSeek-Coder-1.3b-instruct/

# Check dependencies
pip list | grep -E "gradio|torch|transformers"

# Test app
python -c "import gradio, torch, transformers; print('All imports OK')"
```

---

## 🎓 Tips & Best Practices

### Getting Better Responses

1. **Be Specific** - "Write a REST API with JWT auth" vs "make an API"
2. **Provide Context** - Mention language, framework, requirements
3. **Ask Follow-ups** - The AI remembers your conversation
4. **Show Examples** - Paste code you want modified or explained

### Example Conversation Flow

```
You: "Write a Python function to sort a list using quicksort"
AI: [provides implementation]

You: "Add comments explaining the algorithm"
AI: [adds detailed comments]

You: "Now write unit tests for this function"
AI: [generates pytest tests]

You: "Optimize it for performance"
AI: [provides optimized version]
```

### When to Clear Chat

- Starting a new, unrelated topic
- Context is getting too long (slower responses)
- Want a fresh start

---

## 🚀 Performance Notes

### First Launch
- 📥 Downloads model if not present (~5GB)
- ⏱️ Takes 5-10 minutes
- 💾 Model stays cached for future use

### Subsequent Launches
- ⚡ 30-60 seconds
- 🔗 Just links model and starts
- 🚀 Much faster!

### Response Times
- 🎯 **With GPU**: 2-5 seconds per response
- 💻 **CPU Only**: 10-30 seconds per response
- 📏 Depends on response length

### Token Limits
- 📝 **Max input**: ~2048 tokens (depends on context)
- 📝 **Max output**: 512 tokens
- 🔄 Clear chat if you hit limits

---

## 📞 Support

### Quick Checks
1. ✅ Is instance running? (`nvidia-smi`)
2. ✅ Is model linked? (`ls -la models/`)
3. ✅ Are deps installed? (`pip list | grep gradio`)
4. ✅ Check logs (`cat server.err.log`)

### Common Solutions
- 🔄 **Restart**: `./start.sh`
- 🔗 **Relink model**: See Troubleshooting section
- 📦 **Reinstall deps**: `pip install -r requirements.txt`
- 🗑️ **Clean start**: `pkill -9 -f python && ./start.sh`

---

## 🎉 You're All Set!

**Next time you log in, just run:**
```bash
./start.sh
```

**Everything else is automatic!**

Built with ❤️ using DeepSeek Coder & Gradio
