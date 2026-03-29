from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os

from server.env import SmartInboxEnv
from server.grader import Grader

app = FastAPI(title="Smart Inbox OpenEnv")

# State to keep track of env instance
env_instance = None
grader_instance = None

class ResetRequest(BaseModel):
    task: str = "hard"

class ActionRequest(BaseModel):
    action: Dict[str, Any]

@app.post("/reset")
def reset(req: ResetRequest):
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

@app.post("/step")
def step(req: ActionRequest):
    global env_instance, grader_instance
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    state, reward, done, info = env_instance.step(req.action)
    
    # Calculate final score if done
    score = None
    if done:
        min_r, max_r = env_instance.get_min_max_rewards()
        score = grader_instance.calculate_final_score(env_instance.total_reward, max_r, min_r)
        info["final_score"] = score
        info["total_reward"] = env_instance.total_reward
        
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Environment not initialized.")
    return {"state": env_instance.state()}
