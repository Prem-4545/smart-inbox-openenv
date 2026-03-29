from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any
import os

from server.env import SmartInboxEnv
from server.grader import Grader

app = FastAPI(title="Smart Inbox OpenEnv")

# Global state
env_instance = None
grader_instance = None


# ✅ ROOT (VERY IMPORTANT)
@app.get("/")
def root():
    return {"message": "Smart Inbox Running 🚀"}


# ✅ Reset Request (make optional)
class ResetRequest(BaseModel):
    task: str = "hard"


# ✅ Step Request
class ActionRequest(BaseModel):
    action: Dict[str, Any]


# ✅ RESET (FIXED)
@app.post("/reset")
def reset(req: ResetRequest = Body(default=ResetRequest())):
    global env_instance, grader_instance

    if req.task not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=400, detail="Invalid task")

    data_path = os.environ.get("DATA_PATH", "data/emails.json")

    try:
        env_instance = SmartInboxEnv(task=req.task, data_path=data_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    grader_instance = Grader(task=req.task)

    state = env_instance.reset()

    return {"state": state}


# ✅ STEP
@app.post("/step")
def step(req: ActionRequest = Body(...)):
    global env_instance, grader_instance

    if env_instance is None:
        raise HTTPException(status_code=400, detail="Call /reset first")

    state, reward, done, info = env_instance.step(req.action)

    if done:
        min_r, max_r = env_instance.get_min_max_rewards()
        score = grader_instance.calculate_final_score(
            env_instance.total_reward, max_r, min_r
        )
        info["final_score"] = score
        info["total_reward"] = env_instance.total_reward

    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }


# ✅ OPTIONAL (OK)
@app.get("/state")
def get_state():
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Not initialized")
    return {"state": env_instance.state()}
    def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
