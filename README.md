# Smart Inbox OpenEnv

A complete, OpenEnv-compliant simulation environment for customer support email triage. 
This project sets up a FastAPI server to act as a realistic triage environment where agents can classify incoming emails, determine their urgency, and make actionable decisions.

## Problem Statement
Support teams often face hundreds of raw, unstructured emails daily. The goal of this environment is to provide a platform to train and score LLM or heuristic agents on triaging these emails effectively without reading them one-by-one manually. It acts as a realistic text-based environment to classify categories, measure urgency, and act.

## Architecture
- **Environment API (`server/app.py`)**: A FastAPI server that exposes standard OpenEnv endpoints (`/reset`, `/step`).
- **Core Logic (`server/env.py`)**: The `SmartInboxEnv` class that maintains the email state, samples an inbox queue, and passes actions to the grader.
- **Grader System (`server/grader.py`)**: A deterministic scoring system evaluating the reward at each step and returning a globally normalized final score between 0.0 and 1.0.
- **Dataset Generation (`scripts/generate_data.py`)**: A helper script to procedurally construct realistic support emails cleanly into `data/emails.json`.

## Tasks
The project features 3 complexity tiers:
1. **Easy**: "classify email" - Find the right department category (billing, technical, spam, general).
2. **Medium**: "classify + urgency detection" - Find the category and the level of urgency (low, medium, high).
3. **Hard**: "classify + urgency + action decision" - Find the category, rank urgency, and output a discrete action (e.g. refund, reply_faq, ignore).

## Reward System
The environment features a deterministic reward structure:
- **Correct classification**: +2 points
- **Wrong classification**: -2 points
- **High urgency accurately identified**: +3 points
- **High urgency missed/wrong**: -3 points
- **Correct non-high urgency (Partial progress)**: +1 point
- **Wrong non-high urgency**: -1 point
- **Action decision correct (Hard task)**: +2 points
- **Action decision wrong**: -1 point

The final score calculates `(total_reward - min_possible_reward) / (max_possible_reward - min_possible_reward)` capping precisely between `0.0` and `1.0`.

## How to Run

### Via Docker (Recommended)
Build and run the OpenEnv server on port `7860`:
```bash
docker build -t smart-inbox-openenv .
docker run -p 7860:7860 smart-inbox-openenv
```

### Via Local Python
Install dependencies and run standard python tooling:
```bash
pip install -r requirements.txt
python scripts/generate_data.py
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Running the Baseline Agent
Once the server is running on `localhost:7860`, open a new terminal and execute the baseline script:
```bash
python run_agent.py
```
This runs a heuristic baseline across all 3 tasks (easy, medium, hard) and outputs the final 0.0 - 1.0 deterministic score.
