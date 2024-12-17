"""
press the right side of the screen to flip the page, in the AVD
"""
import subprocess


def get_screen_size(device):
    """
    Get the screen size of the device.
    :param device: name of the device
    :return: screen width, screen height
    """
    get_size_cmd = f"adb -s {device} shell wm size"
    result = subprocess.run(get_size_cmd, shell=True, stdout=subprocess.PIPE, text=True)
    size = result.stdout.split()[2].split("x")
    return int(size[0]), int(size[1])


def tap_screen(device, x, y):
    """
    Tap the screen at the position (x, y).
    :param device: name of the device
    :param x: x-coordinate
    :param y: y-coordinate
    """
    subprocess.run(f"adb -s {device} shell input tap {x} {y}", shell=True)
    print("Tap at", x, y)


def flip_page(device):
    """
    Press the right side of the screen to flip the page.
    :param device: name of the device
    """
    screen_width, screen_height = get_screen_size(device)
    x = screen_width - 100
    y = screen_height // 2
    tap_screen(device, x, y)
