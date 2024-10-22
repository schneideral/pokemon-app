import sqlite3
import json

class PokeSchema:
    def __init__(self):
        self.conn = sqlite3.connect('pokemon.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemons (
                id INTEGER PRIMARY KEY,
                pokemon TEXT,
                moves TEXT
            )
        ''')
        self.conn.commit()

    def add_pokemon(self, id, data):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO pokemons (id, pokemon, moves) VALUES (?, ?, ?)", (id, data['pokemon'], json.dumps(data['moves'])))
        self.conn.commit()

    def get_current_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM pokemons")
        current_id = cursor.fetchall()
        return current_id[0][0]

    def get_all_mons(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pokemons")
        rows = cursor.fetchall()
        mons = []
        for row in rows:
            mons.append({
                'id': row[0],
                'pokemon': row[1],
                'moves': row[2],
            })
        return mons

    def get_mon_by_id(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pokemons WHERE id=?", (item_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'pokemon': row[1],
                'moves': row[2]
            }
        else:
            return {"error": "Item not found"}, 404

    def update_mon(self, item_id, data):
        cursor = self.conn.cursor()
        set_clause = ", ".join([f"{key}=?" for key in data])
        values = []
        for key in data:
            if key == 'pokemon':
                values.append(data[key])
            else:
                values.append(json.dumps(data[key]))
        values.append(item_id)
        try:
            print(set_clause)
            print(tuple(values))
            cursor.execute(f"UPDATE pokemons SET {set_clause} WHERE id=?", tuple(values))
            self.conn.commit()
            return self.get_mon_by_id(item_id)
        except Exception as e:
            return {"error": f"Failed to update pokemon: {str(e)}"}, 500

    def delete_mon(self, item_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM pokemons WHERE id = ?", (item_id,))
            cursor.execute("UPDATE pokemons SET id = id - 1 WHERE id > ?", (item_id,))
            self.conn.commit()
            return "", 204
        except Exception as e:
            return {"error": f"Failed to delete pokemon: {str(e)}"}, 500
