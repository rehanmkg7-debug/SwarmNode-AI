import time
import random
import requests

MASTER_URL = "http://127.0.0.1:5000"
# ورکر کے لیے یونیک آئی ڈی (مثلاً Worker-Mobile-1)
WORKER_ID = f"Node-Android-{random.randint(100, 999)}"

def run_text_ai(text):
    words = text.split()
    word_count = len(words)
    negative_words = ["error", "failed", "poor", "slowed", "timeout"]
    sentiment = "POSITIVE"
    for word in words:
        if word.lower().strip(".,!") in negative_words:
            sentiment = "NEGATIVE"
            break
    time.sleep(1.5)
    return {"word_count": word_count, "sentiment": sentiment}

def run_image_processing(image_data_str):
    # سیمولیٹنگ امیج فائل اینالیسز اور کمپریشن
    size_bytes = len(image_data_str) * 128
    compression_ratio = "65%"
    time.sleep(2)
    return {"size_bytes": size_bytes, "compression_ratio": compression_ratio}

def start_node_worker():
    print(f"🚀 SwarmNode Worker Active! Registered ID: [{WORKER_ID}]")
    
    while True:
        try:
            response = requests.get(f"{MASTER_URL}/get_task", timeout=5)
            res_data = response.json()
            
            if res_data.get("status") == "available":
                task = res_data["task"]
                task_id = task["task_id"]
                task_type = task["type"]
                raw_data = task["data"]
                
                print(f"[+] Task Received! ID: {task_id} | Type: {task_type}")
                
                if task_type == "text":
                    processed_res = run_text_ai(raw_data)
                else:
                    processed_res = run_image_processing(raw_data)
                
                payload = {
                    "task_id": task_id,
                    "worker_id": WORKER_ID,
                    "type": task_type,
                    "result": processed_res
                }
                
                submit_res = requests.post(f"{MASTER_URL}/submit_result", json=payload, timeout=5)
                if submit_res.json().get("status") == "success":
                    print(f"[💰] Task {task_id} submitted! +10 SWARM Tokens earned by {WORKER_ID}\n")
            else:
                print("[💤] No pending tasks. Waiting...")
                
        except Exception as e:
            print(f"[❌] Connection Error: {e}")
            
        time.sleep(4)

if __name__ == "__main__":
    start_node_worker()

