---
title: Fine-Tuning Models
date: 2025-02-23
---
Google Collab provides free GPU/TPU resources perfect for fine-tuning AI models. Here's a complete guide to fine-tuning models in Colab, from setup to saving your trained model.

## Setting Up Your Colab Environment

```python
# 1. Connect to a GPU runtime
# Go to Runtime > Change runtime type > GPU

# 2. Verify GPU is available
!nvidia-smi

# 3. Install necessary libraries
!pip install -q transformers datasets accelerate peft bitsandbytes trl tensorboard
```


## Method 1: QLoRA Fine-Tuning for Large Models

This approach is ideal for 7B+ parameter models on Colab's limited GPU:

```python
# Import libraries
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# Configure quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

# Load model and tokenizer
model_id = "meta-llama/Llama-2-7b-hf"  # Or any compatible model
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

# Configure LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
)

# Apply LoRA to model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Prepare dataset
# Option 1: Load from Hugging Face
dataset = load_dataset("Abirate/english_quotes", split="train")

# Option 2: Or upload CSV to Colab
from google.colab import files
uploaded = files.upload()  # Upload your CSV
import pandas as pd
from datasets import Dataset
df = pd.read_csv("your_file.csv")
dataset = Dataset.from_pandas(df)

# Configure trainer
training_args = SFTConfig(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=50,
    save_strategy="epoch",
    fp16=True,
)

# Initialize trainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    dataset_text_field="quote"  # Change to your text column name
)

# Start training
trainer.train()

# Save the model
peft_model_id = "my-fine-tuned-model"
trainer.model.save_pretrained(peft_model_id)
tokenizer.save_pretrained(peft_model_id)

# Save to Google Drive (to avoid losing work)
from google.colab import drive
drive.mount('/content/drive')
!cp -r {peft_model_id} /content/drive/MyDrive/
```


## Method 2: Full Fine-Tuning for Smaller Models

For smaller models (under 3B parameters) that fit fully in Colab's GPU:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset

# Load model and tokenizer
model_id = "gpt2"  # Or another smaller model
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id)

# Prepare your dataset
dataset = load_dataset("imdb", split="train")

# Define data preprocessing
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Configure training
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    logging_dir="./logs",
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
)

# Start training
trainer.train()

# Save the model
model.save_pretrained("./fine-tuned-gpt2")
tokenizer.save_pretrained("./fine-tuned-gpt2")

# Save to Google Drive
!cp -r ./fine-tuned-gpt2 /content/drive/MyDrive/
```


## Dealing with Colab Limitations

### Session Timeouts

```python
# Add this to prevent idle timeouts
from IPython.display import display, Javascript
display(Javascript('''
function ClickConnect(){
  console.log("Clicking connect button"); 
  document.querySelector("colab-connect-button").click()
}
setInterval(ClickConnect, 60000)
'''))
```


### Memory Management

```python
# Clear GPU memory if needed
import gc
gc.collect()
torch.cuda.empty_cache()

# Monitor memory usage
!nvidia-smi
```


### Checkpointing

```python
# Configure checkpointing for recovery
training_args = TrainingArguments(
    # ... other args
    save_strategy="steps",
    save_steps=500,
    save_total_limit=2,  # Keep only the last 2 checkpoints
)
```


## Testing Your Fine-Tuned Model

```python
# Load your fine-tuned model
from peft import PeftModel, PeftConfig

# For LoRA models
config = PeftConfig.from_pretrained("my-fine-tuned-model")
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(model, "my-fine-tuned-model")

# Generate text
tokenizer = AutoTokenizer.from_pretrained("my-fine-tuned-model")
inputs = tokenizer("Your prompt text here", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```


## Best Practices for Colab Fine-Tuning

1. **Always connect to Google Drive** to prevent losing work if Collab disconnects
2. **Start small** - Test your pipeline with a tiny subset of data before full training
3. **Monitor GPU usage** regularly with `!nvidia-smi`
4. **Use QLoRA for large models** - It's the most efficient way to fine-tune on Colab
5. **Save checkpoints frequently** and to Google Drive
6. **Close other tabs** in your browser to prevent Collab from disconnecting due to inactivity

This guide provides everything you need to fine-tune models in Google Collab, from small BERT variants all the way to 7B+ parameter models using memory-efficient techniques.

