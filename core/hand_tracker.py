import cv2
import mediapipe as mp
import config
from collections import deque


class HandTracker:
    def __init__(self):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_HANDS,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawer = mp.solutions.drawing_utils

        # 🔥 Trail storage
        self.trail = deque(maxlen=12)

    def get_finger_position(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            index_tip = hand.landmark[
                self.hands_module.HandLandmark.INDEX_FINGER_TIP
            ]

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Save for trail
            self.trail.append((x, y))

            if config.DRAW_HAND_LANDMARKS:
                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    self.hands_module.HAND_CONNECTIONS
                )

            # Sword tip
            cv2.circle(frame, (x, y), 8, config.COLOR_SWORD, -1)
            return x, y

        # If hand lost, clear trail
        self.trail.clear()
        return None

    def draw_trail(self, frame):
        for i in range(1, len(self.trail)):
            thickness = int(6 * (1 - i / len(self.trail)))

            # 🔒 SAFETY: OpenCV requires thickness >= 1
            thickness = max(1, thickness)

            cv2.line(
                frame,
                self.trail[i - 1],
                self.trail[i],
                (255, 255, 255),
                thickness
            )
