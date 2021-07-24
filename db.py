import sqlite3
import config


class DatabaseConnection:
    def __init__(self, path=config.database_path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        # TODO: Check if this data types are correct
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
            discord_id int PRIMARY KEY,
            codingame_id text NOT NULL
        );''')

    # Get a linked codingame id from a discord id in the database
    # Returns None if the user is not registered
    def get_codingame_id(self, discord_id: int) -> str:
        self.cur.execute('''SELECT codingame_id FROM users WHERE discord_id = ?''', (discord_id,))
        result = self.cur.fetchone()
        if result is None:
            return None
        return result[0]

    # Register a new user in the database
    # Returns True if the user was registered
    def link(self, discord_id: int, codingame_id: str) -> bool:
        self.cur.execute('''INSERT INTO users (discord_id, codingame_id) VALUES (?, ?)''', (discord_id, codingame_id))
        self.con.commit()
        return True

    # Remove a user from the database
    # Returns True if the user was removed
    def unlink(self, discord_id: int) -> bool:
        self.cur.execute('''DELETE FROM users WHERE discord_id = ?''', (discord_id,))
        self.con.commit()
        return True

    def is_linked(self, discord_id: int) -> bool:
        self.cur.execute('''SELECT discord_id FROM users WHERE discord_id = ?''', (discord_id,))
        result = self.cur.fetchone()
        if result is None:
            return False
        return True


    def __del__(self):
        self.con.close()


# TODO: Make this configurable
db = DatabaseConnection()
