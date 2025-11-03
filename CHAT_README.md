# 🤖 Mozart R2D2 V5 - DeepSeek Coder Chat Interface

**A Cursor-inspired modern chat interface for DeepSeek Coder with PyQt5 launcher**

---

## ⚡ Quick Start (30 Seconds)

### Option 1: GUI Launcher (Recommended)
```bash
python launcher.py
```
- Choose interface type
- Download model (if needed)
- Install dependencies
- Launch with one click
- View real-time logs

### Option 2: Direct Launch

**Modern Chat Interface:**
```bash
python chat_app.py
```

**Simple Text Interface:**
```bash
python app.py
```

Both launch on `http://0.0.0.0:7860`

---

## ✨ Features

### 🎨 Modern Chat UI
- **Dark Theme** - GitHub colors (#010409, #0d1117, #58a6ff)
- **Cursor-Inspired** - clean, professional design
- **Message Bubbles** - beautiful conversation layout
- **Syntax Highlighting** - readable code blocks
- **8 Example Prompts** - quick starting points
- **Tips Accordion** - feature discovery
- **One-Click Copy** - easy response copying
- **Clear Chat** - fresh start button

### 💬 Conversation Features
- **Multi-turn Context** - remembers last 5 exchanges
- **Real-time Streaming** - see responses generate
- **Context-Aware** - understands follow-up questions
- **Chat History** - full conversation memory

### 🚀 Code Generation
- **Temperature: 0.2** - focused, accurate responses
- **Max Tokens: 512** - balanced response length
- **Repetition Penalty: 1.2** - cleaner code
- **Top-P: 0.95** - quality + diversity
- **Adjustable Parameters** - fine-tune on-the-fly

### 📋 Model Parameters
Adjust in real-time:
- Temperature (0.1-1.0)
- Max Tokens (64-512)
- See immediate impact

---

## 📦 Installation

### Requirements
- Python 3.10+
- CUDA 11.8+ (optional, for GPU acceleration)
- 4GB+ RAM (16GB+ recommended)

### Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download model:**
   ```bash
   huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct \
     --local-dir models/deepseek-coder-1.3b-instruct
   ```

Or use the GUI launcher - it handles all of this!

---

## 🎮 Using the Chat Interface

### Layout
```
┌────────────────────────────────────────┐
│  🤖 DeepSeek Coder Chat                │
├────────────────────────────────────────┤
│  [💡 Examples] [✨ Tips]                │
├────────────────────────────────────────┤
│                                        │
│  🤖 Bot: Hello! How can I help?        │
│                                        │
│  👤 You: Write a Python function  ➜  │
│                                        │
│  🤖 Bot: Here's the code:             │
│         ```python                      │
│         def func(): ...                │
│         ```                            │
│                                        │
├────────────────────────────────────────┤
│  [Type here...]                  [Send]│
│  [Clear Chat] [Copy Last Response]    │
├────────────────────────────────────────┤
│  [⚙️ Model Parameters]                 │
└────────────────────────────────────────┘
```

### Example Prompts

1. **Write Python function:** "Write a function to reverse a string"
2. **REST API:** "Create a REST API endpoint in Flask"
3. **JavaScript concepts:** "Explain async/await with examples"
4. **SQL queries:** "Write a query to find duplicates"
5. **Unit tests:** "Create unit tests for factorial function"
6. **CSS layouts:** "Write a CSS flexbox layout"
7. **Programming concepts:** "Explain closures with examples"
8. **Algorithms:** "Write a quicksort algorithm in Python"

### Tips & Features

**Temperature Setting:**
- 0.1 = Very focused, deterministic
- 0.2 = Default (accurate, consistent)
- 0.5 = Balanced
- 1.0 = Creative, varied

**Max Tokens:**
- 64 = Quick responses
- 256 = Default (balanced)
- 512 = Detailed responses

**Context Window:**
- Last 5 exchanges used for context
- Great for follow-up questions
- Natural conversation flow

---

## 🔧 Configuration

### Adjust in Web UI
Under "⚙️ Model Parameters":
- Temperature slider (0.1-1.0)
- Max tokens slider (64-512)
- Changes take effect immediately

### Server Settings
Edit `chat_app.py` to change:

```python
demo.launch(
    server_name="0.0.0.0",     # "0.0.0.0" for all, "127.0.0.1" for local
    server_port=7860,          # Change port here
    share=True,                # Set False to disable public sharing
)
```

### Model Generation Parameters
Edit in `generate_code()` function:
```python
output = model.generate(
    input_ids,
    max_new_tokens=min(max_tokens, 512),
    temperature=temperature,
    top_p=0.95,               # Adjust diversity
    repetition_penalty=1.2,   # Adjust repetition reduction
)
```

---

## 🌐 Remote Deployment

### Deploy to Vast.ai

**1. Upload project:**
```bash
scp -P <port> -r Mozart_R2D2_V5/ root@<ip>:/workspace/
```

**2. SSH into instance:**
```bash
ssh -p <port> root@<ip>
cd /workspace/Mozart_R2D2_V5
```

**3. Set up:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
huggingface-cli download deepseek-ai/deepseek-coder-1.3b-instruct \
  --local-dir models/deepseek-coder-1.3b-instruct
```

**4. Launch:**
```bash
python chat_app.py
```

**5. Access via Vast.ai tunnel or SSH forwarding:**
```bash
# SSH port forward (from local machine)
ssh -p <port> -L 7860:localhost:7860 root@<ip>
# Then open http://localhost:7860
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Model Size | 1.3B parameters |
| Memory Usage | ~3-4GB VRAM |
| Generation Speed | 50-100 tokens/sec |
| Response Time | 2-10 seconds typical |
| Max Context | Last 5 exchanges |

---

## 🐛 Troubleshooting

### Issue: Model won't load

**Check CUDA availability:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**Verify model download:**
```bash
ls -la models/deepseek-coder-1.3b-instruct/
```

**Fallback to CPU:**
Edit `chat_app.py`, change `.to('cuda')` to `.to('cpu')`

### Issue: Port already in use

**Use different port:**
```bash
python chat_app.py  # Edit server_port in code
```

**Kill existing process:**
```bash
# Linux/Mac:
lsof -i :7860 | grep LISTEN | awk '{print $2}' | xargs kill

# Windows:
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

### Issue: Out of memory

**Reduce token generation:**
Edit `chat_app.py`:
```python
max_new_tokens=min(max_tokens, 256)  # Reduce from 512
```

### Issue: Slow responses

**Check GPU usage:**
```bash
nvidia-smi
```

**Reduce batch processing:**
- Lower max_tokens
- Reduce temperature (more focused = faster)

### Ignore these warnings
- `pkg_resources is deprecated` - harmless
- `Could not get documentation group` - UI documentation only
- `torch_dtype is deprecated` - framework update, ignored

---

## 📚 Example Conversations

### Example 1: Writing a Function

**You:** Write a Python function to check if a number is prime

**Bot:**
```python
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Test
print(is_prime(17))  # True
print(is_prime(18))  # False
```

### Example 2: Explaining Concepts

**You:** Explain what a closure is with a JavaScript example

**Bot:**
A closure is a function that has access to variables from its outer scope...
[detailed explanation with code examples]

### Example 3: Debugging

**You:** This code is throwing an error. Fix it:
```javascript
const arr = [1,2,3]
arr.map(x => x * 2).then(...)
```

**Bot:**
Arrays don't have a `.then()` method. Here's the corrected approach:
[fixed code with explanation]

---

## 🎓 Resources

- [DeepSeek Coder GitHub](https://github.com/deepseek-ai/deepseek-coder)
- [Gradio Documentation](https://gradio.app)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [CUDA Setup Guide](https://docs.nvidia.com/cuda/)
- [PyTorch Documentation](https://pytorch.org/docs/)

---

## 📁 Project Structure

```
Mozart_R2D2_V5/
├── launcher.py           # PyQt5 GUI launcher
├── chat_app.py          # Modern chat interface (NEW!)
├── app.py               # Simple text interface
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── models/              # DeepSeek model directory
│   └── deepseek-coder-1.3b-instruct/
├── .venv/               # Virtual environment
└── .git/                # Version control
```

---

## 💡 Tips for Best Results

1. **Be Specific:** "Write a function to sort an array" → specific
2. **Provide Context:** Share relevant code or requirements
3. **Ask Follow-ups:** "Can you optimize this?" works great
4. **Adjust Temperature:** Lower for consistency, higher for creativity
5. **Use Examples:** Show what you want in comments
6. **Break Complex Tasks:** Split into smaller requests

---

## 🤝 Contributing

Fork, modify, improve, and share!

---

## 📧 Support

**Issues?**
1. Check Troubleshooting section
2. Review logs in chat window
3. Verify model download and dependencies
4. Check GPU availability

---

**Happy coding! 🚀 Powered by DeepSeek Coder 1.3B**
