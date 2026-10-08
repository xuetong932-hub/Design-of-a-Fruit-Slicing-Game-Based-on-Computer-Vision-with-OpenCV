import time

class Combo:
    def __init__(self, window=0.35):
        self.window = window      # seconds allowed between slices
        self.last_slice_time = 0
        self.count = 0

    def register_slice(self):
        now = time.time()
        if now - self.last_slice_time <= self.window:
            self.count += 1
        else:
            self.count = 1
        self.last_slice_time = now

    def get_bonus(self):
        if self.count >= 3:
            return 3   # big combo
        elif self.count == 2:
            return 1   # small combo
        return 0
