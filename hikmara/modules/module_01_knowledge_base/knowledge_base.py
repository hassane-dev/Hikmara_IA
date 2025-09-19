# hikmara/modules/module_01_knowledge_base/knowledge_base.py
import sqlite3
import os

class KnowledgeBase:
    """
    Gère la base de connaissances locale de Hikmara, stockée dans une base de données SQLite.
    """
    def __init__(self, db_path="hikmara_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_name TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de l'initialisation de la DB: {e}")

    def add_knowledge(self, concept_name: str, content: str, source: str = None) -> int:
        if not self.conn: return None
        sql = "INSERT INTO knowledge (concept_name, content, source) VALUES (?, ?, ?)"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name, content, source))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de l'ajout de connaissance: {e}")
            return None

    def get_knowledge(self, concept_name: str) -> dict:
        if not self.conn: return None
        sql = "SELECT * FROM knowledge WHERE concept_name = ?"
        try:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération de connaissance: {e}")
            return None

    def update_knowledge(self, concept_name: str, new_content: str) -> bool:
        if not self.conn: return False
        sql = "UPDATE knowledge SET content = ? WHERE concept_name = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (new_content, concept_name))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la mise à jour de connaissance: {e}")
            return False

    def delete_knowledge(self, concept_name: str) -> bool:
        if not self.conn: return False
        sql = "DELETE FROM knowledge WHERE concept_name = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression de connaissance: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
