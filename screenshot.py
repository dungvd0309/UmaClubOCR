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

# Hàm mask icon thông tin người chơi (preprocessing cho OCR)
def mask_info_icon(image):
    minRadius = image.shape[1]//40 # Đối với hình đã được crop

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                            param1=60, param2=35, minRadius=minRadius, maxRadius=int(minRadius*1.5))

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (cx, cy, r) in circles:
            r = int(r * 1.2) # Tăng bán kinh để đủ cover icon
            cv2.circle(image, (cx, cy), r, (0, 0, 0), -1)  # Vẽ màu lên vùng icon
            
    return image

# Hàm chụp ảnh window game dựa trên crop_ratio 
def take_screenshot(crop_ratio_left, crop_ratio_right, crop_ratio_top, crop_ratio_bottom):
    # screen = cv2.imread('assets/screen_copy.png', cv2.IMREAD_COLOR_BGR)
    # height, width = screen.shape[:2]

    # Tìm cửa sổ theo tiêu đề 
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        # window.activate()
    except IndexError:
        print("Không tìm thấy game!")
        return None

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