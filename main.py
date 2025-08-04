import easyocr
import pyautogui
import pygetwindow as gw
import cv2
import threading
from paddleocr import PaddleOCR
from PIL import Image

import numpy as np

from display import *
from screenshot import take_screenshot
from text_extraction import extract_member_from_text


# ----------------------------------------------------------------
window_title = "Umamusume"

crop_ratio_left = 0.14
crop_ratio_right = 0.62
crop_ratio_top = 0.45
crop_ratio_bottom = 0.22



# ----------------------------------------------------------------


## EasyOCR
# reader = easyocr.Reader(['en', 'ja'], gpu = True)
# PaddleOCR
ocr = PaddleOCR(use_angle_cls=True)

# ----------------------------------------------------------------
def scroll_down(amount = 100, step=2):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        window.activate()
    except Exception:
        print("Không tìm thấy game!")
        return None
    left, top, width, height = window.left, window.top, window.width, window.height
    left = left + int(width * crop_ratio_left)
    top = top + int(height * crop_ratio_top)
    width = int(width * (1 - crop_ratio_left - crop_ratio_right))
    height = int(height * (1 - crop_ratio_top - crop_ratio_bottom))

    x = left + width
    y = top + width/2
    
    pyautogui.moveTo(x, y)
    for _ in range(step):
        pyautogui.scroll(-amount)
        time.sleep(0.05)

def ocr_to_lines(image):
    # Easy OCR
    # result = reader.readtext(image)
    # lines = [res[1] for res in result]

    # PaddleOCR
    result = ocr.predict(screen)
    lines = result[0]['rec_texts']
    return lines

members = []
member_num = 0


display_t = threading.Thread(target=display_loop, args=['Screenshot'])
display_t.start()
print("Start displaying")

running = True
non_update_count = 0

try:
    window_title = "Umamusume"
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()
    time.sleep(2)

    while running:
        screen = take_screenshot(crop_ratio_left, crop_ratio_right, crop_ratio_top, crop_ratio_bottom)
        if screen is not None:
            # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # screen = cv2.adaptiveThreshold(screen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            add_frame(screen)
        
        lines = ocr_to_lines(screen)

        # Thêm member nếu members chưa có trong danh sách
        found_members = extract_member_from_text(lines)
        for member in found_members:
            if member not in members:
                members.append(member)

        # DEBUG
        print(lines)
        print(found_members)

        # Hiển thị danh sách mỗi lần có cập nhật
        if len(members) > member_num:
            print('-' * 50)
            for member in members:
                print(member)
            member_num = len(members)
            print('-' * 50)
            non_update_count = 0
        else:
            print("Không tìm được member mới")
            non_update_count += 1

        # Dừng nếu display thread kết thúc hoặc sau 3 lần không update danh sách
        if not display_t.is_alive() or non_update_count == 5:
            raise KeyboardInterrupt
        
        scroll_down()
except KeyboardInterrupt:
    print("Đã dừng chương trình!")
    stop_display()
    exit()

except Exception as err:
    print("Error:", err)
    stop_display()
    exit()

display_t.join()