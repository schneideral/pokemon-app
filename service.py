from models import PokeSchema

import json


class MonService:
    def __init__(self):
        self.schema = PokeSchema()
        current_id = self.schema.get_current_id()
        if current_id == None:
            current_id = 0
        self.next_id = current_id + 1

    def create(self, data):
        if "pokemon" not in data:
            return {"error": "No task provided"}, 400
        self.schema.add_pokemon(self.next_id, data)
        self.next_id += 1
        return data

    def list(self):
        return self.schema.get_all_mons()

    def get_by_id(self, item_id):
        try:
            item_id = int(item_id)
        except ValueError:
            return {"error": "Invalid item ID"}, 400
        return self.schema.get_mon_by_id(item_id)

    def update(self, item_id, data):
        try:
            item_id = int(item_id)
        except ValueError:
            return {"error": "Invalid item ID"}, 400
        return self.schema.update_mon(item_id, data)

    def delete(self, item_id):
        try:
            item_id = int(item_id)
        except ValueError:
            return {"error": "Invalid item ID"}, 400
        return self.schema.delete_mon(item_id)
