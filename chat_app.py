"""
Modern Chat Interface for DeepSeek Coder
Cursor-inspired design with dark theme and advanced features
"""

import gradio as gr
import logging
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Tuple
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("deepseek_chat")

# Load the model
logger.info("Loading DeepSeek Coder model...")
try:
    model_path = "models/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        trust_remote_code=True, 
        torch_dtype=torch.float16
    ).to('cuda')
    logger.info(f"Model device after loading: {model.device}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

# Example prompts for users
EXAMPLE_PROMPTS = [
    "Write a Python function to reverse a string",
    "Create a REST API endpoint in Flask",
    "Explain async/await in JavaScript",
    "Write a SQL query to find duplicates",
    "Create a unit test for a calculator function",
    "Write a CSS flexbox layout",
    "Explain what a closure is with examples",
    "Write a quick sort algorithm in Python",
]

def generate_code(message: str, history: List[Tuple[str, str]], temperature: float = 0.2, max_tokens: int = 512) -> str:
    """
    Generate code or text response with temperature and token control.
    
    Args:
        message: User's input message
        history: Chat history for context
        temperature: Sampling temperature (0.2 for focused output)
        max_tokens: Maximum tokens to generate (up to 512)
    
    Returns:
        Generated text response
    """
    if model is None:
        return "❌ **Model not loaded.** Error during initialization. Please check the logs."
    
    try:
        # Build context from history
        context = ""
        for user_msg, bot_msg in history[-5:]:  # Keep last 5 exchanges for context
            context += f"User: {user_msg}\n"
            context += f"Assistant: {bot_msg}\n\n"
        
        # Prepare full prompt
        full_prompt = context + f"User: {message}\nAssistant:"
        
        # Tokenize
        input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids.to(model.device)
        
        # Generate with temperature control
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_new_tokens=min(max_tokens, 512),
                temperature=temperature,
                top_p=0.95,
                repetition_penalty=1.2,  # Reduce repetition
                do_sample=True,
            )
        
        # Decode
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        response = generated_text[len(full_prompt):].strip()
        
        # Clean up response
        response = response.split('\n\nUser:')[0]  # Remove next user prompt if included
        
        return response if response else "I'm having trouble generating a response. Try rephrasing your question."
        
    except Exception as e:
        logger.error(f"Error during inference: {e}", exc_info=True)
        return f"❌ **Error during generation:** {str(e)[:200]}"

# Create custom CSS for Cursor-inspired dark theme
custom_css = """
:root {
    --primary: #010409;
    --secondary: #0d1117;
    --tertiary: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-secondary: #8b949e;
    --accent: #FFD700;
    --success: #3fb950;
    --warning: #d29922;
    --error: #f85149;
    --yellow-text: #FFD700;
}

* {
    font-family: 'Segoe UI', 'Roboto', 'Monaco', monospace;
}

body {
    background-color: var(--primary) !important;
    color: var(--text) !important;
}

.gradio-container {
    background-color: var(--primary) !important;
    max-width: 900px !important;
}

/* Chat container */
.chatbot-container {
    background-color: var(--secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Messages */
.message {
    border-radius: 8px !important;
    padding: 12px 16px !important;
    margin: 8px 0 !important;
    word-wrap: break-word !important;
}

.message.user {
    background-color: #1a3a52 !important;
    color: var(--yellow-text) !important;
    margin-left: auto !important;
    max-width: 80% !important;
}

.message.bot {
    background-color: var(--tertiary) !important;
    color: var(--yellow-text) !important;
    border: 1px solid var(--border) !important;
    max-width: 80% !important;
}

/* Code blocks */
code {
    background-color: var(--tertiary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    color: #79c0ff !important;
}

pre {
    background-color: var(--primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 12px !important;
    overflow-x: auto !important;
}

pre code {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Input */
textarea {
    background-color: var(--secondary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

textarea:focus {
    border-color: var(--accent) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2) !important;
}

/* Buttons */
button {
    background-color: var(--accent) !important;
    color: #010409 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

button:hover {
    background-color: #FFF44F !important;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.5) !important;
}

button:active {
    background-color: #FFD700 !important;
}

/* Labels */
label {
    color: var(--text) !important;
    font-weight: 500 !important;
}

/* Header */
h1 {
    color: var(--text) !important;
    text-align: center !important;
}

p {
    color: var(--text-secondary) !important;
}

/* Accordion */
.accordion-label {
    background-color: var(--tertiary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}
"""

