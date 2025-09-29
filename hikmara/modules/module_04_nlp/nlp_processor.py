# hikmara/modules/module_04_nlp/nlp_processor.py
import spacy
import os

class NLPProcessor:
    """
    Module 4: NLP / Compréhension du langage naturel.
    Utilise spaCy pour analyser les commandes de l'utilisateur,
    identifier les intentions et extraire les entités.
    """
    def __init__(self, internet_controller, model_name="fr_core_news_sm"):
        """
        Initialise le processeur NLP en chargeant le modèle spaCy.
        :param internet_controller: L'instance du contrôleur Internet pour gérer les téléchargements.
        :param model_name: Le nom du modèle spaCy à utiliser.
        """
        self.model_name = model_name
        self.internet_controller = internet_controller
        self.nlp = self._load_model()

    def _load_model(self):
        """
        Charge le modèle spaCy. S'il n'est pas disponible,
        demande la permission de le télécharger via l'InternetController.
        """
        try:
            return spacy.load(self.model_name)
        except OSError:
            prompt = f"Le modèle spaCy '{self.model_name}' est manquant. Puis-je le télécharger ?"
            if self.internet_controller.request_permission(prompt):
                self.internet_controller.view.display_message(f"Téléchargement du modèle spaCy '{self.model_name}'...")
                try:
                    spacy.cli.download(self.model_name)
                    self.internet_controller.view.display_message("Téléchargement terminé.")
                    return spacy.load(self.model_name)
                except Exception as e:
                    self.internet_controller.view.display_message(f"ERREUR: Impossible de télécharger le modèle. {e}")
                    return None
            else:
                self.internet_controller.view.display_message("Téléchargement refusé. Le module NLP ne sera pas fonctionnel.")
                return None

    def process_command(self, command_text: str) -> dict:
        """
        Analyse une commande textuelle et retourne une structure de données
        contenant les intentions, types de projet et noms.
        """
        if not self.nlp:
            return {"error": "Le modèle NLP n'est pas chargé."}

        doc = self.nlp(command_text.lower()) # Travailler en minuscules pour la simplicité

        # --- Définition des mots-clés ---
        INTENT_KEYWORDS = {
            "create": ["crée", "créer", "fabrique", "génère"],
            "execute": ["exécute", "exécuter", "lance", "lancer", "démarre"],
            "install": ["installe", "installer", "télécharge"],
            "search": ["recherche", "cherche", "trouve"],
            "speak": ["parle", "parler", "dis", "dire", "présente-toi"],
            "learn_face": ["apprends", "apprendre", "mémorise", "mémoriser", "enregistre mon visage"],
            "verify_face": ["identifie", "identifier", "vérifie", "vérifier", "reconnais", "qui suis-je"]
        }
        PROJECT_TYPE_KEYWORDS = {
            "python": ["python", "py"],
            "web": ["web", "html", "site"]
        }

        # --- Initialisation des résultats ---
        result = {
            "original_text": command_text,
            "intent": "unknown",
            "project_type": "unknown",
            "project_name": None,
            "package_name": None,
            "search_query": None, # Ajout pour la recherche
            "entities": {ent.label_: ent.text for ent in self.nlp(command_text).ents}
        }

        # --- Extraction par mots-clés ---
        tokens = [token.text for token in doc]

        # 1. Trouver l'intention
        for intent, keywords in INTENT_KEYWORDS.items():
            if any(keyword in tokens for keyword in keywords):
                result["intent"] = intent
                break

        # 2. Trouver le type de projet
        for project_type, keywords in PROJECT_TYPE_KEYWORDS.items():
            if any(keyword in tokens for keyword in keywords):
                result["project_type"] = project_type
                break

        # 3. Extraire le nom du projet (heuristique simple)
        # On cherche un nom propre (PROPN) ou un nom (NOUN) qui n'est pas un mot-clé.
        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"] and token.text not in (
                PROJECT_TYPE_KEYWORDS["python"] + PROJECT_TYPE_KEYWORDS["web"] + ["projet", "script"]
            ):
                 # On prend le nom original (avec majuscules) pour le nom du projet
                result["project_name"] = self.nlp(command_text)[token.i].text
                break

        # Si le nom n'est pas trouvé, on peut essayer avec les entités génériques
        if not result["project_name"] and result["entities"]:
            result["project_name"] = next(iter(result["entities"].values()), None)

        # 4. Extraire le nom du paquet si l'intention est d'installer
        if result["intent"] == "install":
            # Heuristique: le nom du paquet est souvent le nom qui suit le mot-clé d'installation.
            for i, token in enumerate(doc):
                if token.text in INTENT_KEYWORDS["install"] and i + 1 < len(doc):
                    result["package_name"] = doc[i + 1].text
                    break
            if not result["package_name"]:
                result["package_name"] = result["project_name"]

        # 5. Extraire la requête de recherche
        if result["intent"] == "search":
            for i, token in enumerate(doc):
                if token.text in INTENT_KEYWORDS["search"]:
                    # On prend tout le reste de la phrase comme requête
                    result["search_query"] = command_text[token.idx + len(token.text):].strip()
                    break

        return result