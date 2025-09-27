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
        contenant les informations extraites. Ne fait pas d'affichage.
        """
        if not self.nlp:
            return {
                "error": "Le modèle NLP n'est pas chargé.",
                "intent": None,
                "entities": {}
            }

        doc = self.nlp(command_text)

        # Logique d'extraction d'intention (simpliste pour commencer)
        # Exemple: si le verbe est "créer" ou "ouvrir", on en déduit l'intention.
        intent = None
        for token in doc:
            if token.pos_ == "VERB":
                intent = token.lemma_ # Utiliser le lemme pour la forme de base
                break
        if intent is None:
            intent = "unknown"

        # Extraction d'entités nommées
        entities = {ent.label_: ent.text for ent in doc.ents}

        return {
            "original_text": command_text,
            "intent": intent,
            "entities": entities,
            "tokens": [token.text for token in doc]
        }