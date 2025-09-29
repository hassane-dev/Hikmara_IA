# hikmara/modules/module_10_internet_control/internet_controller.py
import subprocess
import sys

class InternetController:
    """
    Module 10: Contrôle Internet et installation locale.
    Sert de gardien pour toutes les actions nécessitant un accès à Internet.
    """

    def __init__(self, view):
        """
        Initialise le contrôleur Internet.
        :param view: L'instance de la vue pour interagir avec l'utilisateur.
        """
        self.view = view

    def request_permission(self, prompt: str) -> bool:
        """
        Demande la permission à l'utilisateur pour une action spécifique.
        :param prompt: La question à poser à l'utilisateur.
        :return: True si l'utilisateur donne son accord, False sinon.
        """
        self.view.display_message(f"[PERMISSION REQUISE] {prompt} [o/n]")

        # Boucle jusqu'à obtenir une réponse valide
        while True:
            response = self.view.get_command().lower().strip()
            if response in ["o", "oui", "yes", "y"]:
                return True
            elif response in ["n", "non", "no"]:
                return False
            else:
                self.view.display_message("Réponse non valide. Veuillez répondre par 'o' (oui) ou 'n' (non).")

    def install_package(self, package_name: str) -> tuple[bool, str]:
        """
        Installe un paquet Python en utilisant pip.
        :param package_name: Le nom du paquet à installer.
        :return: Un tuple (succès, message de sortie).
        """
        try:
            # Utilise l'exécutable Python courant pour lancer pip
            process = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                check=False, # Ne lève pas d'exception si pip échoue
                timeout=300 # Timeout de 5 minutes pour les grosses installations
            )

            if process.returncode == 0:
                message = f"Le paquet '{package_name}' a été installé avec succès."
                return True, message
            else:
                message = f"Erreur lors de l'installation de '{package_name}':\n{process.stderr}"
                return False, message

        except subprocess.TimeoutExpired:
            return False, "Erreur: Le temps d'installation a dépassé 5 minutes."
        except Exception as e:
            return False, f"Une erreur inattendue est survenue: {e}"