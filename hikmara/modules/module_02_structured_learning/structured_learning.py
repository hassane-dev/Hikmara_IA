# hikmara/modules/module_02_structured_learning/structured_learning.py
import nltk
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase

class StructuredLearner:
    """
    Module 2: Apprentissage structuré avec NLTK.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialise le module et s'assure que les dépendances NLTK sont prêtes.
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
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Ressource NLTK 'punkt' non trouvée. Téléchargement en cours...")
            nltk.download('punkt', quiet=True)
            print("Téléchargement de 'punkt' terminé.")

    def learn_concept(self, concept_name: str, content: str, source: str = None) -> bool:
        """
        Analyse (tokenise) et apprend un nouveau concept, puis le stocke.
        """
        print(f"Module 2: Analyse du concept '{concept_name}'...")
        tokens = nltk.word_tokenize(content)
        print(f"  -> Tokens NLTK: {tokens}")

        new_id = self.kb.add_knowledge(concept_name, content, source)
        if new_id is not None:
            print(f"  -> Concept '{concept_name}' stocké avec succès.")
            return True
        else:
            print(f"  -> Échec du stockage du concept '{concept_name}'.")
            return False
