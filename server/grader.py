class Grader:
    def __init__(self, task: str):
        self.task = task
    
    def grade_step(self, email: dict, action: dict):
        reward = 0.0
        details = {}
        
        # Classification (Easy, Medium, Hard)
        pred_cat = action.get("category", "").lower()
        if pred_cat == email["category"].lower():
            reward += 2.0
            details["category_correct"] = True
        else:
            reward -= 2.0
            details["category_correct"] = False
            
        # Urgency (Medium, Hard)
        if self.task in ["medium", "hard"]:
            pred_urgency = action.get("urgency", "").lower()
            actual_urgency = email["urgency"].lower()
            
            if actual_urgency == "high":
                if pred_urgency == "high":
                    reward += 3.0
                    details["high_urgency_correct"] = True
                else:
                    reward -= 3.0
                    details["high_urgency_correct"] = False
            else:
                # Partial progress / correct for non-high urgency
                if pred_urgency == actual_urgency:
                    reward += 1.0
                    details["urgency_correct"] = True
                else:
                    reward -= 1.0
                    details["urgency_correct"] = False

        # Action Decision (Hard)
        if self.task == "hard":
            pred_action = action.get("action", "").lower()
            if pred_action == email["expected_action"].lower():
                reward += 2.0
                details["action_correct"] = True
            else:
                reward -= 1.0
                details["action_correct"] = False
                
        return reward, details

    def calculate_final_score(self, total_reward: float, max_reward: float, min_reward: float) -> float:
        """Returns a deterministic score between 0.0 and 1.0"""
        if max_reward == min_reward:
            return 0.0
        score = (total_reward - min_reward) / (max_reward - min_reward)
        return max(0.0, min(1.0, score))
