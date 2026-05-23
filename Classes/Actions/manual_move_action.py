import time
from Actions.action import Action
from window_handler import WindowHandler
import pyautogui
import os
from adb_handler import ADBHandler
class ManualMoveAction(Action):
    def __init__(self,x=50,y=50, delay=0, remember_position=False, retard=0.0):
        self.window_handler = WindowHandler()
        self.delay = delay
        self.window_title = 'Rise of Kingdoms'
        self.x = x
        self.y = y
        self.remember_position = remember_position
        self.retard = retard



    def execute(self):
        time.sleep(self.delay)

        click_x = int(self.window_handler.get_window(self.window_title).left + self.window_handler.get_window(self.window_title).width * self.x / 100)
        click_y = int(self.window_handler.get_window(self.window_title).top + self.window_handler.get_window(self.window_title).height * self.y / 100)
        
        mode = os.getenv('MODE', 'PC')
        if mode == 'ADB':
            adb = ADBHandler()
            # In ADB, we can't just "move" a cursor. We simulate a quick swipe to the location or do nothing.
            # Usually, moving the mouse in PyAutoGUI is to hover. Hover doesn't exist in touch.
            # We will use tap if needed, or swipe from current to target.
            # For now, we will simulate it with a tap or small swipe.
            adb.swipe(click_x, click_y, click_x, click_y, 0)
        else:
            prev_active_window = pyautogui.getActiveWindow()
            prev_mouse_x, prev_mouse_y = pyautogui.position()
            pyautogui.moveTo(click_x, click_y)
            if prev_active_window:
                prev_active_window.activate()
            if self.remember_position:
                pyautogui.moveTo(prev_mouse_x, prev_mouse_y)
        return True
