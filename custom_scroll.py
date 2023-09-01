import time
import win32api
import win32con


def scroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
    """
    Source: https://learn.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-mouse_event?redirectedfrom=MSDN

    void mouse_event(
      DWORD     dwFlags,
      DWORD     dx,
      DWORD     dy,
      DWORD     dwData,
      ULONG_PTR dwExtraInfo
    );

    If dwFlags contains MOUSEEVENTF_WHEEL,
    then dwData specifies the amount of wheel movement.
    A positive value indicates that the wheel was rotated forward, away from the user;
    A negative value indicates that the wheel was rotated backward, toward the user.
    One wheel click is defined as WHEEL_DELTA, which is 120.

    :param delay_between_ticks:
    :param delta_y:
    :param delta_x:
    :param clicks:
    :return:
    """
    if clicks > 0:
        increment = win32con.WHEEL_DELTA
    else:
        increment = win32con.WHEEL_DELTA * -1

    for _ in range(abs(clicks)):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, delta_x, delta_y, increment, 0)
        time.sleep(delay_between_ticks)


# pyautogui.moveTo(x=click_point[0], y=click_point[1], duration=0.25)
# time.sleep(2)
# scroll(-4)

# if __name__ == '__main__':
#     main()
