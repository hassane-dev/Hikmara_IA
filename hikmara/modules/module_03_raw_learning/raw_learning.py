# hikmara/modules/module_03_raw_learning/raw_learning.py
import os
import nltk
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
        Lit un fichier, le segmente en phrases, et utilise le Module 2
        pour apprendre chaque phrase individuellement.

        :param filepath: Le chemin d'accès au fichier à apprendre.
        :return: True si l'apprentissage de toutes les phrases a réussi, False sinon.
        """
        print(f"Module 3: Lecture du fichier '{filepath}' pour apprentissage granulaire...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            base_filename = os.path.basename(filepath)
            sentences = nltk.sent_tokenize(content)
            print(f"  -> Fichier découpé en {len(sentences)} phrases.")

            all_successful = True
            for i, sentence in enumerate(sentences):
                # Crée un nom de concept unique pour chaque phrase
                concept_name = f"{base_filename}_sentence_{i+1}"
                success = self.structured_learner.learn_concept(
                    concept_name=concept_name,
                    content=sentence.strip(),
                    source=f"{base_filename} (phrase {i+1})"
                )
                if not success:
                    all_successful = False

            return all_successful

        except FileNotFoundError:
            print(f"  -> ERREUR: Fichier non trouvé à '{filepath}'.")
            return False
        except Exception as e:
            print(f"  -> ERREUR: Une erreur inattendue est survenue en lisant le fichier: {e}")
            return False
