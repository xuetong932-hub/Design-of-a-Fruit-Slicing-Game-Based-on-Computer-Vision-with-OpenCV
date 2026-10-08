import math

def is_sliced(finger_pos, fruit_pos, radius):
    if finger_pos is None:
        return False

    fx, fy = fruit_pos
    x, y = finger_pos
    distance = math.hypot(x - fx, y - fy)

    return distance < radius
