# hikmara/modules/module_02_structured_learning/structured_learning.py
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

    def learn_concept(self, concept_name: str, content: str, source: str = None) -> bool:
        """
        Apprend un nouveau concept et l'ajoute à la base de connaissances.
        """
        print(f"Module 2: Tentative d'apprentissage du concept '{concept_name}'.")
        new_id = self.kb.add_knowledge(concept_name, content, source)
        return new_id is not None
