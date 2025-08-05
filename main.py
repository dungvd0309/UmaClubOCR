import csv
import time
import threading

from utils.display import display_loop, add_frame, stop_display
from utils.screenshot import take_screenshot, mask_info_icon
from utils.window import activate_window, scroll_down, get_crop_region
from ocr.ocr_utils import init_ocr, ocr_to_lines, extract_members_from_lines

# Constants
FAILED_TRIES = 3  
CROP_RATIO_LEFT = 0.14
CROP_RATIO_RIGHT = 0.62
CROP_RATIO_TOP = 0.45
CROP_RATIO_BOTTOM = 0.22
CROP_RATIOS = (CROP_RATIO_LEFT, CROP_RATIO_RIGHT, CROP_RATIO_TOP, CROP_RATIO_BOTTOM) 

def export_csv(members):
    """
    Exports a csv from member list to "output/members_YYYYmmdd_HHMMSS.csv"
    """
    from datetime import datetime
    import os

    directory = "output"
    base_name = "members"

    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"[ERROR] {e}")

    now = datetime.now()
    file_name = f'{directory}/{base_name}_{now.strftime("%Y%m%d_%H%M%S")}.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Header
        writer.writerow(['name','fans'])
        # Data
        for member in members:
            writer.writerow([member['name'], member['fans']])
        print(f"Member list saved to '{file_name}'")

def main():
    members = []
    scan_successful = False

    # A thread to display screenshots
    display_t = threading.Thread(target=display_loop, args=['Screenshot'])
    display_t.start()

    try:
        print("[INFO] PaddleOCR initializing...")
        ocr = init_ocr()

        print("-" * 50)
        print("[INFO] Make sure you are at Club Info screen.")
        print("[INFO] Starting scan...")
        
        window = activate_window()
        time.sleep(2)

        crop_region = get_crop_region(window, CROP_RATIOS)
        
        member_num = 0
        non_update_count = 0
        while True:
            # Screenshot
            screen = take_screenshot(crop_region)
            if screen is not None:
                screen = mask_info_icon(screen)
                add_frame(screen)
            
            # OCR
            lines = ocr_to_lines(ocr, screen)

            # Add member if not already in the list
            found_members = extract_members_from_lines(lines)
            for member in found_members:
                if member not in members:
                    members.append(member)
                    print(member)

            # print(lines) # FOR DEBUGGING

            # Check for updates and reset retry counter if new members are found
            if len(members) > member_num:
                member_num = len(members)
                non_update_count = 0
            else:
                print(f"[INFO] No new members found. Retrying {FAILED_TRIES - non_update_count - 1} more time(s).")
                non_update_count += 1

            # Stop if the display window is closed
            if not display_t.is_alive():
                raise KeyboardInterrupt("Display window was closed.")
            
            # Stop after a number of FAILED_TRIES with no updates
            if non_update_count >= FAILED_TRIES:
                print("[INFO] Scan finished after multiple tries with no new members.")
                break
            
            scroll_down(crop_region)
        
        scan_successful = True

    except KeyboardInterrupt as e:
        print(f"[INFO] Program interrupted by user. {e}")

    except Exception as err:
        print(f"[ERROR] An unexpected error occurred: {err}")

    finally:
        print("-" * 50)
        stop_display()
        display_t.join()

    # Only export if the scan completed successfully and we have members
    if scan_successful and len(members) > 0:
        print(f"[INFO] Scan completed successfully. Found {len(members)} members.")
        export_csv(members)

if __name__ == "__main__":
    main()