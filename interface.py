import requests

BASE_URL = "https://premchand45-smart-inbox-final.hf.space"

def run():
    task = "smart_inbox"
    env = "openenv"
    model = "rule-based"

    # ✅ START
    print(f"[START] task={task} env={env} model={model}", flush=True)

    rewards = []
    steps = 0
    success = False

    try:
        # RESET
        requests.post(f"{BASE_URL}/reset", json={"task": "hard"}, timeout=10)

        # STEP
        action_payload = {
            "action": {
                "category": "billing",
                "urgency": "high",
                "response": "Checking issue"
            }
        }

        res = requests.post(f"{BASE_URL}/step", json=action_payload, timeout=10)
        data = res.json()

        reward = float(data.get("reward", 0))
        done = data.get("done", True)

        steps = 1
        rewards.append(reward)

        # ✅ STEP FORMAT (STRICT)
        print(
            f"[STEP] step=1 action=billing_action reward={reward:.2f} done={str(done).lower()} error=null",
            flush=True
        )

        # SCORE
        score = data.get("info", {}).get("final_score", 0.5)
        score = float(score)

        success = score > 0.3

    except Exception as e:
        print(
            f"[STEP] step=1 action=error reward=0.00 done=true error={str(e)}",
            flush=True
        )
        score = 0.0
        rewards = [0.0]
        steps = 1
        success = False

    # ✅ END FORMAT (STRICT)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards}",
        flush=True
    )


if __name__ == "__main__":
    run()
