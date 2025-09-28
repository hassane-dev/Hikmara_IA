# hikmara/modules/module_06_code_execution/code_executor.py
import subprocess
import sys

class CodeExecutor:
    """
    Module 6: Exécution de code externe.
    Capable de lancer des scripts dans des sous-processus et de capturer leur sortie.
    """
    def __init__(self):
        """
        Initialise l'exécuteur de code.
        """
        pass

    def execute_python_script(self, script_path: str) -> tuple[bool, str, str]:
        """
        Exécute un script Python et capture sa sortie.
        :param script_path: Le chemin complet vers le script Python à exécuter.
        :return: Un tuple (succès, stdout, stderr).
                  - succès: True si le script s'est terminé avec un code de sortie 0.
                  - stdout: La sortie standard du script.
                  - stderr: La sortie d'erreur du script.
        """
        try:
            # Utilise l'exécutable Python courant pour lancer le script
            # afin de garantir la cohérence de l'environnement.
            process = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                check=False, # Ne lève pas d'exception si le script échoue
                timeout=30 # Sécurité pour éviter les scripts infinis
            )

            success = process.returncode == 0
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()

            return success, stdout, stderr

        except FileNotFoundError:
            return False, "", f"Erreur: Le script '{script_path}' n'a pas été trouvé."
        except subprocess.TimeoutExpired:
            return False, "", "Erreur: Le temps d'exécution du script a dépassé 30 secondes."
        except Exception as e:
            return False, "", f"Une erreur inattendue est survenue lors de l'exécution: {e}"