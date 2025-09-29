# hikmara/modules/module_09_facial_recognition/facial_recognizer.py
import cv2
import face_recognition
import numpy as np
import os

class FacialRecognizer:
    """
    Module 9: Reconnaissance faciale.
    Gère l'apprentissage et la vérification du visage de l'utilisateur.
    """

    def __init__(self, data_path="hikmara/model/security"):
        """
        Initialise le reconnaisseur facial.
        :param data_path: Le dossier où stocker les données de visage.
        """
        self.data_path = data_path
        self.known_face_encoding_path = os.path.join(self.data_path, "user_face.npy")
        os.makedirs(self.data_path, exist_ok=True)
        self.known_face_encoding = self._load_known_face()

    def _load_known_face(self):
        """ Charge l'encodage du visage connu s'il existe. """
        if os.path.exists(self.known_face_encoding_path):
            return np.load(self.known_face_encoding_path)
        return None

    def _get_face_encoding_from_webcam(self):
        """
        Capture une image de la webcam, détecte un visage et retourne son encodage.
        Retourne (status, data), où status peut être "success", "no_face", "multi_face", "error".
        """
        # Utilisation de la webcam 0 (par défaut)
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            return "error", "Impossible d'accéder à la webcam."

        ret, frame = video_capture.read()
        video_capture.release() # On relâche la webcam immédiatement

        if not ret:
            return "error", "Impossible de capturer une image depuis la webcam."

        # Convertir l'image de BGR (utilisé par OpenCV) en RGB (utilisé par face_recognition)
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) == 0:
            return "no_face", "Aucun visage n'a été détecté."

        if len(face_locations) > 1:
            return "multi_face", "Plusieurs visages ont été détectés. Veuillez être seul devant la caméra."

        # On prend le premier (et unique) visage trouvé
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        return "success", face_encoding

    def learn_face(self) -> tuple[bool, str]:
        """
        Apprend le visage de l'utilisateur principal via la webcam.
        :return: Un tuple (succès, message).
        """
        status, data = self._get_face_encoding_from_webcam()

        if status == "success":
            face_encoding = data
            np.save(self.known_face_encoding_path, face_encoding)
            self.known_face_encoding = face_encoding
            return True, "Votre visage a été appris avec succès."
        else:
            # data contient le message d'erreur
            return False, data

    def verify_face(self) -> tuple[bool, str]:
        """
        Vérifie si le visage devant la webcam correspond au visage appris.
        :return: Un tuple (succès, message).
        """
        if self.known_face_encoding is None:
            return False, "Aucun visage n'a été appris. Veuillez d'abord m'apprendre votre visage."

        status, data = self._get_face_encoding_from_webcam()

        if status != "success":
            return False, data # Retourne le message d'erreur ("no_face", etc.)

        unknown_encoding = data
        matches = face_recognition.compare_faces([self.known_face_encoding], unknown_encoding)

        if True in matches:
            return True, "Identification réussie. Bonjour !"
        else:
            return False, "Visage non reconnu."