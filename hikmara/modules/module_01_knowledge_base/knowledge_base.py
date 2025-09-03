# hikmara/modules/module_01_knowledge_base/knowledge_base.py
import sqlite3
import os

class KnowledgeBase:
    """
    Gère la base de connaissances locale de Hikmara, stockée dans une base de données SQLite.
    """
    def __init__(self, db_path="hikmara_knowledge.db"):
        """
        Initialise la base de connaissances.

        :param db_path: Chemin vers le fichier de la base de données SQLite.
        """
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        """
        Initialise la base de données et crée les tables si elles n'existent pas.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            # Création d'une table exemple pour les "connaissances"
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
            print(f"Base de données initialisée avec succès à '{self.db_path}'")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Connexion à la base de données fermée.")
