import csv
import time
import threading

from paddleocr import PaddleOCR

from utils.display import display_loop, add_frame, stop_display
from utils.screenshot import take_screenshot, mask_info_icon
from utils.text_extraction import extract_member_from_text
from ocr.ocr_utils import init_ocr, ocr_to_lines
from utils.window import activate_window, scroll_down, get_crop_region


# ----------------------------------------------------------------
# Crop ratios: left, right, top, bottom
crop_ratio_left = 0.14
crop_ratio_right = 0.62
crop_ratio_top = 0.45
crop_ratio_bottom = 0.22
# ----------------------------------------------------------------

# Create a new thread to display the screenshot
display_t = threading.Thread(target=display_loop, args=['Screenshot'])
display_t.start()

print("Starting scan...")
members = []
member_num = 0
non_update_count = 0
tries = 3

try:
    window = activate_window()
    time.sleep(2)

    # Calculate the crop region once
    crop_region = get_crop_region(window, crop_ratio_left, crop_ratio_right, crop_ratio_top, crop_ratio_bottom)

    # PaddleOCR
    print("Loading PaddleOCR...")
    ocr = init_ocr()

    while True:
        # Screenshot
        screen = take_screenshot(crop_region)
        if screen is not None:
            screen = mask_info_icon(screen)
            add_frame(screen)
        
        # OCR
        lines = ocr_to_lines(ocr, screen)

        # Add member if not already in the list
        found_members = extract_member_from_text(lines)
        for member in found_members:
            if member not in members:
                members.append(member)

        # print(lines) # DEBUG

        # Display the list on each update
        if len(members) > member_num:
            print('-' * 50)
            for member in members:
                print(member)
            member_num = len(members)
            print('-' * 50)
            non_update_count = 0
        else:
            print(f"No new members found. Retrying {tries - non_update_count - 1} more time(s).")
            non_update_count += 1

        # Raise error if the display thread has ended
        if not display_t.is_alive() or non_update_count == tries:
            raise KeyboardInterrupt
        
        # Stop after a number of tries with no updates
        if non_update_count == tries:
            break;
        
        # Scroll mouse
        scroll_down(crop_region)
except KeyboardInterrupt:
    print("Program interrupted.")
    stop_display()

except Exception as err:
    print("Error:", err)
    stop_display()
    exit()

display_t.join()

def export_csv(members):
    from datetime import date
    today = date.today()
    file_name = f'output_{today.strftime("%d_%m_%Y")}.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(['name','fans'])
        # Data
        for member in members:
            writer.writerow([member['name'], member['fans']])
        print(f"Member list saved to {file_name}")
    
if len(members) != 0:
    export_csv(members)
