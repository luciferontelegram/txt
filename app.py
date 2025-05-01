from flask import Flask
import os
from threading import Thread
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Advance TXT Uploader Bot is Running!'

def run_bot():
    subprocess.run(["python3", "main.py"])

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
