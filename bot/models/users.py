import json
from pathlib import Path

PRODUCTS_PATH = Path("bot/data/users.json")

def get_users():
    if PRODUCTS_PATH.exists():
        with open(PRODUCTS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def get_userid_gives_gift_to(user_id):
    all_users = get_users()
    for user in all_users:
        if user["user_id"] == user_id:
            return user["gives_gift_to"]
    return None