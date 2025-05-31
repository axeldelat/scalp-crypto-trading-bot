import json
import os
import time

class PositionManager:
    def __init__(self, state_file="positions.json"):
        self.state_file = state_file
        self.positions = self._load()

    def add_position(self, symbol, qty, price):
        self.positions.append({
            "symbol": symbol,
            "qty": qty,
            "price": price,
            "timestamp": time.time()
        })
        self._save()

    def get_open_position(self, symbol):
        for pos in self.positions:
            if pos["symbol"] == symbol:
                return pos
        return None

    def close_position(self, symbol):
        for i, pos in enumerate(self.positions):
            if pos["symbol"] == symbol:
                removed = self.positions.pop(i)
                self._save()
                return removed
        return None

    def has_position(self, symbol):
        return any(pos["symbol"] == symbol for pos in self.positions)

    def get_all_positions(self):
        return self.positions

    def _save(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.positions, f, indent=2)

    def _load(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []
