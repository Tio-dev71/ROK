import subprocess
import os
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class ADBHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ADBHandler, cls).__new__(cls)
            cls._instance.device = os.getenv('ADB_DEVICE', '')
            if cls._instance.device:
                cls._instance.connect()
        return cls._instance

    def connect(self):
        """Connects to the ADB device if specified."""
        try:
            print(f"Connecting to ADB device: {self.device}")
            subprocess.run(["adb", "connect", self.device], check=True, capture_output=True, text=True)
        except Exception as e:
            print(f"Failed to connect to ADB device {self.device}: {e}")

    def _get_adb_cmd(self, *args):
        cmd = ["adb"]
        if self.device:
            cmd.extend(["-s", self.device])
        cmd.extend(args)
        return cmd

    def screencap(self):
        """Captures the screen and returns a PIL Image."""
        cmd = self._get_adb_cmd("exec-out", "screencap", "-p")
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            image_data = result.stdout
            if not image_data:
                return None
            image = Image.open(io.BytesIO(image_data))
            return image
        except Exception as e:
            print(f"ADB screencap failed: {e}")
            return None

    def tap(self, x, y):
        """Taps at the specified (x, y) coordinates."""
        cmd = self._get_adb_cmd("shell", "input", "tap", str(x), str(y))
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"ADB tap failed: {e}")

    def swipe(self, x1, y1, x2, y2, duration_ms=0):
        """Swipes from (x1, y1) to (x2, y2). Can be used to move/drag."""
        cmd = self._get_adb_cmd("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2))
        if duration_ms > 0:
            cmd.append(str(duration_ms))
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"ADB swipe failed: {e}")

    def keyevent(self, keycode):
        """Sends a keyevent to the device."""
        # e.g. 4 is BACK (Escape)
        cmd = self._get_adb_cmd("shell", "input", "keyevent", str(keycode))
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"ADB keyevent failed: {e}")
