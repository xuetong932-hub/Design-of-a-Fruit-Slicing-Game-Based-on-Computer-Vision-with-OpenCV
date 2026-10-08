# Credits

## Original work

This repository is a derived work. The following is the upstream project:

**Fruit Ninja CV – Hand Gesture Controlled Game using OpenCV & MediaPipe**
<https://github.com/Alexrohith/Fruit-Ninja-CV-Hand-Gesture-Controlled-Game-using-OpenCV-MediaPipe>
Copyright © 2026 **Alex Rohith I** — MIT License

### Inherited from upstream (unchanged or lightly modified)

| File | Contribution |
|---|---|
| `core/hand_tracker.py` | MediaPipe Hands wrapper, 21-landmark access, index-fingertip mapping, tapered trail rendering |
| `core/collision.py` | Distance-to-centre hit test |
| `game/score.py`, `game/lives.py` | Score and life counters |
| `game/combo.py` | Time-window combo detection |
| `game/sound_manager.py` | Pygame mixer wrapper and effect playback |
| `game/bomb_explosion.py` | Explosion animation |
| `assets/fruits/*.png` | Sprite artwork (banana, bomb, cherry, peach) |
| `assets/sounds/*.wav` | Sound effects |

### Added or substantially rewritten in this fork

| File | Contribution |
|---|---|
| `core/camera.py` | Multi-backend camera acquisition with real frame validation |
| `game/data_logger.py` | CSV session telemetry pipeline with schema-drift protection |
| `game/level_manager.py` | Progressive difficulty scaling, weighted object rolls, HUD |
| `game/fruit.py` | Procedural OpenCV sprite generation, gift-crate hit state machine |
| `main.py` | Restructured game loop, gift logic, unified event logging |
| `config.py` | Expanded object registry, pinned tunables |
| `requirements.txt` | Pinned, working dependency set |
| `.gitignore`, `README.md` | Repository hygiene and documentation |

The original MIT `LICENSE` file is preserved unmodified at the repository root, as the
MIT License requires. This `CREDITS.md` file is an addition by this fork's author and is
distributed under the same terms.
