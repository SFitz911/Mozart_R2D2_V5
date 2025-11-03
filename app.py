import gradio as gr
import logging
import torch
import socket
from transformers import AutoTokenizer, AutoModelForCausalLM

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("deepseek_gradio")

# Load the model
logger.info("Loading DeepSeek Coder model...")
try:
    model_path = "models/deepseek-coder-1.3b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.float16).to('cuda')
    logger.info(f"Model device after loading: {model.device}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

def safe_generate(prompt):
    if model is None:
        return "Model not loaded. Error during initialization."
    try:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        output = model.generate(input_ids, max_new_tokens=256)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        generated_text = generated_text[len(prompt):].strip()
        return generated_text
    except Exception as e:
        logger.error(f"Error during inference: {e}", exc_info=True)
        return f"Error: {e}"

iface = gr.Interface(
    fn=safe_generate,
    inputs=[gr.Textbox(label="Code Prompt", placeholder="Enter your code generation prompt here...")],
    outputs=[gr.Textbox(label="Generated Code")],
    title="Mozart R2D2",
    description="Generate code using DeepSeek Coder model."
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
        port = find_open_port(7860, 9000)
        logger.info(f"Starting Gradio app on 0.0.0.0:{port} with share=True")
        iface.launch(server_name="0.0.0.0", server_port=port, share=True)
    except Exception as e:
        logger.error(f"Failed to launch Gradio app: {e}")
