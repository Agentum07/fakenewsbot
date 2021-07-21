# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 18:29:28 2021

@author: agent
"""

import Constants as keys
from telegram.ext import *
import pickle
import string
import pandas as pd

import os
PORT = int(os.environ.get('PORT', 8443))

print("Bot started...")

def start_command(update, context):
    update.message.reply_text('Type something and get a fake news detection')
    
def help_command(update, context):
    update.message.reply_text("Type a text and I'll tell you what I think of its validity!")
    
def load_model():
    global model
    model = pickle.load(open('model.pkl','rb'))
    print('Model loaded')

def handle_message(update, context):
    text = str(update.message.text).lower()
    all_list = [char for char in text if char not in string.punctuation]
    text = ''.join(all_list)
    lines = []
    lines.append(text)
    df = pd.DataFrame({'text' : lines}).astype(str)
    
    result = {}    
    
    # predictions
    result['Query'] = model.predict(df)[0]
    response = model.input(text)
    
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")
    
def main():
    load_model()
    updater = Updater(keys.API_KEY, use_context = True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start_command))
    
    dp.add_handler(CommandHandler("help", help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_error_handler(error)
    
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=keys.API_KEY,
                          webhook_url = 'https://fakenews-api-file.herokuapp.com/' + keys.API_KEY)
    updater.bot.setWebhook('https://fakenews-api-file.herokuapp.com/' + keys.API_KEY)
    
    updater.idle()

if __name__ == '__main__':
    main()