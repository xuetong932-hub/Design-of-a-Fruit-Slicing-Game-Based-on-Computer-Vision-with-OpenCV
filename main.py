import cv2
import config

from core.camera import get_camera
from core.hand_tracker import HandTracker
from core.collision import is_sliced

from game.fruit import Fruit
from game.score import Score
from game.lives import Lives
from game.combo import Combo
from game.data_logger import DataLogger
from game.sound_manager import SoundManager
from game.bomb_explosion import BombExplosion
from game.level_manager import LevelManager


def main():
    cap = get_camera()
    tracker = HandTracker()

    level_manager = LevelManager()
    fruits = [Fruit(level_manager) for _ in range(3)]
    score = Score()
    lives = Lives(3)
    combo = Combo()
    sounds = SoundManager()

    explosion = None
    game_over = False
    logger = DataLogger()
    end_reason = "quit"

    def log_progress(event, *, fruit_type="", input_position=None, target_position=None, detail=""):
        logger.log(
            event,
            fruit_type=fruit_type,
            input_position=input_position,
            target_position=target_position,
            score=score.value,
            lives_remaining=lives.remaining,
            combo_count=combo.count,
            level=level_manager.level,
            level_score=level_manager.level_score,
            detail=detail,
        )

    def award_points(points, reason):
        score.value += points
        return level_manager.add_points(points)

    def log_level_ups(reached_levels, points, reason):
        for reached_level in reached_levels:
            log_progress(
                "level_up",
                detail=(
                    f"level_reached={reached_level};points_awarded={points};"
                    f"next_goal={level_manager.target_score};source={reason}"
                ),
            )

    log_progress("session_start")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                end_reason = "camera_error"
                break

            frame = cv2.flip(frame, 1)
            finger_pos = tracker.get_finger_position(frame)
            tracker.draw_trail(frame)

            for fruit in fruits:
                fruit_type = fruit.type
                previous_position = (fruit.x, fruit.y)
                missed = fruit.y + fruit.speed > config.FRAME_HEIGHT
                fruit.update()
                fruit_position = previous_position if missed else (fruit.x, fruit.y)

                if missed:
                    event = "gift_missed" if fruit_type.startswith("gift_") else (
                        "bomb_avoided" if fruit_type == "bomb" else "fruit_missed"
                    )
                    log_progress(
                        event,
                        fruit_type=fruit_type,
                        input_position=finger_pos,
                        target_position=fruit_position,
                        detail=f"level={level_manager.level};level_score={level_manager.level_score}",
                    )
                    continue

                fruit.draw(frame)

                sliced = is_sliced(finger_pos, (fruit.x, fruit.y), fruit.radius)
                if fruit.is_gift and not sliced:
                    fruit.arm_gift()
                if not sliced:
                    continue

                if fruit.is_gift:
                    hit_result = fruit.register_gift_hit()
                    if hit_result == "cooldown":
                        continue
                    if hit_result == "progress":
                        log_progress(
                            "gift_hit",
                            fruit_type=fruit_type,
                            input_position=finger_pos,
                            target_position=fruit_position,
                            detail=f"hits_remaining={fruit.hits_remaining};hits_required={fruit.hits_required}",
                        )
                        continue

                    reward = fruit.gift_reward
                    required_hits = fruit.hits_required
                    reached_levels = award_points(reward, fruit_type)
                    log_progress(
                        "gift_opened",
                        fruit_type=fruit_type,
                        input_position=finger_pos,
                        target_position=fruit_position,
                        detail=f"hits_required={required_hits};points_awarded={reward}",
                    )
                    log_level_ups(reached_levels, reward, fruit_type)
                    sounds.play_combo(3)
                    if reached_levels:
                        for item in fruits:
                            item.reset()
                    else:
                        fruit.reset()
                    continue

                if fruit.type == "bomb":
                    sounds.play_bomb()
                    explosion = BombExplosion((fruit.x, fruit.y))
                    lives.lose_life()
                    fruit.reset()
                    combo.count = 0
                    log_progress(
                        "bomb_hit",
                        fruit_type="bomb",
                        input_position=finger_pos,
                        target_position=fruit_position,
                    )

                    if lives.is_dead():
                        sounds.play_game_over()
                        game_over = True
                    continue

                combo.register_slice()
                if combo.count == 1:
                    sounds.play_slice()
                else:
                    sounds.play_combo(combo.count)

                bonus = combo.get_bonus()
                points = 1 + bonus
                reached_levels = award_points(points, fruit_type)
                log_progress(
                    "fruit_sliced",
                    fruit_type=fruit_type,
                    input_position=finger_pos,
                    target_position=fruit_position,
                    detail=f"points_awarded={points};level={level_manager.level}",
                )
                log_level_ups(reached_levels, points, fruit_type)
                if reached_levels:
                    for item in fruits:
                        item.reset()
                else:
                    fruit.reset()

            level_manager.draw_hud(frame, score.value)
            lives.draw(frame)

            if combo.count >= 2:
                cv2.putText(
                    frame,
                    f"COMBO x{combo.count}!",
                    (245, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    3,
                )

            if explosion and explosion.active:
                explosion.draw(frame)

            if game_over and (not explosion or not explosion.active):
                cv2.putText(
                    frame,
                    "GAME OVER",
                    (160, 240),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 255),
                    4,
                )
                cv2.imshow("Fruit Ninja CV", frame)
                cv2.waitKey(2000)
                end_reason = "game_over"
                break

            cv2.imshow("Fruit Ninja CV", frame)
            if cv2.waitKey(1) & 0xFF == config.ESC_KEY:
                break
    finally:
        log_progress("session_end", detail=end_reason)
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
