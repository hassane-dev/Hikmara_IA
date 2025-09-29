# hikmara/view/terminal_view.py

class TerminalView:
    """
    Gère l'interface utilisateur en mode terminal.
    Responsable de l'affichage des informations et de la saisie des commandes.
    """
    def __init__(self, synthesizer=None):
        """
        Initialise la vue terminal.
        :param synthesizer: Une instance du VoiceSynthesizer pour la sortie vocale.
        """
        self.synthesizer = synthesizer

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

    def display_message(self, message: str, speak: bool = False):
        """
        Affiche un message général à l'utilisateur et le lit à voix haute si demandé.
        """
        print(message)
        if speak and self.synthesizer:
            self.synthesizer.speak(message)

    def display_listening_prompt(self):
        """ Affiche le message indiquant que l'IA écoute. """
        print("🎤 Je vous écoute...")

    def display_nlp_result(self, nlp_result: dict):
        """
        Affiche de manière formatée le résultat de l'analyse NLP.
        """
        if nlp_result.get("error"):
            self.display_message(f"Erreur NLP: {nlp_result['error']}")
            return

        print("--- Analyse de la commande ---")
        print(f"  > Intention: {nlp_result.get('intent', 'N/A')}")
        print(f"  > Type de projet: {nlp_result.get('project_type', 'N/A')}")
        print(f"  > Nom du projet: {nlp_result.get('project_name', 'N/A')}")
        print("------------------------------")

    def display_execution_result(self, success: bool, stdout: str, stderr: str, speak: bool = False):
        """
        Affiche le résultat de l'exécution d'un script de manière formatée.
        """
        if success:
            message = "Exécution terminée avec succès."
            self.display_message(f"-> {message}", speak=speak)
            if stdout:
                print("--- Sortie du Script ---")
                print(stdout)
                # On ne lit pas la sortie complète pour ne pas être trop verbeux
        else:
            message = "L'exécution a échoué."
            self.display_message(f"-> {message}", speak=speak)
            if stderr:
                print("--- Erreur du Script ---")
                print(stderr)

    def display_search_results(self, results: list):
        """
        Affiche les résultats d'une recherche web.
        """
        self.display_message("-> Voici les résultats trouvés :")
        for i, result in enumerate(results):
            # Pour l'instant, on n'a que l'URL.
            print(f"  {i+1}. {result['url']}")

    def display_shutdown_message(self):
        """
        Affiche le message d'arrêt de l'application.
        """
        print("Arrêt de Hikmara.")