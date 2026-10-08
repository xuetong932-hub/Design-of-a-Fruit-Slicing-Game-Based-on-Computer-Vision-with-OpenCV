import cv2
import config

class Score:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def draw(self, frame):
        cv2.putText(
            frame,
            f"Score: {self.value}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            config.FONT_SCALE,
            config.COLOR_TEXT,
            config.FONT_THICKNESS
        )
