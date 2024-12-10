import win32gui
import win32ui
import win32con
import ctypes
import numpy as np
import cv2

class WindowCapture:
    def __init__(self, window_name=None):
        self.window_name = window_name
        hwnd = win32gui.FindWindow(None, window_name)
        if not hwnd:
            raise Exception(f"Window '{window_name}' not found!")
        self.hwnd = hwnd

    def get_screenshot(self):
        # Get the window dimensions
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)

        # Width and height
        width = right - left
        height = bottom - top

        # Ensure the dimensions match the window
        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # Create a bitmap to store the capture
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # Capture the window's contents
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)

        # Convert to a NumPy array
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)

        # Release resources
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)

        # Convert to BGR (if needed for OpenCV)
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

# Example usage
window_name = "Harbi2 Global | International Official\xa0Server - Doyyumhwan"
wincap = WindowCapture(window_name)  # Replace with the name of your window
screenshot = wincap.get_screenshot()
cv2.imshow("Captured Window", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
