# hikmara/controller/main_controller.py
import os
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner
from hikmara.modules.module_03_raw_learning.raw_learning import RawLearner
from hikmara.modules.module_04_nlp.nlp_processor import NLPProcessor
from hikmara.modules.module_05_code_generation.code_generator import CodeGenerator
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
        self.code_generator = CodeGenerator() # Instanciation du Module 5
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

            # Le contrôleur interprète l'intention et agit en conséquence
            self._process_intent(nlp_result)

    def _process_intent(self, nlp_result: dict):
        """
        Analyse l'intention et les entités pour déclencher les actions appropriées.
        """
        intent = nlp_result.get("intent")
        entities = nlp_result.get("entities")

        self.view.display_nlp_result(nlp_result)

        if intent == "créer":
            self._handle_creation_intent(entities)
        elif intent == "unknown":
            self.view.display_message("-> Je n'ai pas compris l'action principale. Pouvez-vous reformuler ?")
        else:
            self.view.display_message(f"-> L'action '{intent}' n'est pas encore prise en charge.")

    def _handle_creation_intent(self, entities: dict):
        """
        Gère spécifiquement l'intention de 'créer'.
        Pour l'instant, ne gère que la création de projet web.
        """
        # Simplification: on prend la première entité comme nom de projet.
        # Idéalement, il faudrait analyser le type de projet demandé.
        project_name = next(iter(entities.values()), None)

        if not project_name:
            self.view.display_message("-> Vous voulez créer quelque chose, mais je n'ai pas compris quoi. Pouvez-vous préciser le nom ?")
            return

        # Appel du CodeGenerator
        success, message = self.code_generator.create_web_project(project_name)

        # Affichage du résultat via la vue
        self.view.display_message(f"-> {message}")


    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        self.knowledge_base.close()
        self.view.display_shutdown_message()
