import pyautogui
import pygetwindow as gw
import cv2
import numpy as np

window_title = "Umamusume"

# try:
#     window = gw.getWindowsWithTitle(window_title)[0]  
# except IndexError:
#     print("Không tìm thấy cửa sổ!")
#     exit()

# pyautogui.screenshot(region=(window.left, window.top, window.width, window.height)).save('temp.png')

def take_screenshot(crop_ratio_left, crop_ratio_right, crop_ratio_top, crop_ratio_bottom):
    # screen = cv2.imread('assets/screen_copy.png', cv2.IMREAD_COLOR_BGR)
    # Tìm cửa sổ theo tiêu đề 
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        # window.activate()
    except IndexError:
        print("Không tìm thấy game!")
        return None


    # height, width = screen.shape[:2]


    # Crop ảnh theo tỉ lệ
    left, top, width, height = window.left, window.top, window.width, window.height

    left = left + int(width * crop_ratio_left)
    top = top + int(height * crop_ratio_top)
    width = int(width * (1 - crop_ratio_left - crop_ratio_right))
    height = int(height * (1 - crop_ratio_top - crop_ratio_bottom))
    # screen = screen[top:top + height, left:left + width] 
    
    screen = pyautogui.screenshot(region=(left, top, width, height))
    # Chuyển từ PIL.Image sang numpy array
    screen = np.array(screen)
    # Chuyển kênh màu từ RGB sang BGR (do OpenCV dùng BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    

    return screen