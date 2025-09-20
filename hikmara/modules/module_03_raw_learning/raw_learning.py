# hikmara/modules/module_03_raw_learning/raw_learning.py
import os
import nltk
import ast
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner

class RawLearner:
    """
    Module 3: Apprentissage brut à partir de fichiers.
    Contient un aiguilleur pour choisir la bonne méthode d'analyse
    en fonction du type de fichier.
    """
    def __init__(self, structured_learner: StructuredLearner):
        if structured_learner is None:
            raise ValueError("L'instance de StructuredLearner ne peut pas être None.")
        self.structured_learner = structured_learner

    def learn_from_file(self, filepath: str) -> bool:
        """
        Aiguilleur principal: choisit la méthode d'apprentissage appropriée
        en fonction de l'extension du fichier.
        """
        print(f"Module 3: Réception du fichier '{filepath}'. Détection du type...")
        if filepath.endswith('.py'):
            print("  -> Fichier Python détecté. Lancement de l'analyseur de code.")
            return self._learn_from_python_file(filepath)
        else: # Par défaut, traiter comme un fichier texte
            print("  -> Fichier texte par défaut détecté. Lancement de l'analyseur de texte.")
            return self._learn_from_text_file(filepath)

    def _learn_from_text_file(self, filepath: str) -> bool:
        """
        Analyse un fichier texte en le segmentant en phrases.
        """
        print(f"Module 3 (Texte): Lecture du fichier '{filepath}'...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            base_filename = os.path.basename(filepath)
            sentences = nltk.sent_tokenize(content)
            print(f"  -> Fichier découpé en {len(sentences)} phrases.")

            all_successful = True
            for i, sentence in enumerate(sentences):
                concept_name = f"{base_filename}_sentence_{i+1}"
                if not self.structured_learner.learn_concept(concept_name, sentence.strip(), f"{base_filename} (phrase {i+1})"):
                    all_successful = False
            return all_successful

        except FileNotFoundError:
            print(f"  -> ERREUR: Fichier non trouvé à '{filepath}'.")
            return False
        except Exception as e:
            print(f"  -> ERREUR: Une erreur inattendue est survenue en lisant le fichier: {e}")
            return False

    def _learn_from_python_file(self, filepath: str) -> bool:
        """
        Analyse un fichier de code Python et apprend ses fonctions et classes
        en extrayant leur docstring.
        """
        print(f"Module 3 (Python): Analyse du fichier '{filepath}'...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()

            tree = ast.parse(source_code)
            all_successful = True

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    node_type = "Fonction" if isinstance(node, ast.FunctionDef) else "Classe"
                    concept_name = f"py_{node_type.lower()}:{node.name}"
                    # Utilise le docstring comme contenu, ou une description par défaut
                    content = ast.get_docstring(node) or f"{node_type} '{node.name}' sans docstring."

                    if not self.structured_learner.learn_concept(concept_name, content, filepath):
                        all_successful = False

            return all_successful

        except FileNotFoundError:
            print(f"  -> ERREUR: Fichier Python non trouvé à '{filepath}'.")
            return False
        except SyntaxError as e:
            print(f"  -> ERREUR: Erreur de syntaxe dans le fichier Python: {e}")
            return False
        except Exception as e:
            print(f"  -> ERREUR: Une erreur inattendue est survenue: {e}")
            return False
