# hikmara/controller/main_controller.py
import os
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner
from hikmara.modules.module_03_raw_learning.raw_learning import RawLearner
from hikmara.modules.module_04_nlp.nlp_processor import NLPProcessor
from hikmara.modules.module_05_code_generation.code_generator import CodeGenerator
from hikmara.modules.module_06_code_execution.code_executor import CodeExecutor
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
        self.code_generator = CodeGenerator()
        self.code_executor = CodeExecutor() # Instanciation du Module 6
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

        self.view.display_nlp_result(nlp_result)

        if intent == "create":
            self._handle_creation_intent(nlp_result)
        elif intent == "execute":
            self._handle_execution_intent(nlp_result)
        elif intent == "unknown":
            self.view.display_message("-> Je n'ai pas compris l'action principale. Pouvez-vous reformuler ?")
        else:
            self.view.display_message(f"-> L'action '{intent}' n'est pas encore prise en charge.")

    def _handle_creation_intent(self, nlp_result: dict):
        """
        Gère spécifiquement l'intention de 'créer'.
        """
        project_type = nlp_result.get("project_type")
        project_name = nlp_result.get("project_name")

        if not project_name:
            self.view.display_message("-> Vous voulez créer quelque chose, mais je n'ai pas compris le nom du projet.")
            return

        if project_type == "python":
            success, message = self.code_generator.create_python_project(project_name)
        elif project_type == "web":
            success, message = self.code_generator.create_web_project(project_name)
        else:
            self.view.display_message(f"-> Je ne sais pas comment créer un projet de type '{project_type}'. Je vais créer un projet web par défaut.")
            success, message = self.code_generator.create_web_project(project_name)

        self.view.display_message(f"-> {message}")

    def _handle_execution_intent(self, nlp_result: dict):
        """
        Gère spécifiquement l'intention d'exécuter'.
        """
        project_name = nlp_result.get("project_name")
        if not project_name:
            self.view.display_message("-> Vous voulez exécuter un projet, mais je n'ai pas compris lequel.")
            return

        # On suppose que le script principal s'appelle 'main.py'
        project_path = os.path.join(self.code_generator.base_path, project_name)
        script_path = os.path.join(project_path, "main.py")

        if not os.path.exists(script_path):
            self.view.display_message(f"-> Erreur: Impossible de trouver le script principal pour le projet '{project_name}'.")
            return

        self.view.display_message(f"-> Lancement du script pour le projet '{project_name}'...")
        success, stdout, stderr = self.code_executor.execute_python_script(script_path)

        # Le contrôleur demande à la vue d'afficher le résultat de l'exécution
        self.view.display_execution_result(success, stdout, stderr)


    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        self.knowledge_base.close()
        self.view.display_shutdown_message()
