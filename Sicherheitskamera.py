import time  # Importieren Sie die time-Bibliothek
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import pygame
from datetime import datetime
import os

# Initialisierung von Pygame für Sound
pygame.mixer.init()

# Öffnen der Kamera
cap = cv2.VideoCapture(0)

# Variable zur Verfolgung des Soundstatus
sound_playing = False

# Schleife, um die Bilder von der Kamera zu lesen
while True:
    # Lesen Sie ein Bild von der Kamera
    ret, frame = cap.read()

    # Erkennen Sie Objekte im Bild mit cvlib
    bbox, label, conf = cv.detect_common_objects(frame)

    # Zeichnen Sie die erkannten Objekte auf dem Bild
    output_image = draw_bbox(frame, bbox, label, conf)

    # Überprüfe, ob eine Person im Bild erkannt wurde
    if 'person' in label:

        today = datetime.today().strftime('J%Y-M%m-T%d-H%H-M%M-S%S')
        # Erstellen Sie einen Dateinamen für das Bild
        filename = f'Erkennung{today}.jpg'
        # Erstellen Sie einen Ordner namens 'persons', wenn er nicht existiert
        if not os.path.exists('Erkennung'):
            os.mkdir('Erkennung')
        # Speichern Sie das Bild im Ordner 'persons' mit dem Dateinamen
        cv2.imwrite(os.path.join('Erkennung', filename), output_image)

        # Überprüfen, ob der Sound nicht bereits abgespielt wird
        if not sound_playing:
            # Laden und abspielen des Warnsounds
            pygame.mixer.music.load('Warning1_Adam.wav')
            pygame.mixer.music.play()

            # Setzen Sie den Soundstatus auf "wird abgespielt"
            sound_playing = True

            # Warten, bis der Sound vollständig abgespielt ist
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # Setzen Sie den Soundstatus auf "nicht abgespielt"
            sound_playing = False

    # Zeigen Sie das Bild in einem Fenster an
    cv2.imshow('output', output_image)

    # Beenden Sie die Schleife, wenn die Taste 'q' gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Schließen Sie die Kamera und das Fenster
cap.release()
cv2.destroyAllWindows()