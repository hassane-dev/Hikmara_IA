# hikmara/main.py
import sys
import os

# Ajout du chemin du projet au sys.path pour permettre les imports absolus
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from hikmara.controller.main_controller import MainController

def main():
    """
    Point d'entrée principal de l'application Hikmara.
    """
    print("--- Initialisation de Hikmara ---")
    app_controller = MainController()
    try:
        app_controller.start()
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur détectée.")
    finally:
        app_controller.shutdown()
        print("--- Hikmara terminée ---")

if __name__ == "__main__":
    main()
