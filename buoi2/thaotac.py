from pynput import mouse, keyboard
import logging
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="Ghi nhận sự kiện")
parser.add_argument(
    "-l", "--logfile",
    default="events.log",
    help="File log"
)

args = parser.parse_args()

log_path = Path(args.logfile)
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
def on_move(x, y):
    logging.info(f"Move ({x},{y})")

def on_click(x, y, button, pressed):
    logging.info(f"{'Press' if pressed else 'Release'} {button} at ({x},{y})")

def on_press(key):
    logging.info(f"Key: {key}")

    if key == keyboard.Key.esc:
        logging.info("Nhấn ESC → thoát")
        return False

def main():
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click
    )

    keyboard_listener = keyboard.Listener(
        on_press=on_press
    )

    mouse_listener.start()
    keyboard_listener.start()

    logging.info("Đang ghi nhận... Nhấn ESC để dừng")

    keyboard_listener.join()
    mouse_listener.stop()

if __name__ == "__main__":
    main()
