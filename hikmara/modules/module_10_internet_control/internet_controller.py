# hikmara/modules/module_10_internet_control/internet_controller.py
import subprocess
import sys
import requests
from bs4 import BeautifulSoup

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

    def fetch_website_content(self, url: str) -> tuple[bool, str]:
        """
        Récupère et nettoie le contenu textuel d'une page web.
        :param url: L'URL de la page à lire.
        :return: Un tuple (succès, contenu textuel ou message d'erreur).
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP

            soup = BeautifulSoup(response.text, 'html.parser')

            # Supprimer les balises de script et de style
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            # Extraire le texte et nettoyer les espaces
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)

            return True, clean_text

        except requests.exceptions.RequestException as e:
            return False, f"Erreur réseau lors de l'accès à l'URL: {e}"
        except Exception as e:
            return False, f"Une erreur inattendue est survenue lors de la lecture de la page: {e}"