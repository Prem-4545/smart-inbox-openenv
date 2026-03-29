import requests

# ✅ IMPORTANT: Your Hugging Face Space URL
BASE_URL = "https://premchand45-smart-inbox-final.hf.space"


def run():
    print("Running inference...")  # cache break + debug

    try:
        # 🔹 Step 1: Reset environment
        reset_res = requests.post(
            f"{BASE_URL}/reset",
            json={"task": "hard"}
        )
        print("RESET STATUS:", reset_res.status_code)
        print("RESET RESPONSE:", reset_res.text)

        # 🔹 Step 2: Send action
        action = {
            "action": {
                "category": "billing",
                "urgency": "high",
                "response": "We are checking your issue."
            }
        }

        step_res = requests.post(
            f"{BASE_URL}/step",
            json=action
        )
        print("STEP STATUS:", step_res.status_code)
        print("STEP RESPONSE:", step_res.text)

    except Exception as e:
        print("ERROR:", str(e))


if __name__ == "__main__":
    run()
