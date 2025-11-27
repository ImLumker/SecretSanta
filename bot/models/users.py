import json
from pathlib import Path

PRODUCTS_PATH = Path("bot/data/users.json")

def get_all_users():
    if PRODUCTS_PATH.exists():
        with open(PRODUCTS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def get_userid_gives_gift_to(user_id):
    all_users = get_all_users()
    for user in all_users:
        if user["user_id"] == user_id:
            return user["gives_gift_to"]
    return None

def save_users(users):
    with open(PRODUCTS_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

def find_user(user_id):
    all_users = get_all_users()
    for user in all_users:
        if user["user_id"] == user_id:
            return user
    return None

def delete_user(user_id):
    all_users = [user for user in get_all_users() if int(user["user_id"]) != int(user_id)]
    save_users(all_users)