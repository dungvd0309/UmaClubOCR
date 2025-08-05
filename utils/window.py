import time
import pyautogui
import pygetwindow as gw

def activate_window():
    """
    Finds and activates the 'Umamusume' game window.
    """
    windows = gw.getWindowsWithTitle("Umamusume")
    if not windows:
        raise Exception("Umamusume window not found.")
    win = windows[0]
    if win.isMinimized:
        win.restore()
    win.activate()
    return win

def get_crop_region(window, crop_ratios):
    """
    Calculates the crop region based on the window and crop ratios.
    Returns a tuple (left, top, width, height).
    """
    crop_ratio_left, crop_ratio_right, crop_ratio_top, crop_ratio_bottom = crop_ratios

    left, top, width, height = window.left, window.top, window.width, window.height
    left = left + int(width * crop_ratio_left)
    top = top + int(height * crop_ratio_top)
    width = int(width * (1 - crop_ratio_left - crop_ratio_right))
    height = int(height * (1 - crop_ratio_top - crop_ratio_bottom))
    return left, top, width, height

def scroll_down(region, amount=300, step=4):
    """
    Scrolls down at the right edge of the given region.
    The region is a tuple (left, top, width, height).
    """
    left, top, width, height = region

    # Scroll mouse position (right edge, vertical center of the region)
    x = left + width
    y = top + (height / 2)
    
    pyautogui.moveTo(x, y)
    for _ in range(step):
        pyautogui.scroll(-amount)
