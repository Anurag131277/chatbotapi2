#import requests
#from pyrogram import Client as Bot
#from pyrogram import idle
#from config import API_ID, API_HASH, BOT_TOKEN


#bot = Bot(
 #   ":memory:",
 #   API_ID,
#API_HASH,
#    bot_token=BOT_TOKEN,
#   plugins=dict(root="plugins")
#)

#bot.start()

#idle()
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fastapi.middleware.cors import CORSMiddleware

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.get("/chatbot/{query}")
async def read_item(query : str):
    text= query
    for step in range(1):
        new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return {"query": response}
