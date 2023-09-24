import os
import sys
import json
import ctypes
import ctypes.wintypes
import collections
from ctypes import c_long
from typing import Tuple

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP


def resource_path(relative_path) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def check_dir_exists(exe_path, config_path, default_path, nothing_path):
    presets_dir = 'presets'

    if not os.path.exists(f"{exe_path}\\{presets_dir}\\"):
        os.makedirs(f"{exe_path}\\{presets_dir}")

    if not os.path.exists(config_path):
        with open(config_path, 'w') as json_file:
            json.dump(
                {
                    "presets": [
                        "nothing",
                        "default"
                    ],
                    "path_to_tesseract": "tesseract",
                    "language": "rus",
                    "app_theme": "dark",
                    "auto_open_genshin": "True",
                    "screen_ratio": "16:9"
                }, json_file, ensure_ascii=False

            )

    if not os.path.exists(default_path):
        with open(default_path, 'w') as json_file:
            json.dump({"sets": [],
                       "sands": [], "goblet": [], "circlet": ["Шанс крит. попадания", "Крит. урон"],
                       "sands_d": [], "goblet_d": [], "circlet_d": [],
                       "substats": ["Шанс крит. попадания", "Крит. урон"]},
                      json_file, ensure_ascii=False)

    if not os.path.exists(nothing_path):
        with open(nothing_path, 'w') as json_file:
            json.dump({"sets": [],
                       "sands": [], "goblet": [], "circlet": [],
                       "sands_d": [], "goblet_d": [], "circlet_d": [],
                       "substats": []},
                      json_file, ensure_ascii=False)


def path_and_dir() -> Tuple[str, str, str, str]:
    presets_dir = 'presets'
    exe_dir = os.path.dirname(sys.executable)
    # exe_dir = 'C:\\Users\\TrumW\\PycharmProjects\\artparser'
    # exe_dir = 'C:\\Users\\TrumW\\PycharmProjects\\artparser\\dist'
    config_path = resource_path(f'{exe_dir}\\{presets_dir}\\config.json')
    default_path = resource_path(f'{exe_dir}\\{presets_dir}\\default.json')
    nothing_path = resource_path(f'{exe_dir}\\{presets_dir}\\nothing.json')
    return exe_dir, config_path, default_path, nothing_path


def config_info(config_path):
    # check_dir_exists()

    with open(config_path, 'r') as json_file:
        data = json.load(json_file)
        # presets = data['presets']
        # tesseract_path = data['path_to_tesseract']
        # language = data['language']
    # return presets, tesseract_path
    return data


Point = collections.namedtuple("Point", "x y")


class UtilsException(Exception):
    pass


class FailSafeException(UtilsException):
    """
    This exception is raised by functions when the user puts the mouse cursor into one of the "failsafe
    points" (by default, one of the four corners of the primary monitor). This exception shouldn't be caught; it's
    meant to provide a way to terminate a misbehaving script.
    """

    pass


def failSafeCheck():
    if tuple(position()) in [(0, 0)]:
        raise FailSafeException(
            "Fail-safe triggered from mouse moving to a corner of the screen."
        )


def moveTo(x, y):
    failSafeCheck()
    _mouseMoveDrag(x, y, 0, 0)


def _moveTo(x, y):
    failSafeCheck()
    ctypes.windll.user32.SetCursorPos(x, y)


def _position() -> tuple[c_long, c_long]:
    """Returns the current xy coordinates of the mouse cursor as a two-integer
    tuple by calling the GetCursorPos() win32 function.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.
    """

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return cursor.x, cursor.y


def position(x=None, y=None):
    """
    Returns the current xy coordinates of the mouse cursor as a two-integer tuple.

    Args:
      x (int, None, optional) - If not None, this argument overrides the x in
        the return value.
      y (int, None, optional) - If not None, this argument overrides the y in
        the return value.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.

    NOTE: The position() function doesn't check for failsafe.
    """
    posx, posy = _position()
    posx = int(posx)
    posy = int(posy)
    if x is not None:  # If set, the x parameter overrides the return value.
        posx = int(x)
    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)
    return Point(posx, posy)


def click(x=None, y=None):
    if x is None and y is None:
        x, y = position()
    try:
        failSafeCheck()
        _sendMouseEvent(x, y)
    except (PermissionError, OSError):
        # TODO: We need to figure out how to prevent these errors, see https://github.com/asweigart/pyautogui/issues/60
        pass


def _sendMouseEvent(x, y):
    failSafeCheck()

    width, height = _size()
    convertedX = 65536 * x // width + 1
    convertedY = 65536 * y // height + 1
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTCLICK, ctypes.c_long(convertedX), ctypes.c_long(convertedY), 0, 0)


def _size():
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


def linear(n):
    if not 0.0 <= n <= 1.0:
        raise UtilsException("Argument must be between 0.0 and 1.0.")
    return n


# _mouseMoveDrag(x, y, 0, 0, duration, linear)


def _mouseMoveDrag(x, y, xOffset, yOffset):
    xOffset = int(xOffset) if xOffset is not None else 0
    yOffset = int(yOffset) if yOffset is not None else 0

    if x is None and y is None and xOffset == 0 and yOffset == 0:
        return  # Special case for no mouse movement at all.

    startx, starty = position()

    x = int(x) if x is not None else startx
    y = int(y) if y is not None else starty

    # x, y, xOffset, yOffset are now int.
    x += xOffset
    y += yOffset

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]

    for tweenX, tweenY in steps:
        # if len(steps) > 1:
        #     # A single step does not require tweening.
        #     time.sleep(sleep_amount)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))

        # Do a fail-safe check to see if the user moved the mouse to a fail-safe position, but not if the mouse cursor
        # moved there as a result of this function. (Just because tweenX and tweenY aren't in a fail-safe position
        # doesn't mean the user couldn't have moved the mouse cursor to a fail-safe position.)
        if (tweenX, tweenY) not in [(0, 0)]:
            failSafeCheck()

        _moveTo(tweenX, tweenY)

    if (tweenX, tweenY) not in [(0, 0)]:
        failSafeCheck()


def moveRel(xOffset=None, yOffset=None, duration=0.0, tween=linear, logScreenshot=False, _pause=True):
    failSafeCheck()

    """Moves the mouse cursor to a point on the screen, relative to its current
    position.
    """
    # xOffset, yOffset = _normalizeXYArgs(xOffset, yOffset)

    _mouseMoveDrag(None, None, xOffset, yOffset)
