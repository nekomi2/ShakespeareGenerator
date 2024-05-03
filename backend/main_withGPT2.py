from fastapi import FastAPI, HTTPException
from transformers import pipeline, set_seed
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer

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
    max_length: int = 300
    seed: int = 72



# Load the trained model and tokenizer
model_path = "../training/outputs/gpt2-tiny-shakespeare-final"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.post("/generate/")
async def generate_text(prompt: Prompt):
    try:
        before = time.time()
        set_seed(prompt.seed)
        generated = generator(
            prompt.text, max_length=prompt.max_length, num_return_sequences=1
        )
        duration = time.time() - before
        print(generated)
        return {
            "generated_text": generated[0]["generated_text"],
            "response_time": duration,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
