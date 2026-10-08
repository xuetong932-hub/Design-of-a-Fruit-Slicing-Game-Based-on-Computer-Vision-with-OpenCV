import cv2

class Lives:
    def __init__(self, total=3):
        self.total = total
        self.remaining = total

    def lose_life(self):
        if self.remaining > 0:
            self.remaining -= 1

    def is_dead(self):
        return self.remaining == 0

    def draw(self, frame):
        for i in range(self.remaining):
            cv2.circle(
                frame,
                (548 + i * 28, 40),
                12,
                (0, 0, 255),
                -1
            )
