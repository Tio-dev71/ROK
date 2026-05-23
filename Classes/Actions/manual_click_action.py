import time
from Actions.action import Action
from window_handler import WindowHandler
import pyautogui
import os
from adb_handler import ADBHandler

class ManualClickAction(Action):
    def __init__(self,x=50,y=50, delay=0, remember_position=True, retard=0.0):
        self.window_handler = WindowHandler()
        self.delay = delay
        self.window_title = 'Rise of Kingdoms'
        self.x = x
        self.y = y
        self.remember_position = remember_position
        self.retard = retard



    def execute(self):
        time.sleep(self.delay)
        time.sleep(0.1)
        click_x = int(self.window_handler.get_window(self.window_title).left + self.window_handler.get_window(self.window_title).width * self.x / 100)
        click_y = int(self.window_handler.get_window(self.window_title).top + self.window_handler.get_window(self.window_title).height * self.y / 100)
        
        mode = os.getenv('MODE', 'PC')
        if mode == 'ADB':
            adb = ADBHandler()
            adb.tap(click_x, click_y)
        else:
            prev_active_window = pyautogui.getActiveWindow()
            prev_mouse_x, prev_mouse_y = pyautogui.position()
            pyautogui.click(click_x, click_y)
            if prev_active_window:
                prev_active_window.activate()
            if self.remember_position:
                pyautogui.moveTo(prev_mouse_x, prev_mouse_y)
        return True
