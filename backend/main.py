from fastapi import FastAPI, HTTPException
from transformers import pipeline, set_seed
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time


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


generator = pipeline("text-generation", model="vicgalle/gpt2-open-instruct-v1")
set_seed(42)


@app.post("/generate/")
async def generate_text(prompt: Prompt):
    try:
        before = time.time()
        set_seed(prompt.seed)
        user_prompt = f'Below is an instruction that describes a task. \
        Write a response that appropriately completes the request. \
        \n ### Instruction: \
        \n Pretend you are Shakespeare, complete this request in Shakespearean English. {prompt.text}\
        \n ### Response:'
        generated = generator(
            user_prompt, max_length=prompt.max_length, num_return_sequences=1
        )
        duration = time.time() - before
        print(generated)
        return {
            "generated_text": generated[0]["generated_text"][len(user_prompt) :],
            "response_time": duration,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
