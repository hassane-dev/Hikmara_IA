# hikmara/controller/main_controller.py
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase

class MainController:
    """
    Le contrôleur principal qui orchestre les différents modules de Hikmara.
    """
    def __init__(self):
        """
        Initialise le contrôleur principal et ses modules.
        """
        db_full_path = "hikmara/model/hikmara_kb.db"
        self.knowledge_base = KnowledgeBase(db_path=db_full_path)
        print("Controller initialisé. Module KnowledgeBase chargé.")

    def start(self):
        """
        Démarre la boucle principale de l'application.
        """
        print("Hikmara démarré. En attente de commandes...")
        # La future logique de l'application viendra ici.
        # Pour l'instant, l'application se terminera après le démarrage.
        pass

    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        print("Arrêt de Hikmara...")
        self.knowledge_base.close()
        print("Modules arrêtés proprement.")
