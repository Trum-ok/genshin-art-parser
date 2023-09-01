import os
import mss


def take_screenshot():
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.jpg")


def delete_screenshot():
    os.remove("screenshot.jpg")


if __name__ == "__main__":
    take_screenshot()
    # delete_screenshot()
