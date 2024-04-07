from fastapi import FastAPI, HTTPException
from transformers import pipeline, set_seed
from pydantic import BaseModel

app = FastAPI()

class Prompt(BaseModel):
    text: str
    max_length: int = 50
    seed: int = 42

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

@app.post("/generate/")
async def generate_text(prompt: Prompt):
    try:
        set_seed(prompt.seed)
        generated = generator(prompt.text, max_length=prompt.max_length, num_return_sequences=1)
        return {"generated_text": generated[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))