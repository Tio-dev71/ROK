from Actions.action import Action
from window_handler import WindowHandler
import pyautogui
import time
import os
from adb_handler import ADBHandler

class PressKeyAction(Action):
    def __init__(self, key: str, delay=0, retard=0, times=1):
        self.key = key
        self.delay = delay
        self.retard = retard
        self.times = times
        self.window_handler = WindowHandler()

    def execute(self):
        time.sleep(self.delay)
        
        mode = os.getenv('MODE', 'PC')
        if mode == 'ADB':
            adb = ADBHandler()
            
            # Map known PC keys to Android Keyevents or Taps
            # ROK Mobile doesn't use 'space' or 'f'. It relies on touch.
            # 4 is KEYCODE_BACK (acts as Escape)
            if self.key == 'escape':
                adb.keyevent(4)
            elif self.key == 'space':
                # Map to bottom left city/world toggle (approximate coordinates for 16:9 like 1280x720)
                adb.tap(90, 630) # Example fallback tap for 'space'
            elif self.key == 'f':
                # Map to search icon (approximate coordinates)
                adb.tap(120, 630) # Example fallback tap for 'f'
            else:
                # Fallback to trying to send character
                pass
        else:
            self.window_handler.activate_window()
            #pyautogui.press(self.key, presses=self.times)
            pyautogui.keyDown(self.key)
            time.sleep(1)
            pyautogui.keyUp(self.key)
            #press arrow left
            
        return True  # Always return True since pressing a key will not fail
