import json
import os
from typing import Dict, Any

class DataStorage:
    def __init__(self, file_path: str = "user_data.json"):
        self.file_path = file_path
        self.data: Dict[int, Dict[str, Any]] = self.load_data()

    def load_data(self) -> Dict[int, Dict[str, Any]]:
        """Load user data from JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid JSON file. Starting with empty data.")
        return {}

    def save_data(self) -> None:
        """Save user data to JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data to JSON: {e}")

    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get user data by user_id, initialize if not exists."""
        if user_id not in self.data:
            self.data[user_id] = {}
        return self.data[user_id]

    def set_user_data(self, user_id: int, key: str, value: Any) -> None:
        """Set a specific key-value pair for a user and save."""
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id][key] = value
        self.save_data()

    def clear_user_data(self, user_id: int) -> None:
        """Clear user data for a specific user and save."""
        if user_id in self.data:
            del self.data[user_id]
            self.save_data()