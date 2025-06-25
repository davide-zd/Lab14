from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ordine:
    id: int

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"id: {self.id}"