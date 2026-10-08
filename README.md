# Fruit Ninja CV — Hand-Gesture-Controlled Game

Real-time hand-gesture-controlled arcade game built with **OpenCV** and **MediaPipe Hands**.
The webcam tracks the player's hand; the index fingertip acts as a virtual blade — no controller needed.

> **Attribution & license**
> This repository is a **derived work**, forked from
> [`Alexrohith/Fruit-Ninja-CV-Hand-Gesture-Controlled-Game-using-OpenCV-MediaPipe`](https://github.com/Alexrohith/Fruit-Ninja-CV-Hand-Gesture-Controlled-Game-using-OpenCV-MediaPipe)
> (MIT License, © 2026 Alex Rohith I). The original camera loop, hand-tracking module,
> collision primitive, scoring/combo logic and all art/audio assets are the work of the
> original author and are used under the terms of the MIT License.
>
> **My contributions** are listed explicitly in [What I Added](#what-i-added). The original
> `LICENSE` file is preserved unmodified. If you fork this further, keep the copyright notice.

---

## What I Added

The upstream project was a single-level demo with 4 fruit types, a hard-coded webcam open,
and no instrumentation. I extended it into a structured, instrumented application:

### 1. Cross-platform camera acquisition (`core/camera.py`)
The original `cv2.VideoCapture(index)` silently returned unusable captures on some Windows
webcams — the device opened but returned no frames. I replaced it with a backend-probing
fallback chain:

```python
backends = (cv2.CAP_ANY, cv2.CAP_DSHOW, cv2.CAP_MSMF)
```

Each backend is validated by **actually decoding a frame**, not just by `isOpened()` — because
a capture can report success and still be dead. Failures raise an actionable error naming the
likely causes (camera in use / Windows permission / wrong index) instead of a bare OpenCV error.

### 2. Session telemetry pipeline (`game/data_logger.py`)
Added a structured event logger that appends 16 normalised fields per event to
`data/session_events*.csv`. Design points:

- **Coordinates normalised to `[0, 1]`** by frame dimensions, so runs at different resolutions
  are directly comparable and the data is resolution-independent.
- **Schema-drift safe**: if an existing CSV has an older column set, the writer automatically
  redirects to a new `*_v2` / `_v3` file instead of corrupting prior data.
- **Privacy-preserving by construction**: stores coordinates and game state only — never webcam
  frames or video. Session IDs are random UUIDs, so runs cannot be linked to a person.
- Records 10 event types (`fruit_sliced`, `bomb_hit`, `gift_opened`, `level_up`, …) plus
  level, score, lives, and combo count, making the data usable for gameplay-balance analysis.

### 3. Progressive difficulty system (`game/level_manager.py`)
Replaced fixed difficulty with level-driven parameters that scale independently:

| Parameter | Scaling |
|---|---|
| Level goal | `15 + 10 × (level − 1)` points |
| Object speed | `min(3 + level − 1, 12)` … `min(5 + 2(level − 1), 18)` |
| Bomb probability | `min(0.06 + 0.035(level − 1), 0.38)` |
| Gift probability | unlocked at level 2 (small) / level 4 (large) |

Object selection uses a **weighted roll** rather than `random.choice`, so bombs and gifts
compete with ordinary fruit inside one probability budget. Fruits unlock by level tier.
The manager also renders an on-canvas HUD with a goal-progress bar and a level-up flash.

### 4. Procedural sprite generation (`game/fruit.py`)
The original loaded 4 PNG sprites. Rather than hunting for 12 more image files, I wrote a
generator that **draws** the remaining fruits and gift crates with OpenCV primitives
(`fillPoly`, `ellipse`, `LINE_AA`) onto transparent BGRA canvases. This kept the repo small
and made every asset reproducible from code. `load_image()` now falls back to the generator
whenever a PNG is missing, and converts 3-channel BGR assets to BGRA.

### 5. Multi-hit gift interaction (`game/fruit.py`, `main.py`)
Gift crates require **repeated in-and-out hand movements** (5 hits → 15 pts, 10 hits → 40 pts)
rather than a single contact. This needed a debounce state machine — a hit only counts after
the fingertip leaves the crate:

```
slice detected → register_gift_hit() → "cooldown" if inside 350 ms window
                                   → "progress" if hits remain
                                   → "opened"  when hits_required reached
not sliced    → arm_gift()  (re-arms only after the hand withdraws)
```

This prevents one fast swipe from registering as several hits, and demonstrates a general
pattern for **debounced gesture recognition** on noisy real-time input.

### 6. Other changes
- `main.py` restructured from 115 → 219 lines, with the game loop decomposed into named
  helpers and a single `log_progress()` funnel so every event is recorded consistently.
- Dependency pinning (`opencv-contrib-python==4.11.0.86`, `mediapipe==0.10.21`, `numpy<2`)
  because `numpy≥2` breaks MediaPipe 0.10.x, and unpinned OpenCV builds disagreed on the
  `cv2` namespace.
- `.gitignore` extended to exclude local telemetry output and IDE folders.
- `运行游戏.bat` launcher for Windows with a guard when the virtualenv is missing.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Hand tracking | MediaPipe Hands (`static_image_mode=False`, 21 landmarks) |
| Image processing | OpenCV 4.11 (`opencv-contrib-python`) |
| Numerical | NumPy |
| Game loop & audio | Pygame |
| Language | Python 3.12 |

## How It Works

```
webcam frame
    → cv2.flip (mirror selfie view)
    → BGR→RGB conversion
    → MediaPipe Hands.process()  ──► 21 hand landmarks
    → INDEX_FINGER_TIP × (w, h)  ──► pixel-space fingertip
    → deque(maxlen=12) trail     ──► tapered blade trail
    → distance-to-centre test    ──► collision with fruit radius
```

`min_detection_confidence` and `min_tracking_confidence` are both set to `0.7`, and the
trail is cleared whenever the hand leaves frame so the blade does not smear across cuts.

## Features

- Real-time webcam gameplay at 640×480
- 12 fruit types + bombs + two gift-crate tiers
- 3-hit / multi-slice combo scoring with a 0.35 s window
- 3-life system, bomb penalty, explosion animation
- Progressive levels with per-level speed / bomb / gift tuning
- Gift crates needing 5 or 10 debounced in-and-out hand movements
- Blade trail, HUD with level progress bar, sound effects
- Anonymous session telemetry to CSV

## Project Structure

```
Fruit-Ninja-CV/
├── main.py                  # game loop + event logging (extended)
├── config.py                # all tunables (extended: 15 object types)
├── requirements.txt         # pinned dependencies
├── core/
│   ├── camera.py            # ← rewritten: multi-backend probing
│   ├── hand_tracker.py      #     MediaPipe wrapper + trail
│   └── collision.py         #     distance-based hit test
├── game/
│   ├── fruit.py             # ← extended: procedural sprites, gift FSM
│   ├── level_manager.py     # ← new: difficulty scaling, weighted rolls, HUD
│   ├── data_logger.py       # ← new: CSV telemetry pipeline
│   ├── score.py  lives.py  combo.py
│   ├── sound_manager.py  bomb_explosion.py
├── CREDITS.md                # fork attribution
└── assets/
    ├── fruits/              # 4 original PNGs; others are generated
    └── sounds/
```

## Getting Started

### Requirements
- Python 3.10–3.12 (MediaPipe 0.10.x does not support 3.13+)
- A webcam

### Install & run

**Windows**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

Or double-click **`运行游戏.bat`**.

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The webcam preview opens mirrored. Press **Esc** to end a session.

> On Linux you may need `sudo apt install libgl1 libglib2.0-0` for OpenCV.

## Telemetry

Each run appends to `data/session_events.csv` (git-ignored). Columns:

`session_id, timestamp_utc, elapsed_seconds, event, fruit_type, input_x_norm, input_y_norm, target_x_norm, target_y_norm, score, lives_remaining, combo_count, level, level_score, detail`

A typical session produces 90+ events. To explore it:

```python
import pandas as pd
df = pd.read_csv("data/session_events.csv")
df[df.event == "fruit_sliced"].describe()[["input_x_norm", "target_x_norm"]]
```

No frames or video are stored — only coordinates and game state.

## Possible Next Steps

- Session analytics: accuracy and reaction-time distributions from the CSV
- Temporal smoothing (One Euro filter) on the fingertip to cut jitter
- Handedness detection and two-hand tracking
- Model-based classification (pointing / open palm / fist) instead of a single landmark
- Recorded demo GIF for the README

## Credits

- Original project and assets: [Alex Rohith I](https://github.com/Alexrohith) — MIT License
- [MediaPipe](https://mediapipe.dev) by Google
- [OpenCV](https://opencv.org)

## License

MIT — see [LICENSE](LICENSE). The `Copyright (c) 2026 Alex Rohith I` notice covers the
inherited original work and is preserved as required by the MIT License.
