from fastapi import FastAPI, HTTPException
from transformers import set_seed, AutoTokenizer
import transformers
import torch
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
from transformers import AutoModelForCausalLM


app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    text: str
    max_length: int = 50
    seed: int = 42


set_seed(42)
model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model, load_in_4bit=True, device_map="auto")


@app.post("/generate/")
async def generate_text(prompt: Prompt):
    try:
        before = time.time()
        set_seed(prompt.seed)
        inputs = tokenizer(prompt.text, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=prompt.max_length)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        duration = time.time() - before
        return {
            "generated_text": generated_text,
            "response_time": duration,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
