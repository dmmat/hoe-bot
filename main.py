from ShutdownBot import ShutdownBot
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from Watchdog import *
import os
import logging

app = FastAPI()
shutdown_bot = ShutdownBot()

allowed_chat_ids = list(map(int, os.getenv("ALLOWED_CHAT_IDS").split(",")))

street_id = os.getenv("STREET_ID")
house = os.getenv("HOUSE")

logging.basicConfig(level=logging.INFO)

# Pydantic модель для обробки оновлень від Telegram
class TelegramWebhook(BaseModel):
    update_id: int
    message: dict

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tg-webhook")
async def webhook(request: Request):
    data = await request.json()
    if "message" in data:
        message = data["message"]
        text = message.get("text", "")
        chat_id = message["chat"]["id"]
        if chat_id not in allowed_chat_ids:
            # response_text = "You are not allowed to use this bot"
            logging.info(f"User {chat_id} is not allowed")
            return JSONResponse(content={"status": "not allowed"})
        elif text.startswith("/start"):
            response_text = "Hello! Use /shutdown or /queue or /schedule or /status"
        elif text.startswith("/shutdown"):
            response_text = shutdown_bot.get_current_shutdown(street_id, house)
            update_shutdown(response_text)
        elif text.startswith("/queue"):
            response_text = shutdown_bot.get_shutdown_queue(street_id, house)
            update_queue(response_text)
        elif text.startswith("/schedule"):
            image_url = shutdown_bot.get_shutdown_schedule_image()
            update_schedule(image_url)            
            send_image(chat_id, image_url)
            return JSONResponse(content={"status": "ok"})
        elif text.startswith("/status"):
            if not os.getenv("ROUTER_URL"):  
                return {"status": "error", "message": "ROUTER_URL is not set"}
            
            status = check_home_server_status()
            update_status(status)
   
            response_text = "Електроенергія є" if status else "Скоріше за все електроенергії немає \n/shutdown - перевірити відключення"
        else:
            return JSONResponse(content={"status": "ok"})

        send_message(chat_id, response_text)
    return JSONResponse(content={"status": "ok"})


@app.get("/sw")
async def set_webhook():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    params = {
        "url": f'{WEBHOOK_URL}/tg-webhook'
    }

    response = requests.post(url, params=params)
    
    # set commands
    commands = [
        {
            "command": "queue",
            "description": "Показати чергу"
        },
        {
            "command": "schedule",
            "description": "Показати графік відключень"
        },
        {
            "command": "shutdown",
            "description": "Показати чи є актуальні відключення"
        },
        {
            "command": "status",
            "description": "Перевірити чи є електроенергія в дома"
        }
    ]
  
    url = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"
    response2 = requests.post(url, json={"commands": commands})
    
    
    return response.json()


@app.post("/__space/v0/actions")
async def space_actions(request: Request):
    data = await request.json()
    if data["event"] and data["event"]["id"] == "check":
    
        logging.info(data)
        NOTIFY_CHAT_IDS = os.getenv("NOTIFY_CHAT_IDS") or os.getenv("ALLOWED_CHAT_IDS") or []
        chats = list(map(int, NOTIFY_CHAT_IDS.split(",")))
        
        for chat_id in chats:
            status = check_home_server_status()
            if status_changed(status):
                response_text = "Електроенергія є" if status else "Скоріше за все електроенергії немає \n/shutdown - перевірити відключення"
                send_message(chat_id, response_text)
            
            schedule = shutdown_bot.get_shutdown_schedule_image()
            if schedule_changed(schedule):
                send_image(chat_id, schedule)
            
            queue = shutdown_bot.get_shutdown_queue(street_id, house)
            if queue_changed(queue):
                send_message(chat_id, queue)
                
            shutdown = shutdown_bot.get_current_shutdown(street_id, house)
            if shutdown_changed(shutdown):
                send_message(chat_id, shutdown)
            
        return JSONResponse(content={"status": "ok"})
                

def send_message(chat_id: int, text: str):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
    
def send_image(chat_id: int, image_url: str):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": image_url
    }
    requests.post(url, json=payload)

def check_home_server_status():
    router_url = os.getenv("ROUTER_URL")
    response = requests.get(router_url)
    return response.status_code == 200


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)