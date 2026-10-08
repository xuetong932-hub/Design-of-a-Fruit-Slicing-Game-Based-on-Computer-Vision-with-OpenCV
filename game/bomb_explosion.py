import cv2
import math
import time


class BombExplosion:
    def __init__(self, center, max_radius=120, duration=0.4):
        self.cx, self.cy = center
        self.max_radius = max_radius
        self.duration = duration
        self.start_time = time.time()
        self.active = True

    def draw(self, frame):
        elapsed = time.time() - self.start_time
        progress = elapsed / self.duration

        if progress >= 1.0:
            self.active = False
            return

        radius = int(self.max_radius * progress)
        alpha = int(255 * (1 - progress))

        overlay = frame.copy()

        # Draw shockwave rings
        for r in range(radius, max(radius - 30, 0), -10):
            cv2.circle(overlay, (self.cx, self.cy), r, (0, 0, 255), 4)

        # Blend explosion
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
