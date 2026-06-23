import urequests
import ujson

def handle_update(update, base_url):
    if "message" not in update:
        return
        
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    if text:
        print(f"Received: {text}")
        send_message(base_url, chat_id, f"Echo: {text}")

def send_message(base_url, chat_id, text):
    url = f"{base_url}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    headers = {'Content-Type': 'application/json'}
    
    try:
        res = urequests.post(url, data=ujson.dumps(payload), headers=headers)
        res.close()
    except Exception as e:
        print(f"Send failed: {e}")
