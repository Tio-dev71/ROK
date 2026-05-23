from PIL import Image
from mss import mss
import pygetwindow as gw
import os
from adb_handler import ADBHandler

class WindowHandler:
    def get_window(self, title):
        windows = gw.getWindowsWithTitle(title)
        
        if not windows:
            print(f"No window found with title: {title}")
            return None
        return windows[0]

    def screenshot_window(self, title):
        mode = os.getenv('MODE', 'PC')
        if mode == 'ADB':
            adb = ADBHandler()
            screenshot = adb.screencap()
            
            # Dummy window object for ADB mode
            class DummyWin:
                left = 0
                top = 0
                width = screenshot.width if screenshot else 1280
                height = screenshot.height if screenshot else 720
            
            return screenshot, DummyWin()

        # Fallback to PC mode
        win = self.get_window(title)
        if not win:
            return None, None

        sct = mss()
        monitor = {"top": win.top, "left": win.left, "width": win.width, "height": win.height}
        try:
            img = sct.grab(monitor)
        finally:
            sct.close()
        screenshot = Image.frombytes("RGB", img.size, img.rgb, "raw")
        return screenshot, win

    
    def activate_window(self, title="Rise of Kingdoms"):
        try:
            win = self.get_window(title)
            win.activate()
            
        except:
            print("Window not found")
        return 