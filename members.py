
import json
import os

FILE = "members.json"

CATEGORIES = {
    "video_star": "⭐ Video Star",
    "admin": "🔵 Roblox Admin"
}


def load_members():
    if not os.path.exists(FILE):
        return {
            "video_star": [],
            "admin": []
        }

    with open(FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_members(data):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def add_member(category, username, user_id):
    if category not in CATEGORIES:
        raise ValueError("Unknown category")

    data = load_members()

    member = {
        "username": username,
        "user_id": int(user_id)
    }

    if member not in data[category]:
        data[category].append(member)

    save_members(data)


def get_members(category):
    if category not in CATEGORIES:
        return []

    return load_members()[category]


def get_all_members():
    data = load_members()

    return {
        category: len(data[category])
        for category in CATEGORIES
    }
  
