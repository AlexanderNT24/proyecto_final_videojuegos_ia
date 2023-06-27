import cv2
import mediapipe as mp


def detect_hand_raised(hand_landmarks):
    # Obtiene las coordenadas de la muñeca y las puntas de los dedos de la mano derecha e izquierda
    wrist_left = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x
    wrist_right = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x
    thumb_tip_left = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y
    thumb_tip_right = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y
    index_finger_tip_left = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
    index_finger_tip_right = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y

    if wrist_left < index_finger_tip_left and wrist_left < thumb_tip_left:
        return 'right'
    elif wrist_right > index_finger_tip_right and wrist_right > thumb_tip_right:
        return 'left'
    else:
        return 'none'

def main():
    cap = cv2.VideoCapture(0)  # Abre la cámara web
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convierte la imagen de BGR a RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecta las manos en la imagen
        results = hands.process(image_rgb)

        # Dibuja los puntos y las conexiones en las manos detectadas
        image_output = frame.copy()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_color = (0, 0, 255)  
                connection_color = (0, 255, 0)  
                mp_drawing.draw_landmarks(image_output, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=2,
                                                                                         circle_radius=3),
                                          connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2))
                data_to_send = detect_hand_raised(hand_landmarks)
                f = open ('file.txt','w')
                f.write(data_to_send)
                f.close()

        # Muestra la imagen resultante
        cv2.imshow('Controller VideoGame', image_output)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
