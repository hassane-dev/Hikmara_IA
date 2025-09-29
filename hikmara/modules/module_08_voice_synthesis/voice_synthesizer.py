# hikmara/modules/module_08_voice_synthesis/voice_synthesizer.py
import pyttsx3

class VoiceSynthesizer:
    """
    Module 8: Synthèse vocale.
    Utilise la bibliothèque pyttsx3 pour convertir du texte en parole.
    """

    def __init__(self):
        """
        Initialise le moteur de synthèse vocale.
        """
        try:
            self.engine = pyttsx3.init()
            self._configure_voice()
        except Exception:
            # Si le moteur ne peut pas être initialisé, il sera None.
            # La logique appelante devra gérer ce cas.
            self.engine = None

    def _configure_voice(self):
        """
        Tente de configurer une voix française si disponible.
        """
        if not self.engine:
            return

        voices = self.engine.getProperty('voices')
        # Cherche une voix française. La détection peut varier selon l'OS.
        for voice in voices:
            if "french" in voice.name.lower() or "fr-fr" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                return
        # Si aucune voix française n'est trouvée, la voix par défaut sera utilisée.

    def speak(self, text: str):
        """
        Convertit le texte fourni en parole et le lit à voix haute.
        Cette méthode est bloquante jusqu'à ce que la parole soit terminée.
        """
        if not self.engine:
            # Si le moteur n'est pas disponible, ne fait rien.
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            # En cas d'erreur de la bibliothèque, on ne bloque pas le programme.
            pass