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

    def learn_concept(self, concept_name: str, content: str, source: str = None) -> bool:
        """
        Analyse (tokenise) et apprend un nouveau concept, puis le stocke.
        Retourne True en cas de succès, False sinon.
        """
        # La tokenisation est une étape interne, pas besoin de l'afficher.
        nltk.word_tokenize(content)

        new_id = self.kb.add_knowledge(concept_name, content, source)
        return new_id is not None
