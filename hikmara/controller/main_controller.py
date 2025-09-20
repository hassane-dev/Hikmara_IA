# hikmara/controller/main_controller.py
import os
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner
from hikmara.modules.module_03_raw_learning.raw_learning import RawLearner

class MainController:
    """
    Le contrôleur principal qui orchestre les différents modules de Hikmara.
    """
    def __init__(self):
        """
        Initialise le contrôleur principal et ses modules.
        """
        db_full_path = "hikmara/model/hikmara_kb.db"

        # Initialisation des modules dans l'ordre de dépendance
        self.knowledge_base = KnowledgeBase(db_path=db_full_path)
        self.structured_learner = StructuredLearner(knowledge_base=self.knowledge_base)
        self.raw_learner = RawLearner(structured_learner=self.structured_learner)

    def start(self):
        """
        Démarre la boucle principale de l'application.
        """
        print("Hikmara Controller: Application démarrée.")

    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        self.knowledge_base.close()
        print("Hikmara Controller: Application arrêtée.")