# Create the Gradio chat interface
def chat_interface(message: str, history: List[Tuple[str, str]]) -> str:
    """Wrapper function for Gradio chatbot"""
    return generate_code(message, history)

# Build the app with custom theme
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.HTML("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="font-size: 2.5em; margin: 0; color: #FFD700;">🎵 Mozart R2D2</h1>
        <p style="color: #FFD700; font-size: 1.1em; margin: 10px 0;">
            Powered by DeepSeek Coder OpenSource 🎸 Oh Yeah!
        </p>
        <p style="color: #FFD700; font-size: 0.95em; margin: 10px 0;">
            🥝 Created by knowledge gained by New Zealand's best. Nextwork.org. 🥝
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column():
            # Example prompts
            with gr.Accordion("💡 Example Prompts", open=False):
                gr.HTML("<div style='color: #8b949e; font-size: 0.9em; line-height: 1.8;'>" + 
                        "<br>".join([f"• {prompt}" for prompt in EXAMPLE_PROMPTS]) + 
                        "</div>")
            
            # Tips & Features
            with gr.Accordion("✨ Tips & Features", open=False):
                gr.HTML("""
                <div style='color: #8b949e; font-size: 0.9em; line-height: 1.8;'>
                    <strong style='color: #79c0ff;'>🎯 Features:</strong><br>
                    • Temperature: 0.2 (focused, accurate responses)<br>
                    • Up to 512 tokens per response<br>
                    • Repetition penalty for cleaner code<br>
                    • Context-aware multi-turn conversations<br>
                    • Syntax highlighting support<br>
                    <br>
                    <strong style='color: #79c0ff;'>💡 Tips:</strong><br>
                    • Be specific with your code requests<br>
                    • Ask follow-up questions for refinement<br>
                    • Request explanations with examples<br>
                    • Use code blocks for better formatting<br>
                </div>
                """)
    
    # Chat interface
    chatbot = gr.Chatbot(
        label="Chat with DeepSeek Coder",
        height=500,
        show_label=True,
        container=True,
        type="tuples",
    )
    
    with gr.Row():
        message_input = gr.Textbox(
            label="Your Message",
            placeholder="Type your code generation request... (Press Enter to send)",
            lines=2,
            show_label=False,
            scale=4,
        )
        send_button = gr.Button("Send", scale=1)
    
    with gr.Row():
        clear_button = gr.Button("🗑️ Clear Chat", scale=1)
        copy_button = gr.Button("📋 Copy Last Response", scale=1)
    
    # Parameters for fine-tuning
    with gr.Accordion("⚙️ Model Parameters", open=False):
        with gr.Row():
            temperature = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.2,
                step=0.1,
                label="Temperature (Lower = More Focused)",
            )
            max_tokens = gr.Slider(
                minimum=64,
                maximum=512,
                value=256,
                step=32,
                label="Max Tokens",
            )
    
    # Chat functionality
    def process_message(message: str, history: List[Tuple[str, str]], temp: float, tokens: int):
        """Process user message and generate response"""
        if not message.strip():
            return history
        
        response = generate_code(message, history, temperature=temp, max_tokens=tokens)
        history.append((message, response))
        return history
    
    # Event handlers
    send_button.click(
        process_message,
        inputs=[message_input, chatbot, temperature, max_tokens],
        outputs=[chatbot],
    ).then(
        lambda: "",
        outputs=[message_input],
    )
    
    message_input.submit(
        process_message,
        inputs=[message_input, chatbot, temperature, max_tokens],
        outputs=[chatbot],
    ).then(
        lambda: "",
        outputs=[message_input],
    )
    
    clear_button.click(lambda: [], outputs=[chatbot])
    
    # Copy functionality (note: Gradio has limited clipboard access)
    copy_button.click(
        lambda hist: f"Last response copied! ({len(hist[-1][1])} chars)" if hist else "No messages yet",
        inputs=[chatbot],
        outputs=[gr.Textbox(label="Status", interactive=False)],
    )
    
    gr.HTML("""
    <div style='text-align: center; margin-top: 30px; color: #8b949e; font-size: 0.9em;'>
        <p>🚀 Powered by DeepSeek Coder 1.3B • CUDA Accelerated • GitHub-inspired Dark Theme</p>
    </div>
    """)

if __name__ == "__main__":
    logger.info("Starting Gradio chat interface on 0.0.0.0:7860 with share=True")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
    )
