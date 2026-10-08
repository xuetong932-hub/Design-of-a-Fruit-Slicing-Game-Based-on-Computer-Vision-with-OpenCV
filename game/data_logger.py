import csv
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import config


class DataLogger:
    """Append anonymous gameplay events to a local CSV file."""

    FIELDS = [
        "session_id",
        "timestamp_utc",
        "elapsed_seconds",
        "event",
        "fruit_type",
        "input_x_norm",
        "input_y_norm",
        "target_x_norm",
        "target_y_norm",
        "score",
        "lives_remaining",
        "combo_count",
        "level",
        "level_score",
        "detail",
    ]

    def __init__(self, output_path="data/session_events.csv"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        # Preserve earlier assignment data if its CSV has the previous schema.
        if self.output_path.exists() and self.output_path.stat().st_size:
            with self.output_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
                existing_fields = next(csv.reader(csv_file), [])
            if existing_fields != self.FIELDS:
                base = self.output_path.with_name(f"{self.output_path.stem}_v2{self.output_path.suffix}")
                candidate = base
                version = 2
                while candidate.exists() and candidate.stat().st_size:
                    with candidate.open("r", newline="", encoding="utf-8-sig") as csv_file:
                        candidate_fields = next(csv.reader(csv_file), [])
                    if candidate_fields == self.FIELDS:
                        break
                    version += 1
                    candidate = self.output_path.with_name(
                        f"{self.output_path.stem}_v{version}{self.output_path.suffix}"
                    )
                self.output_path = candidate
        self.session_id = str(uuid.uuid4())
        self.started_at = time.monotonic()

    def log(
        self,
        event,
        *,
        fruit_type="",
        input_position=None,
        target_position=None,
        score=0,
        lives_remaining=0,
        combo_count=0,
        level=1,
        level_score=0,
        detail="",
    ):
        input_x, input_y = self._normalize(input_position)
        target_x, target_y = self._normalize(target_position)
        row = {
            "session_id": self.session_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "elapsed_seconds": round(time.monotonic() - self.started_at, 3),
            "event": event,
            "fruit_type": fruit_type,
            "input_x_norm": input_x,
            "input_y_norm": input_y,
            "target_x_norm": target_x,
            "target_y_norm": target_y,
            "score": score,
            "lives_remaining": lives_remaining,
            "combo_count": combo_count,
            "level": level,
            "level_score": level_score,
            "detail": detail,
        }
        write_header = not self.output_path.exists() or self.output_path.stat().st_size == 0
        with self.output_path.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELDS)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
            csv_file.flush()

    @staticmethod
    def _normalize(position):
        if position is None:
            return "", ""
        x, y = position
        return round(x / config.FRAME_WIDTH, 4), round(y / config.FRAME_HEIGHT, 4)
