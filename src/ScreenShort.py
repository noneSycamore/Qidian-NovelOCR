"""
Take screenshot in Windows OS, target: Android Virtual Device.
"""

import pygetwindow as gw
import pyautogui as pg
import subprocess


class AndroidEmulator:
    def __init__(self):
        self._window = None
        self._device = self._choose_adb_device()

    @property
    def window(self):
        return self._window

    @property
    def device(self):
        return self._device

    def choose_avd_window(self):
        """
        Choose the Android Emulator window from the list.
        May do not need this func, if ADB screenshot works.
        """
        avd_window_list = self._get_android_emulator_window()
        for i, window in enumerate(avd_window_list):
            print(f"[{i + 1}]: {window}")
        index = int(input("Choose the AVD window: "))
        self._window = self._get_object_window(avd_window_list[index - 1])

    def _choose_adb_device(self):
        """
        Choose the device from the list.
        :return: name of the device
        """
        device_list = self._get_adb_devices()
        for i, device in enumerate(device_list):
            print(f"[{i + 1}]: {device}")
        index = int(input("Choose the device: "))
        return device_list[index - 1]

    @staticmethod
    def _get_adb_devices():
        """
        Get the list of connected devices.
        :return: list of the device
        """
        result = subprocess.run("adb devices", shell=True, stdout=subprocess.PIPE, text=True)
        devices = []
        for line in result.stdout.splitlines()[1:]:
            if line.strip() and "device" in line:
                devices.append(line.split()[0])
        return devices

    @staticmethod
    def _get_android_emulator_window():
        """
        Get Name of Android Emulator window.
        (e.g. "Android Emulator - Pixel_8a_API_31:5554")
        :return: list of the name
        """
        avd_window_list = []
        all_windows = gw.getAllTitles()

        for title in all_windows:
            if "Android Emulator" in title:
                avd_window_list.append(title)
        return avd_window_list

    @staticmethod
    def _get_object_window(window_name):
        """
        Get the window object by name.
        :param window_name: name of the window
        :return: window object
        """
        return gw.getWindowsWithTitle(window_name)[0]


def take_screenshot(target, filename, method="adb", save=True):
    """
    Take screenshot of the window.
    :param target: For "window", a window object. For "adb", a device name.
    :param filename: path and filename to save the screenshot
    :param method: method to take screenshot, "adb" or "window"
    :param save: if save the screenshot
    :return:
    """
    local_path = f"../screenshots/{filename}"
    if method == "adb":
        capture_cmd = f"adb -s {target} exec-out screencap -p > {local_path}"
        subprocess.run(capture_cmd, shell=True, check=True)
        print(f"Screenshot saved at \"{local_path}\"")
    elif method == "window":
        screenshot = pg.screenshot(region=(target.left, target.top, target.width, target.height))
        screenshot.save(local_path)
        print(f"Screenshot saved at \"{local_path}\"")
    else:
        raise ValueError("Unsupported method. Use 'window' or 'adb'.")
