import requests

BASE_URL = "https://premchand45-smart-inbox-final.hf.space"

def run():
    try:
        res = requests.post(f"{BASE_URL}/reset", json={"task": "hard"})
        print("RESET:", res.status_code, res.text)

        action = {
            "action": {
                "category": "billing",
                "urgency": "high",
                "response": "We are checking your issue."
            }
        }

        res2 = requests.post(f"{BASE_URL}/step", json=action)
        print("STEP:", res2.status_code, res2.text)

    except Exception as e:
        print("ERROR:", str(e))

if __name__ == "__main__":
    run()
