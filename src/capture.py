import ctypes
import time

import cv2
import numpy as np
import win32gui
import win32ui

from ocr import OCRReader


def capture_window(hwnd):
    """Capture the selected Windows window using PrintWindow."""

    if not win32gui.IsWindow(hwnd):
        raise ValueError("Invalid window handle.")

    if win32gui.IsIconic(hwnd):
        raise ValueError("Selected window is minimized.")

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        raise ValueError("Invalid window dimensions.")

    window_dc = win32gui.GetWindowDC(hwnd)
    source_dc = win32ui.CreateDCFromHandle(window_dc)

    memory_dc = source_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(
        source_dc,
        width,
        height,
    )

    memory_dc.SelectObject(bitmap)

    try:
        result = ctypes.windll.user32.PrintWindow(
            hwnd,
            memory_dc.GetSafeHdc(),
            2,
        )

        if result != 1:
            raise RuntimeError("PrintWindow failed.")

        bitmap_data = bitmap.GetBitmapBits(True)

        frame = np.frombuffer(
            bitmap_data,
            dtype=np.uint8,
        )

        frame.shape = (height, width, 4)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGRA2BGR,
        )

        return frame.copy()

    finally:
        win32gui.DeleteObject(bitmap.GetHandle())
        memory_dc.DeleteDC()
        source_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, window_dc)


def run_capture(hwnd, stop_event):
    """Capture a window and periodically run OCR."""

    print("Starting OCR...")

    ocr = OCRReader()

    last_ocr_time = 0
    last_text = ""

    while not stop_event.is_set():
        try:
            frame = capture_window(hwnd)

        except Exception as error:
            print(f"Capture error: {error}")
            break

        current_time = time.time()

        # OCR twice per second.
        if current_time - last_ocr_time >= 0.5:
            try:
                text = ocr.read_text(frame)

                if text and text != last_text:
                    print("\n----------------")
                    print("DETECTED:")
                    print(text)
                    print("----------------")

                    last_text = text

            except Exception as error:
                print(f"OCR error: {error}")

            last_ocr_time = current_time

        cv2.imshow(
            "Game Translator - Window Capture",
            frame,
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            stop_event.set()
            break

    cv2.destroyAllWindows()