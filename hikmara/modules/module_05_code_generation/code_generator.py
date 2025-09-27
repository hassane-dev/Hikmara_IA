# hikmara/modules/module_05_code_generation/code_generator.py
import os

class CodeGenerator:
    """
    Module 5: Génération de code et de structures de projet.
    """
    def __init__(self, base_path="projects"):
        """
        Initialise le générateur de code.
        :param base_path: Le dossier racine où les projets seront créés.
        """
        self.base_path = base_path
        # S'assurer que le dossier de base pour les projets existe
        os.makedirs(self.base_path, exist_ok=True)

    def create_web_project(self, project_name: str) -> tuple[bool, str]:
        """
        Crée une structure de base pour un projet web simple.
        - Crée un dossier pour le projet.
        - Crée un fichier index.html de base.
        :param project_name: Le nom du projet à créer.
        :return: Un tuple (succès, message).
        """
        project_path = os.path.join(self.base_path, project_name)

        # Vérifier si le projet existe déjà pour éviter les erreurs
        if os.path.exists(project_path):
            return False, f"Le projet '{project_name}' existe déjà."

        try:
            # 1. Créer le dossier du projet
            os.makedirs(project_path)

            # 2. Créer le fichier index.html de base
            index_html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; margin-top: 50px; }}
    </style>
</head>
<body>
    <h1>Bienvenue sur le projet '{project_name}'</h1>
    <p>Ce projet a été généré par Hikmara.</p>
</body>
</html>"""

            with open(os.path.join(project_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_html_content)

            success_message = f"Le projet web '{project_name}' a été créé avec succès dans '{project_path}'."
            return True, success_message

        except OSError as e:
            error_message = f"Erreur lors de la création du projet '{project_name}': {e}"
            return False, error_message