import json
import uuid
from datetime import datetime

DATA_FILE = 'users.json'

def load_users():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def add_user(user):
    users = load_users()
    # Ensure new user has all expected fields, even if empty
    user_template = {
        'id': str(uuid.uuid4()),
        'name': '',
        'email': '',
        'phone': '',
        'city': '',
        'created_at': datetime.now().isoformat()
    }
    # Update template with provided user data
    user_template.update(user)
    users.append(user_template)
    save_users(users)
    return True

def get_user(user_id=None, name=None):
    users = load_users()
    if user_id:
        for user in users:
            if user.get('id') == user_id:
                return user
    if name:
        for user in users:
            if user.get('name').lower() == name.lower():
                return user
    return None

def update_user(user_id, new_data):
    users = load_users()
    for i, user in enumerate(users):
        if user.get('id') == user_id:
            users[i].update(new_data)
            save_users(users)
            return True
    return False

def delete_user(user_id):
    users = load_users()
    initial_len = len(users)
    users = [user for user in users if user.get('id') != user_id]
    if len(users) < initial_len:
        save_users(users)
        return True
    return False

def list_users():
    return load_users()


