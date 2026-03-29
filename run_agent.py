import requests
import time
import os

BASE_URL = os.environ.get("OPENENV_URL", "http://localhost:7860")

def run_task(task_level):
    print(f"\n--- Running Baseline Agent for Task: {task_level.upper()} ---")
    try:
        resp = requests.post(f"{BASE_URL}/reset", json={"task": task_level})
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to environment: {e}")
        return
        
    state = resp.json()["state"]
    done = False
    
    while not done:
        if state.get("done"):
            break
            
        email = state["email"]
        text = (email["subject"] + " " + email["body"]).lower()
        
        # Parse basic heuristics
        category = "general"
        if "charge" in text or "invoice" in text or "billing" in text:
            category = "billing"
        elif "down" in text or "password" in text or "outage" in text:
            category = "technical"
        elif "winner" in text or "prize" in text or "million" in text:
            category = "spam"
            
        urgency = "low"
        if "urgent" in text or "down" in text:
            urgency = "high"
        elif "invoice" in text:
            urgency = "medium"
            
        action = "reply_standard"
        if category == "billing" and urgency == "high":
            action = "refund"
        elif category == "billing":
            action = "invoice_resend"
        elif category == "technical" and urgency == "high":
            action = "escalate_eng"
        elif category == "technical":
            action = "reply_faq"
        elif category == "spam":
            action = "ignore"
            
        action_payload = {"category": category}
        if task_level in ["medium", "hard"]:
            action_payload["urgency"] = urgency
        if task_level == "hard":
            action_payload["action"] = action
            
        print(f"Agent Processing {email['id']} -> Action payload: {action_payload}")
        
        resp = requests.post(f"{BASE_URL}/step", json={"action": action_payload})
        result = resp.json()
        
        state = result["state"]
        done = result["done"]
        reward = result["reward"]
        print(f"Step Reward: {reward}")
        
        if done:
            info = result["info"]
            print(f"Task {task_level.upper()} Completed!")
            print(f"Total Cumulative Reward: {info.get('total_reward')}")
            print(f"Final Normalized Score (0.0 - 1.0): {info.get('final_score')}")

if __name__ == "__main__":
    print("Waiting for server to be ready...")
    time.sleep(2) # Give server a moment to start if run concurrently
    for level in ["easy", "medium", "hard"]:
        run_task(level)
        time.sleep(1)
