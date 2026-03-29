import json
import random
import os
from typing import Dict, Any, Tuple

class SmartInboxEnv:
    def __init__(self, task: str = "hard", data_path: str = "data/emails.json"):
        self.task = task
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file {data_path} not found. Ensure you generate it first.")
        with open(data_path, "r") as f:
            self.all_emails = json.load(f)
        self.emails = []
        self.current_idx = 0
        self.total_reward = 0.0

    def reset(self) -> Dict[str, Any]:
        # Triage 10 realistic emails per episode
        random.seed(42) # For deterministic baseline testing
        shuffled = list(self.all_emails)
        random.shuffle(shuffled)
        self.emails = shuffled[:10] 
        self.current_idx = 0
        self.total_reward = 0.0
        return self.state()

    def get_min_max_rewards(self) -> Tuple[float, float]:
        max_r = 0.0
        min_r = 0.0
        for email in self.emails:
            # Classification
            max_r += 2.0
            min_r -= 2.0
            
            if self.task in ["medium", "hard"]:
                if email["urgency"] == "high":
                    max_r += 3.0
                    min_r -= 3.0
                else:
                    max_r += 1.0
                    min_r -= 1.0
            
            if self.task == "hard":
                max_r += 2.0
                min_r -= 1.0
                
        return min_r, max_r

    def state(self) -> Dict[str, Any]:
        if self.current_idx >= len(self.emails):
            return {
                "done": True, 
                "email": None,
                "left_in_inbox": 0
            }
        email = self.emails[self.current_idx]
        return {
            "done": False,
            "email": {
                "id": email["id"],
                "subject": email["subject"],
                "body": email["body"]
            },
            "left_in_inbox": len(self.emails) - self.current_idx
        }

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        from server.grader import Grader
        grader = Grader(self.task)
        
        if self.current_idx >= len(self.emails):
            return self.state(), 0.0, True, {"msg": "Episode already done."}
        
        email = self.emails[self.current_idx]
        reward, details = grader.grade_step(email, action)
        
        self.total_reward += reward
        self.current_idx += 1
        
        done = self.current_idx >= len(self.emails)
        return self.state(), reward, done, {"details": details}
