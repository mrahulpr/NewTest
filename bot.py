import utime
import urequests
import gc

def run(token, owner_id):
    import echo_plugin
    base_url = f"https://api.telegram.org/bot{token}"
    offset = 0
    print(f"Bot started by owner: {owner_id}")
    
    while True:
        try:
            url = f"{base_url}/getUpdates?offset={offset}&timeout=10"
            res = urequests.get(url)
            
            if res.status_code == 200:
                data = res.json()
                res.close()
                
                if "result" in data:
                    for update in data["result"]:
                        offset = update["update_id"] + 1
                        echo_plugin.handle_update(update, base_url)
            else:
                res.close()
        except Exception as e:
            print(f"Loop error: {e}")
            
        gc.collect()
        utime.sleep(2)
