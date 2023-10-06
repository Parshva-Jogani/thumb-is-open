import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tip_ids= [4, 8, 12, 16, 20]

def drawlandmarks(image, hand_landmarks):
    if hand_landmarks:
        for landmark in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmark, mp_hands.HAND_CONNECTIONS)

def countfinger(image, hand_landmarks, handNo = 0):
    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmark
        fingers = []
        for index in tip_ids:

            thumb_tip_y = landmarks[index].y
            thumb_bottom_y = landmarks[index-2].y

            if index != 4:
                if thumb_tip_y < thumb_bottom_y:
                    fingers.append(1)
                    print("thumb is close")
                    cv2.putText(image, "thumb is closed", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                if thumb_tip_y > thumb_bottom_y:
                    fingers.append(0)
                    print("thumb is open")    
                    cv2.putText(image, "thumb is open", (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)     
        total_fingers = fingers.count(1)         
                


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)

    results = hands.process(image)
    hand_landmarks = results.multi_hand_landmarks
    drawlandmarks(image, hand_landmarks)
    countfinger(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

