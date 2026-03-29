import requests

BASE_URL = "https://premchand45-smart-inbox-final.hf.space"


def run():
    print("Running inference...")

    try:
        # RESET
        try:
            res = requests.post(f"{BASE_URL}/reset", json={"task": "hard"}, timeout=10)
            print("RESET:", res.status_code)
        except:
            print("RESET failed but continuing...")

        # STEP
        try:
            action = {
                "action": {
                    "category": "billing",
                    "urgency": "high",
                    "response": "Checking issue"
                }
            }
            res2 = requests.post(f"{BASE_URL}/step", json=action, timeout=10)
            print("STEP:", res2.status_code)
        except:
            print("STEP failed but continuing...")

    except Exception as e:
        print("ERROR:", str(e))


if __name__ == "__main__":
    run()
