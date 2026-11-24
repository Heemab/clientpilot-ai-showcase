from src.database.database import Database


class Schema:

    def __init__(self):
        self.db = Database()

    def create_tables(self):
        connection = self.db.connect()
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT,
            source TEXT,
            url TEXT,
            budget TEXT,
            status TEXT DEFAULT 'New',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        connection.commit()
        connection.close()

        print("✅ Database schema created successfully.")