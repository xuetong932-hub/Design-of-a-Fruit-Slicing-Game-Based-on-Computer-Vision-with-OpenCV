import random
import time
from pathlib import Path

import cv2
import numpy as np

import config


FRUIT_COLORS = {
    "apple": (40, 45, 220),
    "orange": (0, 145, 255),
    "strawberry": (35, 35, 230),
    "lemon": (40, 220, 245),
    "grape": (175, 65, 150),
    "watermelon": (50, 180, 65),
    "kiwi": (70, 155, 100),
    "mango": (0, 180, 245),
    "pineapple": (0, 190, 235),
    "bomb": (35, 35, 35),
    "gift_small": (25, 175, 245),
    "gift_large": (15, 125, 235),
}


def _draw_procedural_sprite(kind, size):
    """Build a small transparent sprite for fruits that have no supplied PNG."""
    image = np.zeros((size, size, 4), dtype=np.uint8)
    center = (size // 2, size // 2 + 4)
    color = FRUIT_COLORS.get(kind, (100, 180, 230))

    if kind in ("gift_small", "gift_large"):
        inset = 11 if kind == "gift_small" else 7
        cv2.rectangle(image, (inset, inset + 8), (size - inset, size - inset), color + (255,), -1)
        cv2.rectangle(image, (inset, inset + 8), (size - inset, size - inset), (80, 55, 25, 255), 3)
        ribbon = (35, 45, 230, 255)
        cv2.rectangle(image, (size // 2 - 6, inset + 8), (size // 2 + 6, size - inset), ribbon, -1)
        cv2.rectangle(image, (inset, size // 2 - 4), (size - inset, size // 2 + 7), ribbon, -1)
        cv2.ellipse(image, (size // 2 - 8, inset + 4), (9, 6), -25, 0, 360, ribbon, -1, cv2.LINE_AA)
        cv2.ellipse(image, (size // 2 + 8, inset + 4), (9, 6), 25, 0, 360, ribbon, -1, cv2.LINE_AA)
        return image

    if kind == "bomb":
        cv2.circle(image, center, size // 3, color + (255,), -1, cv2.LINE_AA)
        cv2.circle(image, center, size // 3, (180, 180, 180, 255), 3, cv2.LINE_AA)
        cv2.line(image, (center[0] + 14, center[1] - 19), (center[0] + 25, center[1] - 31), (0, 150, 255, 255), 5, cv2.LINE_AA)
        cv2.circle(image, (center[0] + 27, center[1] - 33), 4, (0, 225, 255, 255), -1, cv2.LINE_AA)
        return image

    if kind == "grape":
        cluster = [(32, 35), (47, 31), (24, 49), (40, 49), (56, 48), (32, 63), (47, 64)]
        for x, y in cluster:
            cv2.circle(image, (int(x * size / 80), int(y * size / 80)), max(4, size // 10), color + (255,), -1, cv2.LINE_AA)
        cv2.ellipse(image, (size // 2 + 4, size // 5), (size // 7, size // 12), -25, 0, 360, (45, 160, 50, 255), -1, cv2.LINE_AA)
        cv2.line(image, (size // 2, size // 5), (size // 2 + 2, size // 3), (55, 95, 25, 255), 3, cv2.LINE_AA)
        return image

    if kind == "watermelon":
        cv2.circle(image, center, size // 3, (35, 155, 55, 255), -1, cv2.LINE_AA)
        cv2.circle(image, center, size // 4, (45, 65, 225, 255), -1, cv2.LINE_AA)
        for dx in (-12, 12):
            cv2.ellipse(image, (center[0] + dx, center[1]), (3, size // 5), 0, 0, 360, (25, 115, 45, 255), -1, cv2.LINE_AA)
        for dx, dy in [(-7, -9), (7, 2), (-4, 12)]:
            cv2.ellipse(image, (center[0] + dx, center[1] + dy), (2, 4), 25, 0, 360, (25, 25, 35, 255), -1, cv2.LINE_AA)
        return image

    if kind == "strawberry":
        points = np.array([
            [size // 2, size - 8], [size // 6, size // 2],
            [size // 4, size // 3], [size // 2, size // 2 - 5],
            [size * 3 // 4, size // 3], [size * 5 // 6, size // 2],
        ], dtype=np.int32)
        cv2.fillPoly(image, [points], color + (255,), cv2.LINE_AA)
        for x, y in [(27, 36), (40, 43), (53, 36), (34, 55), (48, 58), (40, 68)]:
            cv2.circle(image, (int(x * size / 80), int(y * size / 80)), max(1, size // 32), (30, 220, 245, 255), -1, cv2.LINE_AA)
        cv2.ellipse(image, (size // 2, size // 4), (size // 5, size // 12), 0, 0, 360, (45, 160, 55, 255), -1, cv2.LINE_AA)
        return image

    # Most round fruits share a body and leaf; small markings distinguish them.
    if kind == "kiwi":
        cv2.circle(image, center, size // 3, (45, 100, 60, 255), -1, cv2.LINE_AA)
        cv2.circle(image, center, size // 4, (70, 185, 105, 255), -1, cv2.LINE_AA)
        cv2.circle(image, center, size // 14, (225, 240, 210, 255), -1, cv2.LINE_AA)
        for angle in range(0, 360, 45):
            x = center[0] + int(size // 6 * np.cos(np.radians(angle)))
            y = center[1] + int(size // 6 * np.sin(np.radians(angle)))
            cv2.ellipse(image, (x, y), (2, 4), angle, 0, 360, (35, 55, 35, 255), -1, cv2.LINE_AA)
    elif kind == "pineapple":
        cv2.ellipse(image, center, (size // 4, size // 3), 0, 0, 360, color + (255,), -1, cv2.LINE_AA)
        for offset in range(-14, 15, 9):
            cv2.line(image, (center[0] - 15, center[1] + offset), (center[0] + 15, center[1] + offset + 8), (35, 125, 180, 255), 2, cv2.LINE_AA)
        for offset in (-12, 0, 12):
            cv2.ellipse(image, (center[0] + offset, size // 6), (5, 13), offset, 0, 360, (40, 145, 45, 255), -1, cv2.LINE_AA)
    else:
        axes = (size // 3, size // 3 + (5 if kind in ("lemon", "mango") else 0))
        cv2.ellipse(image, center, axes, -12 if kind == "mango" else 0, 0, 360, color + (255,), -1, cv2.LINE_AA)
        cv2.ellipse(image, (center[0] - 9, center[1] - 12), (size // 11, size // 6), -20, 0, 360, (255, 255, 255, 75), -1, cv2.LINE_AA)
        if kind == "apple":
            cv2.ellipse(image, (center[0], center[1] - size // 3), (size // 16, size // 9), 0, 0, 360, (55, 70, 40, 255), -1, cv2.LINE_AA)
        if kind in ("orange", "lemon"):
            cv2.circle(image, center, size // 3, (30, 120, 220, 100), 2, cv2.LINE_AA)
        if kind == "mango":
            cv2.ellipse(image, (center[0] + 12, center[1] - 20), (size // 7, size // 12), -30, 0, 360, (40, 145, 45, 255), -1, cv2.LINE_AA)

    if kind not in ("lemon",):
        cv2.ellipse(image, (size // 2 + 10, size // 5), (size // 7, size // 12), -25, 0, 360, (45, 155, 50, 255), -1, cv2.LINE_AA)
        cv2.line(image, (size // 2, size // 5), (size // 2 + 2, size // 3), (55, 95, 25, 255), 3, cv2.LINE_AA)
    return image


class Fruit:
    GIFT_HITS = {"gift_small": 5, "gift_large": 10}
    GIFT_REWARDS = {"gift_small": 15, "gift_large": 40}
    GIFT_HIT_INTERVAL = 0.35

    def __init__(self, level_manager):
        self.level_manager = level_manager
        self.reset()

    @property
    def is_gift(self):
        return self.type in self.GIFT_HITS

    @property
    def gift_reward(self):
        return self.GIFT_REWARDS.get(self.type, 0)

    def load_image(self):
        image_path = config.FRUIT_IMAGES.get(self.type)
        if image_path:
            full_path = Path(__file__).resolve().parent.parent / image_path
            image = cv2.imread(str(full_path), cv2.IMREAD_UNCHANGED)
            if image is not None:
                if image.ndim == 3 and image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                return cv2.resize(image, (config.FRUIT_SIZE, config.FRUIT_SIZE))
        return _draw_procedural_sprite(self.type, config.FRUIT_SIZE)

    def reset(self):
        self.type = self.level_manager.roll_object_type()
        self.x = random.randint(50, config.FRAME_WIDTH - 50)
        self.y = config.FRUIT_SPAWN_Y
        if self.type in self.GIFT_HITS:
            # Give players enough time to make the repeated hand movements needed
            # to open a crate, even after the normal targets become very fast.
            self.speed = 1
        else:
            speed_min, speed_max = self.level_manager.speed_range
            self.speed = random.randint(speed_min, speed_max)
        self.radius = config.FRUIT_SIZE // 2
        self.image = self.load_image()
        self.hits_required = self.GIFT_HITS.get(self.type, 0)
        self.hits_remaining = self.hits_required
        self.last_gift_hit = 0.0
        self.gift_armed = True

    def update(self):
        self.y += self.speed
        if self.y > config.FRAME_HEIGHT:
            self.reset()

    def register_gift_hit(self):
        """Count one hit, then require the tracked fingertip to leave the crate."""
        now = time.monotonic()
        if not self.gift_armed or now - self.last_gift_hit < self.GIFT_HIT_INTERVAL:
            return "cooldown"
        self.last_gift_hit = now
        self.gift_armed = False
        self.hits_remaining -= 1
        return "opened" if self.hits_remaining <= 0 else "progress"

    def arm_gift(self):
        self.gift_armed = True

    def draw(self, frame):
        h, w, _ = frame.shape
        size = config.FRUIT_SIZE
        x1 = self.x - size // 2
        y1 = self.y - size // 2
        x2 = x1 + size
        y2 = y1 + size

        if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
            return

        fruit_img = self.image[:, :, :3]
        alpha = self.image[:, :, 3] / 255.0
        roi = frame[y1:y2, x1:x2]
        for channel in range(3):
            roi[:, :, channel] = (
                alpha * fruit_img[:, :, channel]
                + (1 - alpha) * roi[:, :, channel]
            )

        if self.is_gift:
            text = f"{self.hits_remaining}/{self.hits_required} cuts"
            label_y = min(y2 + 22, h - 8)
            cv2.putText(frame, text, (max(4, x1 - 5), label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 255), 2)
