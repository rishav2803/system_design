from collections import defaultdict
from typing import List

from in_mem_db.command import BaseCommand


class InMemDB:

    def __init__(self):
        self.db = defaultdict()
        self.current_stack: List[dict] = []
        self.undo_stack: List[BaseCommand] = []

    def in_transaction(self) -> bool:
        return len(self.current_stack) > 0

    def _current_layer(self):
        if self.in_transaction():
            return self.current_stack[-1]

        return self.db

    def set(self, key, val):
        current_layer = self._current_layer()
        current_layer[key] = val

    def delete(self, key):
        current_layer = self._current_layer()
        current_layer.pop(key)

    def get(self, key):
        for layer in reversed(self.current_stack):
            if key in layer:
                return layer[key]
        return self.db.get(key)

    # TRANSACTIONS methods

    def begin(self):
        self.current_stack.append({})

    def commit(self):
        if not self.in_transaction():
            raise ValueError("Currently no transaction in progress to COMMIT")

        current_layer = self.current_stack.pop()
        target_layer = self._current_layer()

        for k, v in current_layer.items():
            target_layer[k] = v

    def rollback(self):
        if not self.in_transaction():
            raise ValueError("Currently no transaction in progress to ROLLBACK")

        self.current_stack.pop()
