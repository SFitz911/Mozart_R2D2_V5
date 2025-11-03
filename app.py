import gradio as gr
import logging
import torch
import socket
from transformers import AutoTokenizer, AutoModelForCausalLM

# Setup logging with detailed output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output to console/log files
    ]
)
logger = logging.getLogger("mozart_r2d2")

# Load the model with detailed logging
logger.info("=" * 60)
logger.info("🚀 Mozart_R2D2_V5 - Initializing...")
logger.info("=" * 60)
logger.info("")

logger.info("📋 System Information:")
logger.info(f"   Python version: {torch.__version__}")
logger.info(f"   PyTorch version: {torch.__version__}")
logger.info(f"   CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    logger.info(f"   CUDA version: {torch.version.cuda}")
    logger.info(f"   GPU: {torch.cuda.get_device_name(0)}")
    logger.info(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
logger.info("")

logger.info("🤖 Loading DeepSeek Coder model...")
try:
    model_path = "models/DeepSeek-Coder-1.3b-instruct/deepseek-coder-1.3b-instruct"
    logger.info(f"   Model path: {model_path}")
    
    logger.info("   Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    logger.info(f"   ✅ Tokenizer loaded (vocab size: {len(tokenizer)})")
    
    logger.info("   Loading model weights...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        trust_remote_code=True, 
        torch_dtype=torch.float16
    ).to('cuda' if torch.cuda.is_available() else 'cpu')
    
    logger.info(f"   ✅ Model loaded on device: {model.device}")
    logger.info(f"   Model dtype: {model.dtype}")
    logger.info("   ✅ Model initialization complete!")
except Exception as e:
    logger.error("=" * 60)
    logger.error("❌ FAILED TO LOAD MODEL")
    logger.error("=" * 60)
    logger.error(f"Error: {e}")
    logger.error("The application will run but code generation will not work.")
    logger.error("=" * 60)
    model = None
    tokenizer = None

logger.info("")

def safe_generate(message, history):
    """Generate code based on user prompt with conversation history (Cursor-style)"""
    if model is None or tokenizer is None:
        error_msg = "❌ Model not loaded. Error during initialization."
        logger.error(error_msg)
        return error_msg
    
    try:
        # Build conversation context from history
        conversation = ""
        for user_msg, assistant_msg in history:
            conversation += f"### Instruction:\n{user_msg}\n\n### Response:\n{assistant_msg}\n\n"
        
        # Add current message
        full_prompt = conversation + f"### Instruction:\n{message}\n\n### Response:\n"
        
        logger.info(f"📝 Generating code for: {message[:50]}...")
        
        input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids.to(model.device)
        logger.info(f"   Input tokens: {len(input_ids[0])}")
        
        # Better generation parameters for code
        output = model.generate(
            input_ids,
            max_new_tokens=512,
            temperature=0.2,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1
        )
        
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        # Extract only the new response
        generated_text = generated_text[len(full_prompt):].strip()
        
        # Clean up if it generated extra instructions
        if "### Instruction:" in generated_text:
            generated_text = generated_text.split("### Instruction:")[0].strip()
        
        logger.info(f"   ✅ Generation complete ({len(generated_text)} chars)")
        return generated_text
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"❌ Error during code generation: {e}", exc_info=True)
        logger.error("=" * 60)
        return f"Error: {e}"

# Create Cursor-like chat interface
with gr.Blocks(
    title="Mozart R2D2 - DeepSeek Coder AI",
    theme=gr.themes.Monochrome(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
    ),
    css="""
        footer {visibility: hidden}
        .container {max-width: 100% !important}
        
        /* Cursor-like styling */
        body {background: #1a1a1a !important}
        
        .gradio-container {
            max-width: 100% !important;
            background: #1a1a1a !important;
        }
        
        /* Chat interface styling */
        .chatbot {
            height: 70vh !important;
            border-radius: 12px !important;
            background: #0d1117 !important;
        }
        
        .message {
            border-radius: 8px !important;
            padding: 16px !important;
            margin: 8px 0 !important;
        }
        
        .message.user {
            background: #1f6feb !important;
        }
        
        .message.bot {
            background: #161b22 !important;
        }
        
        /* Code blocks */
        pre {
            background: #0d1117 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
            padding: 16px !important;
            overflow-x: auto !important;
        }
        
        code {
            color: #c9d1d9 !important;
            font-family: 'Fira Code', 'Consolas', monospace !important;
            font-size: 14px !important;
        }
        
        /* Input styling */
        textarea {
            background: #0d1117 !important;
            border: 1px solid #30363d !important;
            color: #c9d1d9 !important;
            font-size: 15px !important;
            border-radius: 8px !important;
        }
        
        /* Buttons */
        .btn-primary {
            background: #1f6feb !important;
            border: none !important;
            font-weight: 600 !important;
        }
        
        .btn-secondary {
            background: #21262d !important;
            border: 1px solid #30363d !important;
        }
        
        /* Examples */
        .examples {
            background: #161b22 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
    """
) as iface:
    
    with gr.Row():
        gr.Markdown(
            """
            # 🎵 Mozart R2D2 - AI Coding Assistant
            ### Powered by DeepSeek Coder | Cursor-Style Interface
            
            Ask me to write code, explain concepts, debug issues, or refactor existing code.
            I maintain conversation context for follow-up questions!
            """,
            elem_classes="header"
        )
    
    # Main chat interface (Cursor-style)
    chatbot = gr.Chatbot(
        label="💬 Conversation",
        height=600,
        show_copy_button=True,
        avatar_images=(None, "🤖"),
        bubble_full_width=False,
        elem_classes="chatbot"
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="",
            placeholder="💭 Ask me anything about coding... (e.g., 'Write a REST API with authentication')",
            lines=3,
            max_lines=10,
            scale=9,
            show_label=False
        )
        with gr.Column(scale=1, min_width=100):
            submit = gr.Button("🚀 Send", variant="primary", size="lg")
            clear = gr.Button("🗑️ Clear Chat", variant="secondary")
    
    # Example prompts (Cursor-style)
    gr.Examples(
        examples=[
            ["Write a Python function to implement quicksort with comments"],
            ["Create a React component for a todo list with TypeScript"],
            ["Build a REST API with Flask including JWT authentication"],
            ["Write a SQL query to find the top 10 customers by revenue"],
            ["Implement a binary search tree in JavaScript with all methods"],
            ["Create a Docker Compose file for a MERN stack application"],
            ["Write unit tests for a user authentication service"],
            ["Explain how async/await works in Python with examples"],
        ],
        inputs=msg,
        label="💡 Example Prompts",
        elem_classes="examples"
    )
    
    # Chat functionality
    def respond(message, chat_history):
        if not message.strip():
            return "", chat_history
        
        # Generate response
        bot_message = safe_generate(message, chat_history)
        
        # Add to history
        chat_history.append((message, bot_message))
        
        return "", chat_history
    
    def clear_chat():
        return None
    
    # Event handlers
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, None, chatbot)
    
    # Info section
    with gr.Accordion("ℹ️ Tips & Features", open=False):
        gr.Markdown(
            """
            ### 🎯 How to Use:
            - **Ask anything**: Request code in any language, explain concepts, debug issues
            - **Follow-up questions**: I remember our conversation context!
            - **Specific requests**: Be detailed for better results
            - **Copy code**: Click the copy button on any response
            
            ### 🚀 Features:
            - ✅ Multi-turn conversations with context awareness
            - ✅ Syntax highlighting for code
            - ✅ Better code generation (temperature: 0.2, up to 512 tokens)
            - ✅ One-click code copying
            - ✅ Cursor-inspired dark theme
            
            ### 💡 Example Queries:
            - "Write a function to..." → Get implementation
            - "Explain how..." → Get detailed explanation with examples
            - "Debug this code..." → Get help fixing issues
            - "Refactor..." → Get improved code suggestions
            - "Add tests for..." → Get unit tests
            """
        )


def find_open_port(start=7860, end=9000):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No open port found in range {start}-{end}")

if __name__ == "__main__":
    try:
        logger.info("=" * 60)
        logger.info("🌐 Starting Gradio Web Interface")
        logger.info("=" * 60)
        logger.info("")
        
        port = find_open_port(7860, 9000)
        logger.info(f"✅ Found available port: {port}")
        logger.info(f"🚀 Launching on 0.0.0.0:{port} with public URL sharing...")
        logger.info("")
        
        # Launch and get the app object
        app_obj = iface.launch(server_name="0.0.0.0", server_port=port, share=True)
        
        # Try to capture and save the public URL
        try:
            share_url = getattr(app_obj, 'share_url', None)
            if share_url:
                # Write to console/logs with VERY prominent formatting
                logger.info("")
                logger.info("=" * 80)
                logger.info("=" * 80)
                logger.info("🎉 SUCCESS! Mozart_R2D2_V5 is now running!")
                logger.info("=" * 80)
                logger.info("")
                logger.info("📡 PUBLIC URL (Copy this):")
                logger.info("")
                logger.info(f"    {share_url}")
                logger.info("")
                logger.info("=" * 80)
                logger.info("")
                logger.info("   ✅ Open this URL in any browser to access your")
                logger.info("      AI coding assistant from anywhere!")
                logger.info("")
                logger.info(f"   🌐 Local URL: http://localhost:{port}")
                logger.info(f"   🌐 Network URL: http://0.0.0.0:{port}")
                logger.info("")
                logger.info("   💡 TIP: Find this URL anytime in server.out.log")
                logger.info("   💡 Or in gradio_url.txt file")
                logger.info("")
                logger.info("   🛑 Press Ctrl+C to stop the server")
                logger.info("=" * 80)
                logger.info("=" * 80)
                logger.info("")
                
                # Save URL to file
                with open("gradio_url.txt", "w") as f:
                    f.write(share_url.strip() + "\n")
                
                # Also append to server.out.log with a marker for easy finding
                with open("server.out.log", "a") as f:
                    f.write("\n")
                    f.write("=" * 80 + "\n")
                    f.write("PUBLIC_URL_START\n")
                    f.write(f"{share_url}\n")
                    f.write("PUBLIC_URL_END\n")
                    f.write("=" * 80 + "\n")
                    f.write("\n")
                
                logger.info(f"💾 Public URL saved to: gradio_url.txt and server.out.log")
            else:
                logger.warning("⚠️  Could not retrieve public URL from Gradio")
        except Exception as e:
            logger.error(f"❌ Failed to save Gradio URL: {e}")
            
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ FAILED TO LAUNCH APPLICATION")
        logger.error("=" * 60)
        logger.error(f"Error: {e}", exc_info=True)
        logger.error("=" * 60)
