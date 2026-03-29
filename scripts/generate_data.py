import json
import random
import os

categories = ["billing", "technical", "spam", "general"]
urgencies = ["low", "medium", "high"]

actions_map = {
    "billing": ["refund", "invoice_resend", "escalate_finance"],
    "technical": ["reply_faq", "forward_to_it", "escalate_eng"],
    "spam": ["ignore", "block_sender"],
    "general": ["reply_standard", "assign_to_human"]
}

random.seed(42) # Deterministic generation for reproducibility

emails = []
for i in range(1, 41): # Generate 40 emails
    cat = random.choice(categories)
    urg = random.choice(urgencies)
    action = random.choice(actions_map[cat])
    
    subject = f"{cat.capitalize()} issue {i}"
    body = f"This is an email regarding {cat}. The priority feels {urg}. Please handle it via {action} if possible."
    
    if cat == "billing":
        body = "My credit card was charged twice!" if urg == "high" else ("Can I get a copy of my invoice? I need to know the charge amount." if urg == "medium" else "Just a general billing question.")
        subject = "URGENT CHARGE" if urg == "high" else "Invoice request"
    elif cat == "technical":
        body = "The whole system is down! We cannot work." if urg == "high" else ("How do I reset my password? I forgot it." if urg == "medium" else "A minor bug report.")
        subject = "System Outage" if urg == "high" else "Password help"
    elif cat == "spam":
        body = "You won a million dollars! Click here to claim your prize!"
        subject = "WINNER WINNER"
        urg = "low" # usually spam is low urgency
        action = "ignore" # Force action to ignore for spam baseline
    elif cat == "general":
        body = "I have a general question about your services."
        subject = "Question about services"

    emails.append({
        "id": f"email_{i:03d}",
        "subject": subject,
        "body": body,
        "category": cat,
        "urgency": urg,
        "expected_action": action
    })

os.makedirs("data", exist_ok=True)
with open("data/emails.json", "w") as f:
    json.dump(emails, f, indent=2)

print(f"Generated {len(emails)} emails in data/emails.json")
