# hikmara/modules/module_03_raw_learning/raw_learning.py
import os
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner

class RawLearner:
    """
    Module 3: Apprentissage brut à partir de fichiers.
    """
    def __init__(self, structured_learner: StructuredLearner):
        """
        Initialise le module d'apprentissage brut.

        :param structured_learner: Une instance de StructuredLearner (Module 2).
        """
        if structured_learner is None:
            raise ValueError("L'instance de StructuredLearner ne peut pas être None.")
        self.structured_learner = structured_learner

    def learn_from_file(self, filepath: str) -> bool:
        """
        Lit un fichier et utilise le Module 2 pour apprendre son contenu.

        :param filepath: Le chemin d'accès au fichier à apprendre.
        :return: True si l'apprentissage a réussi, False sinon.
        """
        print(f"Module 3: Tentative de lecture du fichier '{filepath}'...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            concept_name = os.path.basename(filepath)

            # Utilise le Module 2 pour traiter et stocker le contenu
            return self.structured_learner.learn_concept(
                concept_name=concept_name,
                content=content,
                source=filepath
            )
        except FileNotFoundError:
            print(f"  -> ERREUR: Fichier non trouvé à '{filepath}'.")
            return False
        except Exception as e:
            print(f"  -> ERREUR: Une erreur inattendue est survenue en lisant le fichier: {e}")
            return False
