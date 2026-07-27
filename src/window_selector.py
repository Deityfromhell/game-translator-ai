import win32gui


def get_open_windows():
    windows = []

    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()

        if title:
            windows.append({
                "hwnd": hwnd,
                "title": title,
            })

    win32gui.EnumWindows(callback, None)

    return windows


if __name__ == "__main__":
    for window in get_open_windows():
        print(window["hwnd"], "-", window["title"])