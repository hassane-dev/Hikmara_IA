# hikmara/modules/module_04_nlp/nlp_processor.py
import spacy
import os

class NLPProcessor:
    """
    Module 4: NLP / Compréhension du langage naturel.
    Utilise spaCy pour analyser les commandes de l'utilisateur,
    identifier les intentions et extraire les entités.
    """
    def __init__(self, model_name="fr_core_news_sm"):
        """
        Initialise le processeur NLP en chargeant le modèle spaCy.
        S'assure que le modèle est téléchargé s'il n'existe pas.
        """
        self.model_name = model_name
        self.nlp = self._load_model()

    def _load_model(self):
        """
        Charge le modèle spaCy. S'il n'est pas disponible,
        tente de le télécharger. Retourne None en cas d'échec.
        """
        try:
            return spacy.load(self.model_name)
        except OSError:
            try:
                # Redirige la sortie du téléchargement pour ne pas polluer la console
                print(f"Téléchargement du modèle spaCy '{self.model_name}'...")
                spacy.cli.download(self.model_name)
                print("Téléchargement terminé.")
                return spacy.load(self.model_name)
            except Exception:
                # L'échec sera géré par la logique appelante.
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
            "speak": ["parle", "parler", "dis", "dire", "présente-toi"]
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

        return result