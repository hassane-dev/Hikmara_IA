# hikmara/modules/module_07_voice_recognition/voice_recognizer.py
import speech_recognition as sr

class VoiceRecognizer:
    """
    Module 7: Reconnaissance vocale.
    Utilise la bibliothèque SpeechRecognition pour écouter les commandes de l'utilisateur
    via le microphone et les convertir en texte.
    """

    def __init__(self):
        """
        Initialise le reconnaisseur vocal.
        """
        self.recognizer = sr.Recognizer()
        # On ajuste le seuil d'énergie pour mieux détecter le début et la fin de la parole.
        self.recognizer.energy_threshold = 4000

    def listen_for_command(self) -> tuple[str, str | None]:
        """
        Écoute une commande via le microphone et la transcrit en texte.
        Cette méthode est bloquante pendant l'écoute.

        :return: Un tuple (statut, résultat).
                 - statut: "success", "unrecognized", "error", "timeout".
                 - résultat: Le texte de la commande ou un message d'erreur/information.
        """
        try:
            with sr.Microphone() as source:
                # Ajustement rapide au bruit ambiant
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # L'information "Je vous écoute..." sera gérée par la vue.

                # Écoute de la parole avec un timeout pour ne pas bloquer indéfiniment
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            # La reconnaissance est une étape interne, pas besoin d'afficher de message.
            # Utilisation de l'API de reconnaissance vocale de Google
            text = self.recognizer.recognize_google(audio, language="fr-FR")

            return "success", text

        except sr.WaitTimeoutError:
            # L'utilisateur n'a pas parlé dans le temps imparti
            return "timeout", "Aucune parole n'a été détectée."
        except sr.UnknownValueError:
            # L'API n'a pas pu comprendre l'audio
            return "unrecognized", "Désolé, je n'ai pas compris ce que vous avez dit."
        except sr.RequestError as e:
            # Erreur de connexion à l'API (ex: pas d'Internet)
            error_msg = f"Impossible de contacter le service de reconnaissance vocale; {e}"
            return "error", error_msg
        except Exception as e:
            # Autre erreur inattendue
            return "error", f"Une erreur inattendue est survenue: {e}"