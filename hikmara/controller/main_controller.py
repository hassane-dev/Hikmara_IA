# hikmara/controller/main_controller.py
import os
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner
from hikmara.modules.module_03_raw_learning.raw_learning import RawLearner
from hikmara.modules.module_04_nlp.nlp_processor import NLPProcessor
from hikmara.view.terminal_view import TerminalView

class MainController:
    """
    Le contrôleur principal qui orchestre les différents modules de Hikmara.
    """
    def __init__(self):
        """
        Initialise le contrôleur principal, la vue et les modules.
        """
        db_full_path = "hikmara/model/hikmara_kb.db"

        # Initialisation de la vue
        self.view = TerminalView()

        # Initialisation des modules dans l'ordre de dépendance
        self.view.display_message("Initialisation du contrôleur et des modules...")
        self.knowledge_base = KnowledgeBase(db_path=db_full_path)
        self.structured_learner = StructuredLearner(knowledge_base=self.knowledge_base)
        self.raw_learner = RawLearner(structured_learner=self.structured_learner)
        self.nlp_processor = NLPProcessor()
        self.view.display_message("Modules initialisés.")

    def start(self):
        """
        Démarre la boucle principale de l'application en utilisant la vue.
        """
        self.view.display_welcome()

        while True:
            command = self.view.get_command()

            if command.lower().strip() in ["quitter", "exit", "stop"]:
                break

            if not command.strip():
                continue

            # Le contrôleur traite la commande via le module NLP
            nlp_result = self.nlp_processor.process_command(command)

            # Le contrôleur demande à la vue d'afficher le résultat
            self.view.display_nlp_result(nlp_result)


    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        self.knowledge_base.close()
        self.view.display_shutdown_message()
