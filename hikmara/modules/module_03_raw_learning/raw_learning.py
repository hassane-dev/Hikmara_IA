# hikmara/modules/module_03_raw_learning/raw_learning.py
import os
import nltk
import ast
import re
from hikmara.modules.module_02_structured_learning.structured_learning import StructuredLearner

class RawLearner:
    """
    Module 3: Apprentissage brut à partir de fichiers.
    Contient un aiguilleur pour choisir la bonne méthode d'analyse
    en fonction du type de fichier. Ne fait pas d'affichage.
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
        if filepath.endswith('.py'):
            return self._learn_from_python_file(filepath)
        elif filepath.endswith('.php'):
            return self._learn_from_php_file(filepath)
        else: # Par défaut, traiter comme un fichier texte
            return self._learn_from_text_file(filepath)

    def _learn_from_text_file(self, filepath: str) -> bool:
        """
        Analyse un fichier texte en le segmentant en phrases.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            base_filename = os.path.basename(filepath)
            sentences = nltk.sent_tokenize(content)

            all_successful = True
            for i, sentence in enumerate(sentences):
                concept_name = f"{base_filename}_sentence_{i+1}"
                if not self.structured_learner.learn_concept(concept_name, sentence.strip(), f"{base_filename} (phrase {i+1})"):
                    all_successful = False
            return all_successful
        except (FileNotFoundError, Exception):
            return False

    def _learn_from_python_file(self, filepath: str) -> bool:
        """
        Analyse un fichier de code Python et apprend ses fonctions, classes (avec héritage), et imports.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()

            tree = ast.parse(source_code)
            all_successful = True

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    concept_name = f"py_class:{node.name}"
                    content = ast.get_docstring(node) or f"Classe '{node.name}' sans docstring."
                    parent_classes = [base.id for base in node.bases if isinstance(base, ast.Name)]
                    if parent_classes:
                        content += f"\nHérite de : {parent_classes}."
                    if not self.structured_learner.learn_concept(concept_name, content, filepath):
                        all_successful = False

                elif isinstance(node, ast.FunctionDef):
                    concept_name = f"py_function:{node.name}"
                    content = ast.get_docstring(node) or f"Fonction '{node.name}' sans docstring."
                    args = [a.arg for a in node.args.args]
                    if args:
                        content += f"\nArguments : {args}."
                    if not self.structured_learner.learn_concept(concept_name, content, filepath):
                        all_successful = False

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        concept_name = f"py_import:{alias.name}"
                        content = f"Module '{alias.name}' importé dans {os.path.basename(filepath)}."
                        if not self.structured_learner.learn_concept(concept_name, content, filepath):
                            all_successful = False

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or 'local'
                    for alias in node.names:
                        concept_name = f"py_import_from:{module}.{alias.name}"
                        content = f"'{alias.name}' importé depuis le module '{module}' dans {os.path.basename(filepath)}."
                        if not self.structured_learner.learn_concept(concept_name, content, filepath):
                            all_successful = False
            return all_successful
        except (FileNotFoundError, SyntaxError, Exception):
            return False

    def learn_from_directory(self, directory_path: str) -> bool:
        """
        Parcourt un dossier récursivement et apprend de chaque fichier trouvé.
        """
        if not os.path.isdir(directory_path):
            return False

        overall_success = True
        for root, _, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if not self.learn_from_file(file_path):
                    overall_success = False
        return overall_success

    def _learn_from_php_file(self, filepath: str) -> bool:
        """
        Analyse un fichier .php, extrait les blocs de code PHP et les apprend.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            php_blocks = re.findall(r'<\?php(.*?)\?>', content, re.DOTALL)
            if not php_blocks:
                return True

            base_filename = os.path.basename(filepath)
            all_successful = True
            for i, block in enumerate(php_blocks):
                concept_name = f"php_block_{i+1}_from_{base_filename}"
                if not self.structured_learner.learn_concept(concept_name, block.strip(), filepath):
                    all_successful = False
            return all_successful
        except (FileNotFoundError, Exception):
            return False