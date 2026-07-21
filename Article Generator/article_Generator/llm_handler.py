from transformers import AutoModelForCausalLM, AutoTokenizer

# Pre-load models and tokenizers for efficiency
model_names = {
    "GPT-Neo 1.3B": "EleutherAI/gpt-neo-1.3B",
    "Bloom-560M": "bigscience/bloom-560m",
    "OPT-1.3B": "facebook/opt-1.3b"
}

loaded_models = {}
tokenizers = {}

# Load models and tokenizers
for name, model_path in model_names.items():
    print(f"Loading {name}...")
    loaded_models[name] = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Set or add a padding token
    if tokenizer.pad_token is None:
        if tokenizer.eos_token:  # Use `eos_token` as `pad_token` if available
            tokenizer.pad_token = tokenizer.eos_token
        else:  # Otherwise, add a new `[PAD]` token
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            loaded_models[name].resize_token_embeddings(len(tokenizer))

    tokenizers[name] = tokenizer

def get_llm_response(llm_name, prompt, max_length=300):
    """Generate a response using the selected LLM."""
    model = loaded_models[llm_name]
    tokenizer = tokenizers[llm_name]

    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512, padding=True)

    # Generate text
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=max_length,
        num_beams=3,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id
    )

    # Decode the generated text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
