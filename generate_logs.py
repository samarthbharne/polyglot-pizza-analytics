import pymongo
import random
from datetime import datetime, timedelta

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pizza_analytics_db"]
logs_collection = db["web_logs"]

# Possible actions and pizza types
actions = ['view_item', 'add_to_cart', 'remove_from_cart', 'click_review', 'apply_coupon']
pizzas = ['Margherita', 'Pepperoni', 'BBQ Chicken', 'Veggie Supreme', 'Hawaiian', 'Meat Lovers']

print("🚀 Starting Data Generation...")

log_entries = []
# Generating 5,000 logs for our 2 users (IDs 1 and 2 from your SQL table)
for _ in range(5000):
    user_id = random.choice([1, 2])
    action = random.choice(actions)
    pizza = random.choice(pizzas)
    
    # Random timestamp within the last 7 days
    random_days = random.randint(0, 7)
    random_hours = random.randint(0, 23)
    timestamp = datetime.now() - timedelta(days=random_days, hours=random_hours)

    entry = {
        "user_id": user_id,
        "action": action,
        "item_name": pizza,
        "timestamp": timestamp,
        "metadata": {
            "device": random.choice(["Mobile", "Desktop", "Tablet"]),
            "session_id": random.randint(10000, 99999)
        }
    }
    log_entries.append(entry)

# Insert everything into MongoDB at once for speed
logs_collection.insert_many(log_entries)
print(f"✅ Success! 5,000 logs inserted into MongoDB collection: 'web_logs'")