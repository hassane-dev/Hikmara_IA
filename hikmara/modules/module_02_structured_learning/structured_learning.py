# hikmara/modules/module_02_structured_learning/structured_learning.py

# Importation pour l'annotation de type et la communication inter-module
from hikmara.modules.module_01_knowledge_base.knowledge_base import KnowledgeBase

class StructuredLearner:
    """
    Module 2: Apprentissage structuré.
    Ce module est responsable de l'apprentissage de concepts bien définis
    et de leur enregistrement dans la base de connaissances (Module 1).
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialise le module d'apprentissage structuré.

        :param knowledge_base: Une instance du Module 1 (KnowledgeBase) pour la communication.
        """
        if knowledge_base is None:
            raise ValueError("L'instance de KnowledgeBase ne peut pas être None.")
        self.kb = knowledge_base
        print("Module 2 (StructuredLearner) initialisé.")

    def learn_concept(self, concept_name: str, content: str, source: str = None) -> bool:
        """
        Apprend un nouveau concept et l'ajoute à la base de connaissances.

        :param concept_name: Le nom du concept à apprendre.
        :param content: La définition ou le contenu du concept.
        :param source: La source de l'information.
        :return: True si l'apprentissage (l'ajout) a réussi, False sinon.
        """
        print(f"Apprentissage du concept '{concept_name}'...")
        new_id = self.kb.add_knowledge(concept_name, content, source)
        if new_id is not None:
            print(f"  -> Succès: Concept '{concept_name}' appris et stocké avec l'ID {new_id}.")
            return True
        else:
            print(f"  -> Échec: Impossible d'apprendre le concept '{concept_name}'. Il existe peut-être déjà.")
            return False
