# hikmara/modules/module_02_structured_learning/structured_learning.py
import nltk
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase

class StructuredLearner:
    """
    Module 2: Apprentissage structuré.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialise le module d'apprentissage structuré.
        """
        if knowledge_base is None:
            raise ValueError("L'instance de KnowledgeBase ne peut pas être None.")
        self.kb = knowledge_base
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        """
        S'assure que les données NLTK nécessaires (punkt) sont téléchargées.
        """
        try:
            # Essaye de trouver la ressource. Si elle n'existe pas, une LookupError est levée.
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Ressource NLTK 'punkt' non trouvée. Téléchargement en cours...")
            nltk.download('punkt', quiet=True)
            print("Téléchargement de 'punkt' terminé.")

    def learn_concept(self, concept_name: str, content: str, source: str = None) -> bool:
        """
        Analyse et apprend un nouveau concept, puis l'ajoute à la base de connaissances.
        """
        print(f"Module 2: Analyse du concept '{concept_name}' avec NLTK...")

        # Utilisation de NLTK pour la tokenisation
        tokens = nltk.word_tokenize(content)
        print(f"  -> Contenu tokenisé: {tokens}")

        # Le contenu original est toujours stocké pour l'instant.
        # Les 'tokens' pourraient être stockés dans un autre champ/table plus tard.
        print(f"Module 2: Tentative d'enregistrement du concept '{concept_name}'.")
        new_id = self.kb.add_knowledge(concept_name, content, source)
        return new_id is not None
