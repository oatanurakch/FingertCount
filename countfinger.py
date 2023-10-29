import cv2
import mediapipe as mp
from serial import Serial
from time import sleep

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_hands.Hands(
  model_complexity = 0,
  min_detection_confidence = 0.5,
  min_tracking_confidence = 0.5) as hands:
  while capture.isOpened():
    success, image = capture.read()
    if not success:
      print('Ignored empty webcam\'s frame')
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fingerCount = 0
    fingerlabel = []

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label

        handLandmarks = []

        for landmarks in hand_landmarks.landmark:
          handLandmarks.append([landmarks.x, landmarks.y])
        
        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Thumb")
        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Thumb")

        if handLandmarks[8][1] < handLandmarks[6][1]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Index")
        if handLandmarks[12][1] < handLandmarks[10][1]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Middle")
        if handLandmarks[16][1] < handLandmarks[14][1]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Ring")
        if handLandmarks[20][1] < handLandmarks[18][1]:
          fingerCount = fingerCount + 1
          fingerlabel.append("Little")

        mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style()
        )
    
    # set text label of finger found
    fingerFound = ''
    if fingerlabel != []:
      for idx in range(len(fingerlabel)):
        if idx == len(fingerlabel) - 1:
          fingerFound += fingerlabel[idx]
        else:
          fingerFound += fingerlabel[idx] + ', '

    # Append text finger found to image
    cv2.rectangle(image, (0,440), (640,480), (0,0,0), -1)
    cv2.putText(image, fingerFound, (20, 470), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
    # Append text finger count to image
    cv2.rectangle(image, (0,0), (100,100), (0,0,0), -1)
    cv2.putText(image, str(fingerCount), (20,80), cv2.FONT_HERSHEY_DUPLEX, 3, (0,255,0), 10)
    cv2.imshow('FingerCounting Apps', image)
    try:
      with Serial('COM10', 115200, timeout = 1) as ser:
          ser.setDTR(True)
          ser.setRTS(False)
          ser.write(str(fingerCount).encode())
    except:
      print("Serial Error")
      
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

capture.release()