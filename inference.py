import requests

BASE_URL = "https://premchand45-smart-inbox-final.hf.space"

def run_test():
    # Step 1: Reset environment
    reset_res = requests.post(f"{BASE_URL}/reset", json={"task": "hard"})
    print("RESET:", reset_res.status_code, reset_res.json())

    # Step 2: Take a sample action
    action = {
        "action": {
            "category": "billing",
            "urgency": "high",
            "response": "We are checking your issue."
        }
    }

    step_res = requests.post(f"{BASE_URL}/step", json=action)
    print("STEP:", step_res.status_code, step_res.json())


if __name__ == "__main__":
    run_test
