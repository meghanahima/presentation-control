from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)
gesture_threshold = 300

def detect_gesture(frame):
    hands, img = detector.findHands(frame)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand["center"]
        if cy <= gesture_threshold:
            if fingers == [1, 1,1,1, 1]:
                return "next"
            elif fingers == [1, 0, 0, 0 ,0]:
                return "previous"
    return None
