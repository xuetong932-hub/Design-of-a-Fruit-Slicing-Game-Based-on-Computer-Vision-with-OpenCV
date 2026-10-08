import cv2
import config

def get_camera():
    # Windows webcams can work with one capture backend but not another.
    # Keep the configured camera index and try the common Windows backends.
    backends = (cv2.CAP_ANY, cv2.CAP_DSHOW, cv2.CAP_MSMF)

    for backend in backends:
        cap = cv2.VideoCapture(config.CAMERA_INDEX, backend)
        if not cap.isOpened():
            cap.release()
            continue

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

        # Some drivers report an open device but fail to provide frames.
        ok, _ = cap.read()
        if ok:
            return cap
        cap.release()

    raise RuntimeError(
        f"无法打开摄像头（索引 {config.CAMERA_INDEX}）。请关闭正在使用摄像头的软件，"
        "确认 Windows 已允许桌面应用访问摄像头，并检查 config.py 中的 CAMERA_INDEX。"
    )
