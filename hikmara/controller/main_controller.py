# hikmara/controller/main_controller.py
import os
import nltk
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner
from hikmara.modules.module_03_raw_learning.raw_learning import RawLearner
from hikmara.modules.module_04_nlp.nlp_processor import NLPProcessor
from hikmara.modules.module_05_code_generation.code_generator import CodeGenerator
from hikmara.modules.module_06_code_execution.code_executor import CodeExecutor
from hikmara.modules.module_07_voice_recognition.voice_recognizer import VoiceRecognizer
from hikmara.modules.module_08_voice_synthesis.voice_synthesizer import VoiceSynthesizer
from hikmara.modules.module_09_facial_recognition.facial_recognizer import FacialRecognizer
from hikmara.modules.module_10_internet_control.internet_controller import InternetController
from hikmara.modules.web_search.web_searcher import WebSearcher
from hikmara.modules.module_11_neural_network.neural_network import NeuralNetwork
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
        self.voice_synthesizer = VoiceSynthesizer()
        self.view = TerminalView(synthesizer=self.voice_synthesizer)
        self.voice_mode_enabled = False

        self.view.display_message("Initialisation du contrôleur et des modules...")
        self.internet_controller = InternetController(view=self.view) # Instanciation du Module 10
        self.knowledge_base = KnowledgeBase(db_path=db_full_path)
        self.structured_learner = StructuredLearner(knowledge_base=self.knowledge_base)
        self.raw_learner = RawLearner(structured_learner=self.structured_learner)
        self.nlp_processor = NLPProcessor(internet_controller=self.internet_controller)
        self.code_generator = CodeGenerator()
        self.code_executor = CodeExecutor()
        self.voice_recognizer = VoiceRecognizer()
        self.facial_recognizer = FacialRecognizer()
        self.web_searcher = WebSearcher()
        self.neural_network = NeuralNetwork() # Instanciation du Module 11
        # Le VoiceSynthesizer est déjà initialisé plus haut
        self.view.display_message("Modules initialisés.")

    def _ensure_dependencies(self):
        """
        S'assure que les dépendances de données (comme NLTK) sont prêtes.
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            self.view.display_message("Données NLTK ('punkt') manquantes. Tentative de téléchargement...")
            # On utilise l'internet_controller pour demander la permission
            prompt = "Les données NLTK 'punkt' sont nécessaires pour analyser le texte. Puis-je les télécharger ?"
            if self.internet_controller.request_permission(prompt):
                try:
                    nltk.download('punkt', quiet=True)
                    self.view.display_message("Téléchargement de 'punkt' réussi.")
                except Exception as e:
                    self.view.display_message(f"ERREUR: Impossible de télécharger les données NLTK. {e}")
            else:
                self.view.display_message("Téléchargement refusé. Certaines fonctionnalités d'apprentissage pourraient être limitées.")

    def start(self):
        """
        Démarre la boucle principale de l'application en utilisant la vue.
        Gère les modes d'entrée texte et vocal.
        """
        # On s'assure que les dépendances sont prêtes avant de démarrer la boucle principale
        self._ensure_dependencies()

        self.view.display_welcome()

        while True:
            command = ""
            if self.voice_mode_enabled:
                self.view.display_listening_prompt()
                status, result = self.voice_recognizer.listen_for_command()
                if status == 'success':
                    self.view.display_message(f"Commande reconnue : '{result}'")
                    command = result
                else:
                    self.view.display_message(f"-> {result}")
                    continue
            else:
                command = self.view.get_command()

            # Commandes spéciales pour gérer l'état de l'application
            clean_command = command.lower().strip()
            if clean_command in ["quitter", "exit", "stop"]:
                break
            if clean_command == "mode vocal":
                self.voice_mode_enabled = True
                self.view.display_message("Mode vocal activé.")
                continue
            if clean_command == "mode texte":
                self.voice_mode_enabled = False
                self.view.display_message("Mode texte activé.")
                continue
            if not command.strip():
                continue

            # Traitement de la commande
            nlp_result = self.nlp_processor.process_command(command)
            self._process_intent(nlp_result)

    def _process_intent(self, nlp_result: dict):
        """
        Demande au Module 11 de planifier une action, puis l'exécute.
        """
        # 1. Obtenir un plan du "cerveau"
        plan = self.neural_network.plan_action(nlp_result)

        # 2. Exécuter le plan
        self.view.display_nlp_result(plan.get("params")) # On affiche toujours l'analyse
        self._execute_plan(plan)

    def _execute_plan(self, plan: dict):
        """
        Exécute une action planifiée en utilisant un dictionnaire de dispatch.
        """
        action = plan.get("action")
        params = plan.get("params")

        action_handlers = {
            "create": self._handle_creation_intent,
            "execute": self._handle_execution_intent,
            "speak": self._handle_speak_intent,
            "learn_face": self._handle_learn_face_intent,
            "verify_face": self._handle_verify_face_intent,
            "install": self._handle_install_intent,
            "search": self._handle_search_intent,
        }

        handler = action_handlers.get(action)
        if handler:
            handler(params)
        else:
            message = f"-> Je ne sais pas comment gérer l'action '{action}'. Pouvez-vous reformuler ?"
            self.view.display_message(message, speak=self.voice_mode_enabled)

    def _handle_speak_intent(self, params: dict):
        """ Gère l'intention de parler pour se présenter. """
        message = "Bonjour, je suis Hikmara, votre assistante IA locale."
        self.view.display_message(message, speak=True)

    def _handle_learn_face_intent(self, params: dict):
        """ Gère l'intention d'apprendre un visage. """
        message = "Je vais tenter d'apprendre votre visage. Veuillez regarder la caméra et ne pas bouger."
        self.view.display_message(message, speak=self.voice_mode_enabled)
        success, message = self.facial_recognizer.learn_face()
        self.view.display_message(f"-> {message}", speak=self.voice_mode_enabled)

    def _handle_verify_face_intent(self, params: dict):
        """ Gère l'intention de vérifier un visage. """
        message = "Je vais tenter de vous identifier. Veuillez regarder la caméra."
        self.view.display_message(message, speak=self.voice_mode_enabled)
        success, message = self.facial_recognizer.verify_face()
        self.view.display_message(f"-> {message}", speak=self.voice_mode_enabled)

    def _handle_install_intent(self, params: dict):
        """ Gère l'intention d'installer un paquet. """
        package_name = params.get("package_name")
        if not package_name:
            message = "-> Vous voulez installer un paquet, mais vous n'avez pas précisé lequel."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            return
        prompt = f"Voulez-vous vraiment installer le paquet '{package_name}' ?"
        if self.internet_controller.request_permission(prompt):
            self.view.display_message(f"-> Lancement de l'installation de '{package_name}'...", speak=self.voice_mode_enabled)
            success, message = self.internet_controller.install_package(package_name)
            self.view.display_message(f"-> {message}", speak=self.voice_mode_enabled)
        else:
            message = "-> Installation annulée."
            self.view.display_message(message, speak=self.voice_mode_enabled)

    def _handle_search_intent(self, params: dict):
        """ Gère l'intention de recherche web et le cycle d'apprentissage. """
        query = params.get("search_query")
        if not query:
            message = "-> Vous voulez rechercher quelque chose, mais votre requête est vide."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            return
        message = f"Recherche en cours pour : '{query}'..."
        self.view.display_message(message, speak=self.voice_mode_enabled)
        search_success, results = self.web_searcher.perform_search(query)
        if not search_success:
            self.view.display_message(f"-> {results}", speak=self.voice_mode_enabled)
            return
        self.view.display_search_results(results)
        prompt = "Voulez-vous que j'apprenne le contenu d'un de ces liens ? Si oui, entrez son numéro. Sinon, tapez 'n'."
        self.view.display_message(prompt, speak=self.voice_mode_enabled)
        choice = self.view.get_command()
        if choice.lower().strip() in ['n', 'non']:
            self.view.display_message("-> Apprentissage annulé.", speak=self.voice_mode_enabled)
            return
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(results):
                url_to_learn = results[choice_index]['url']
                self.view.display_message(f"-> Lecture de la page : {url_to_learn}", speak=self.voice_mode_enabled)
                fetch_success, content = self.internet_controller.fetch_website_content(url_to_learn)
                if fetch_success:
                    self.view.display_message("-> Contenu récupéré. Début de l'analyse et de l'apprentissage...", speak=self.voice_mode_enabled)
                    learn_success = self.raw_learner.learn_from_text(content, source_name=url_to_learn)
                    if learn_success:
                        self.view.display_message("-> Apprentissage terminé avec succès.", speak=self.voice_mode_enabled)
                    else:
                        self.view.display_message("-> Une erreur est survenue durant l'apprentissage.", speak=self.voice_mode_enabled)
                else:
                    self.view.display_message(f"-> Erreur lors de la récupération de la page : {content}", speak=self.voice_mode_enabled)
            else:
                self.view.display_message("-> Choix invalide.", speak=self.voice_mode_enabled)
        except ValueError:
            self.view.display_message("-> Entrée non valide. Apprentissage annulé.", speak=self.voice_mode_enabled)

    def _handle_creation_intent(self, params: dict):
        """
        Gère spécifiquement l'intention de 'créer'.
        """
        project_type = params.get("project_type")
        project_name = params.get("project_name")
        if not project_name:
            message = "-> Vous voulez créer quelque chose, mais je n'ai pas compris le nom du projet."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            return
        if project_type == "python":
            success, message = self.code_generator.create_python_project(project_name)
        elif project_type == "web":
            success, message = self.code_generator.create_web_project(project_name)
        else:
            message = f"-> Je ne sais pas comment créer un projet de type '{project_type}'. Je vais créer un projet web par défaut."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            success, message = self.code_generator.create_web_project(project_name)
        self.view.display_message(f"-> {message}", speak=self.voice_mode_enabled)

    def _handle_execution_intent(self, params: dict):
        """
        Gère spécifiquement l'intention d'exécuter'.
        """
        project_name = params.get("project_name")
        if not project_name:
            message = "-> Vous voulez exécuter un projet, mais je n'ai pas compris lequel."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            return
        project_path = os.path.join(self.code_generator.base_path, project_name)
        script_path = os.path.join(project_path, "main.py")
        if not os.path.exists(script_path):
            message = f"-> Erreur: Impossible de trouver le script principal pour le projet '{project_name}'."
            self.view.display_message(message, speak=self.voice_mode_enabled)
            return
        message = f"-> Lancement du script pour le projet '{project_name}'..."
        self.view.display_message(message, speak=self.voice_mode_enabled)
        success, stdout, stderr = self.code_executor.execute_python_script(script_path)
        self.view.display_execution_result(success, stdout, stderr, speak=self.voice_mode_enabled)


    def shutdown(self):
        """
        Arrête proprement les services et les modules.
        """
        self.knowledge_base.close()
        self.view.display_shutdown_message()
