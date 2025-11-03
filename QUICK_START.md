# 🚀 QUICK START GUIDE

## What's New? 

You now have a **Cursor-inspired modern chat interface** for DeepSeek Coder with:
- ✨ Dark GitHub-style theme
- 💬 Multi-turn conversations with context memory
- 🎯 Temperature & token controls
- 📋 Example prompts & tips
- 🎨 Beautiful message bubbles & syntax highlighting
- 🤖 PyQt5 GUI launcher

---

## 🎯 Getting Started (Choose One)

### **Option 1: GUI Launcher (Easiest) ⭐**
```bash
python launcher.py
```
This opens a desktop window where you can:
- Download the model
- Install dependencies  
- Choose chat or simple interface
- Launch with one click
- View live logs

### **Option 2: Direct Launch**

**Modern Chat Interface:**
```bash
python chat_app.py
```

**Simple Text Interface:**
```bash
python app.py
```

### **Option 3: Automated Setup (Linux/Mac)**
```bash
bash setup_and_launch.sh
```

---

## 📋 What Each File Does

| File | Purpose |
|------|---------|
| `chat_app.py` | ✨ **NEW!** Modern Cursor-inspired chat interface |
| `launcher.py` | 🎮 **NEW!** Desktop GUI for setup and launch |
| `app.py` | 📝 Simple text-based interface |
| `requirements.txt` | 📦 Updated Python dependencies |
| `CHAT_README.md` | 📖 **NEW!** Complete documentation |
| `setup_and_launch.sh` | 🚀 **NEW!** Automated setup script |

---

## 🎨 Chat Interface Features

### When You Launch `chat_app.py`:

**You'll see:**
```
┌─────────────────────────────────┐
│ 🤖 DeepSeek Coder Chat          │
├─────────────────────────────────┤
│ [💡 Examples] [✨ Tips]          │
├─────────────────────────────────┤
│ Chat messages here...           │
├─────────────────────────────────┤
│ [Your message box]        [Send]│
│ [Clear] [Copy Response]         │
├─────────────────────────────────┤
│ [⚙️ Model Parameters]            │
└─────────────────────────────────┘
```

**Try these prompts:**
1. "Write a Python function to reverse a string"
2. "Explain async/await in JavaScript"
3. "Create a REST API endpoint in Flask"
4. "Write unit tests for a calculator"
5. "Debug this code: [paste code]"

---

## 🔧 Settings You Can Adjust

**In the Chat Interface:**
- **Temperature:** 0.1 (focused) to 1.0 (creative) — default 0.2
- **Max Tokens:** 64 to 512 — default 256
- Both take effect immediately

---

## 🌐 Using on Remote (Vast.ai)

1. **Upload your project:**
   ```bash
   scp -P 9878 -r Mozart_R2D2_V5/ root@50.35.34.14:/workspace/
   ```

2. **SSH into instance:**
   ```bash
   ssh -p 9878 root@50.35.34.14
   cd /workspace/Mozart_R2D2_V5
   ```

3. **Activate environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Launch chat interface:**
   ```bash
   python chat_app.py
   ```

5. **Access via browser:**
   - Use Vast.ai tunnel, or
   - SSH port forward: `ssh -p 9878 -L 7860:localhost:7860 root@50.35.34.14`
   - Open `http://localhost:7860`

---

## ⚠️ If Something Goes Wrong

**Model won't load?**
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Verify model exists
ls -la models/deepseek-coder-1.3b-instruct/
```

**Port already in use?**
```bash
# Edit chat_app.py and change:
server_port=8000  # or another port
```

**Need help?**
- Check `CHAT_README.md` for detailed guide
- See "Troubleshooting" section
- Review logs in the chat window

---

## 📊 What's Different From Before

| Feature | Old | New |
|---------|-----|-----|
| Interface | Simple text box | Modern chat with bubbles |
| Theme | Basic | Dark GitHub-style |
| Context | Single prompt | Multi-turn memory |
| Controls | Fixed settings | Temperature & tokens sliders |
| Help | None | Examples & tips |
| Launcher | Command line | Desktop GUI app |

---

## 💡 Pro Tips

1. **Copy code easily** - Click the copy button on responses
2. **Follow-up questions** - Chat remembers last 5 exchanges
3. **Adjust settings** - Lower temperature for code, higher for ideas
4. **Use examples** - "Here's my code: [paste] - can you fix it?"
5. **Be specific** - Better prompts = better code

---

## 🚀 You're Ready!

1. Run `python launcher.py` or `python chat_app.py`
2. Wait for it to start (20-30 seconds first time)
3. Open the URL shown in terminal
4. Start chatting!

---

**Questions?** Check `CHAT_README.md` for complete documentation! 📖

**Enjoy your AI coding assistant!** 🎉
