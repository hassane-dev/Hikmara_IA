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
            # S'assurer que le répertoire parent existe
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
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
            # print(f"Base de données initialisée avec succès à '{self.db_path}'")
        except sqlite3.Error as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")

    def add_knowledge(self, concept_name: str, content: str, source: str = None) -> int:
        """
        Ajoute une nouvelle connaissance à la base de données.
        """
        if not self.conn: return None
        sql = "INSERT INTO knowledge (concept_name, content, source) VALUES (?, ?, ?)"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name, content, source))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # print(f"Erreur: Le concept '{concept_name}' existe déjà.")
            return None
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de connaissance: {e}")
            return None

    def get_knowledge(self, concept_name: str) -> dict:
        """
        Récupère une connaissance par son nom.
        """
        if not self.conn: return None
        sql = "SELECT * FROM knowledge WHERE concept_name = ?"
        try:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de connaissance: {e}")
            return None

    def update_knowledge(self, concept_name: str, new_content: str) -> bool:
        """
        Met à jour le contenu d'une connaissance existante.
        """
        if not self.conn: return False
        sql = "UPDATE knowledge SET content = ? WHERE concept_name = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (new_content, concept_name))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de connaissance: {e}")
            return False

    def delete_knowledge(self, concept_name: str) -> bool:
        """
        Supprime une connaissance de la base de données.
        """
        if not self.conn: return False
        sql = "DELETE FROM knowledge WHERE concept_name = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (concept_name,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de connaissance: {e}")
            return False

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            # print("Connexion à la base de données fermée.")
