import json
import os

class Memory:
    def __init__(self, filename="memory.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def add(self, role, message):
        history = self.get_history()
        history.append({"role": role, "message": message})
        with open(self.filename, "w") as f:
            json.dump(history, f, indent=2)

    def get_history(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def clear(self):
        with open(self.filename, "w") as f:
            json.dump([], f)
