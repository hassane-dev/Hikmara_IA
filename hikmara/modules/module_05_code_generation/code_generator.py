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
        Crée une structure de base pour un projet web simple (HTML, CSS, JS).
        - Crée un dossier pour le projet.
        - Crée des sous-dossiers pour css et js.
        - Crée un fichier index.html, style.css et script.js de base.
        :param project_name: Le nom du projet à créer.
        :return: Un tuple (succès, message).
        """
        project_path = os.path.join(self.base_path, project_name)
        if os.path.exists(project_path):
            return False, f"Le projet '{project_name}' existe déjà."

        try:
            # Créer les dossiers
            css_path = os.path.join(project_path, "css")
            js_path = os.path.join(project_path, "js")
            os.makedirs(css_path)
            os.makedirs(js_path)

            # Contenu HTML
            index_html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Bienvenue sur le projet '{project_name}'</h1>
    <p>Ce projet a été généré par Hikmara.</p>
    <script src="js/script.js"></script>
</body>
</html>"""

            # Contenu CSS
            style_css_content = """body {
    font-family: sans-serif;
    text-align: center;
    margin-top: 50px;
    background-color: #f0f0f0;
    color: #333;
}

h1 {
    color: #0056b3;
}
"""

            # Contenu JS
            script_js_content = f"console.log(\"Le script du projet '{project_name}' a été chargé.\");"

            # Écrire les fichiers
            with open(os.path.join(project_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(index_html_content)
            with open(os.path.join(css_path, "style.css"), "w", encoding="utf-8") as f:
                f.write(style_css_content)
            with open(os.path.join(js_path, "script.js"), "w", encoding="utf-8") as f:
                f.write(script_js_content)

            success_message = f"Le projet web '{project_name}' a été créé avec succès dans '{project_path}'."
            return True, success_message

        except OSError as e:
            error_message = f"Erreur lors de la création du projet '{project_name}': {e}"
            return False, error_message

    def create_python_project(self, project_name: str) -> tuple[bool, str]:
        """
        Crée une structure de base pour un projet Python.
        - Crée un dossier pour le projet.
        - Crée un sous-dossier source, un dossier de tests, un README et un requirements.txt.
        - Crée un fichier main.py de base.
        :param project_name: Le nom du projet à créer.
        :return: Un tuple (succès, message).
        """
        project_path = os.path.join(self.base_path, project_name)
        if os.path.exists(project_path):
            return False, f"Le projet '{project_name}' existe déjà."

        try:
            # Créer les dossiers
            # Note: Le dossier source porte le même nom que le projet pour les imports
            src_path = os.path.join(project_path, project_name)
            tests_path = os.path.join(project_path, "tests")
            os.makedirs(src_path)
            os.makedirs(tests_path)

            # Contenu du main.py
            main_py_content = f"""# Projet '{project_name}' généré par Hikmara

def main():
    print("Hello, World! from project '{project_name}'")

if __name__ == "__main__":
    main()
"""
            # Contenu du README
            readme_content = f"# Projet {project_name}\\n\\nCe projet a été généré par Hikmara."

            # Écrire les fichiers
            with open(os.path.join(src_path, "main.py"), "w", encoding="utf-8") as f:
                f.write(main_py_content)
            with open(os.path.join(src_path, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("") # Fichier vide
            with open(os.path.join(tests_path, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("") # Fichier vide
            with open(os.path.join(project_path, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write("# Dépendances du projet\\n")
            with open(os.path.join(project_path, "README.md"), "w", encoding="utf-8") as f:
                f.write(readme_content)

            success_message = f"Le projet Python '{project_name}' a été créé avec succès dans '{project_path}'."
            return True, success_message

        except OSError as e:
            error_message = f"Erreur lors de la création du projet Python '{project_name}': {e}"
            return False, error_message