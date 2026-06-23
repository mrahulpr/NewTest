import urequests
import time
import machine

TOKEN = "7814777092:AAH6M3uRPmEVvuU2NxwO70H2bbpxKlphE6s"
URL = "https://api.telegram.org/bot" + TOKEN + "/"

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=5"
    if offset:
        url += "&offset=" + str(offset)
    res = urequests.get(url)
    data = res.json()
    res.close()
    return data

def send_message(chat_id, text):
    url = URL + "sendMessage?chat_id=" + str(chat_id) + "&text=" + text
    res = urequests.get(url)
    res.close()

def load_plugins():
    try:
        with open("plugin_list.txt", "r") as f:
            plugins = f.read().splitlines()
            for plugin in plugins:
                name = plugin.strip()
                if name:
                    module_name = name.replace(".py", "")
                    __import__(module_name)
    except OSError:
        pass

def run():
    load_plugins()
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            if "result" in updates:
                for item in updates["result"]:
                    offset = item["update_id"] + 1
                    msg = item.get("message", {})
                    text = msg.get("text", "")
                    chat_id = msg.get("chat", {}).get("id")

                    if text == "/update":
                        send_message(chat_id, "Updating from GitHub...")
                        with open("update_flag.txt", "w") as f:
                            f.write("1")
                        machine.reset()
        except Exception as e:
            print("Error:", e)
        time.sleep(2)
