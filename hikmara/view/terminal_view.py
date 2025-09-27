# hikmara/view/terminal_view.py

class TerminalView:
    """
    Gère l'interface utilisateur en mode terminal.
    Responsable de l'affichage des informations et de la saisie des commandes.
    """
    def __init__(self):
        """
        Initialise la vue terminal.
        """
        pass # Pas d'initialisation complexe nécessaire pour l'instant.

    def display_welcome(self):
        """
        Affiche le message de bienvenue au démarrage.
        """
        print("\n--- Hikmara est prête ---")
        print("Entrez une commande ou 'quitter' pour arrêter.")

    def get_command(self) -> str:
        """
        Affiche le prompt et retourne la commande saisie par l'utilisateur.
        """
        try:
            command = input(">>> ")
            return command
        except EOFError:
            # Gère Ctrl+D pour quitter proprement
            return "quitter"
        except KeyboardInterrupt:
            # Gère Ctrl+C pour quitter proprement
            print() # Ajoute une nouvelle ligne pour la propreté
            return "quitter"

    def display_message(self, message: str):
        """
        Affiche un message général à l'utilisateur.
        """
        print(message)

    def display_nlp_result(self, nlp_result: dict):
        """
        Affiche de manière formatée le résultat de l'analyse NLP.
        """
        if nlp_result.get("error"):
            self.display_message(f"Erreur NLP: {nlp_result['error']}")
            return

        print("--- Analyse de la commande ---")
        print(f"  > Intention: {nlp_result.get('intent', 'N/A')}")
        print(f"  > Entités: {nlp_result.get('entities', 'N/A')}")
        print("------------------------------")

    def display_shutdown_message(self):
        """
        Affiche le message d'arrêt de l'application.
        """
        print("Arrêt de Hikmara.")