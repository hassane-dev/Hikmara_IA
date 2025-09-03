# hikmara/controller/main_controller.py
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase

class MainController:
    """
    Le contrôleur principal qui orchestre les différents modules de Hikmara.
    Il gère le flux de données et la communication entre la vue, le modèle,
    et tous les modules fonctionnels.
    """
    def __init__(self):
        """
        Initialise le contrôleur principal et ses modules.
        """
        # Le chemin de la DB est placé dans le dossier model, ce qui est plus logique
        db_full_path = "hikmara/model/hikmara_kb.db"
        self.knowledge_base = KnowledgeBase(db_path=db_full_path)

    def start(self):
        """
        Démarre la boucle principale de l'application.
        """
        print("Hikmara Main Controller started.")
        # La logique principale de coordination des modules viendra ici
        print("Module de base de connaissances chargé.")

    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        print("Arrêt des modules de Hikmara...")
        self.knowledge_base.close()
