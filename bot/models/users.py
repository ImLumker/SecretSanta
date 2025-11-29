import json
from pathlib import Path

PRODUCTS_PATH = Path("bot/data/users.json")

def get_all_users(show_settings: bool = False):
    if PRODUCTS_PATH.exists():
        with open(PRODUCTS_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
            if not show_settings:
                return users[1:]
            else:
                return users
    return []

def get_info_about_gives_gift_to(user_id):
    all_users = get_all_users()
    for user in all_users:
        if user["user_id"] == user_id:
            for user_info in all_users:
                if user["gives_gift_to"] == user_info["user_id"]:
                    return user_info
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
    all_users = [get_all_users(True)[0]]
    for user in get_all_users():
        if int(user["user_id"]) != int(user_id):
            all_users.append(user)
    save_users(all_users)
