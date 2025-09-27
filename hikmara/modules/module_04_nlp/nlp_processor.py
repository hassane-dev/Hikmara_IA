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
        tente de le télécharger.
        """
        try:
            # Essayer de charger le modèle
            nlp = spacy.load(self.model_name)
            print(f"Modèle spaCy '{self.model_name}' chargé avec succès.")
            return nlp
        except OSError:
            print(f"Modèle spaCy '{self.model_name}' non trouvé.")
            print("Tentative de téléchargement...")
            try:
                spacy.cli.download(self.model_name)
                nlp = spacy.load(self.model_name)
                print(f"Modèle '{self.model_name}' téléchargé et chargé avec succès.")
                return nlp
            except Exception as e:
                print(f"ERREUR: Impossible de télécharger le modèle spaCy '{self.model_name}'.")
                print(f"Veuillez l'installer manuellement avec la commande : python -m spacy download {self.model_name}")
                print(f"Erreur originale: {e}")
                return None

    def process_command(self, command_text: str) -> dict:
        """
        Analyse une commande textuelle et retourne une structure de données
        contenant les informations extraites.
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

        print(f"--- Analyse NLP ---")
        print(f"Commande: '{command_text}'")
        print(f"  -> Intention détectée: {intent}")
        print(f"  -> Entités reconnues: {entities}")
        print(f"--------------------")

        return {
            "original_text": command_text,
            "intent": intent,
            "entities": entities,
            "tokens": [token.text for token in doc]
        }