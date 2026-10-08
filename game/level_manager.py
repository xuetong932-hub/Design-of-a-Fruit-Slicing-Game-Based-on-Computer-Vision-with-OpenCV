import random
import time

import cv2

class LevelManager:
    """Tracks stage goals and scales object difficulty as the player advances."""

    FRUITS_BY_LEVEL = {
        1: ["cherry", "peach", "banana", "apple", "orange"],
        2: ["cherry", "peach", "banana", "apple", "orange", "strawberry", "lemon", "grape"],
        3: [
            "cherry", "peach", "banana", "apple", "orange", "strawberry",
            "lemon", "grape", "watermelon", "kiwi", "mango", "pineapple",
        ],
    }

    def __init__(self):
        self.level = 1
        self.level_score = 0
        self.level_up_at = 0.0
        self.previous_level = None

    @property
    def target_score(self):
        return 15 + (self.level - 1) * 10

    @property
    def speed_range(self):
        speed_min = min(3 + self.level - 1, 12)
        speed_max = min(5 + (self.level - 1) * 2, 18)
        return speed_min, max(speed_min, speed_max)

    @property
    def bomb_probability(self):
        return min(0.06 + (self.level - 1) * 0.035, 0.38)

    @property
    def small_gift_probability(self):
        if self.level < 2:
            return 0.0
        return min(0.04 + (self.level - 2) * 0.005, 0.10)

    @property
    def large_gift_probability(self):
        if self.level < 4:
            return 0.0
        return min(0.02 + (self.level - 4) * 0.005, 0.06)

    def roll_object_type(self):
        """Choose a fruit, bomb, or (on later levels) a gift crate."""
        roll = random.random()
        large_gift = self.large_gift_probability
        if roll < large_gift:
            return "gift_large"
        roll -= large_gift

        small_gift = self.small_gift_probability
        if roll < small_gift:
            return "gift_small"
        roll -= small_gift

        if roll < self.bomb_probability:
            return "bomb"

        fruit_level = min(self.level, max(self.FRUITS_BY_LEVEL))
        return random.choice(self.FRUITS_BY_LEVEL[fruit_level])

    def add_points(self, points):
        """Add stage points and return every level reached by this award."""
        self.level_score += points
        reached = []
        while self.level_score >= self.target_score:
            self.level_score -= self.target_score
            self.previous_level = self.level
            self.level += 1
            reached.append(self.level)
        if reached:
            self.level_up_at = time.monotonic()
        return reached

    def draw_hud(self, frame, total_score):
        cv2.putText(
            frame, f"Score: {total_score}", (18, 32),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2,
        )
        cv2.putText(
            frame,
            f"Level {self.level}   Goal: {self.level_score}/{self.target_score}",
            (18, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2,
        )

        bar_x, bar_y, bar_width, bar_height = 18, 74, 210, 10
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (80, 80, 80), -1)
        progress = min(self.level_score / self.target_score, 1.0)
        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + int(bar_width * progress), bar_y + bar_height),
            (0, 210, 255),
            -1,
        )

        if self.level_up_at and time.monotonic() - self.level_up_at < 2.0:
            cv2.putText(
                frame,
                f"LEVEL {self.level}!",
                (190, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 255, 255),
                4,
            )
