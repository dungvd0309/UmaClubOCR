import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
from PIL import Image, ImageEnhance

from .window import get_crop_region, activate_window

# Mask the info icon (i) (preprocessing for OCR)
def mask_info_icon(image):
    minRadius = image.shape[1]//40 # For cropped images

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                            param1=60, param2=35, minRadius=minRadius, maxRadius=int(minRadius*1.5))

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (cx, cy, r) in circles:
            r = int(r * 1.2) # Increase radius to fully cover the icon
            cv2.circle(image, (cx, cy), r, (0, 255, 0), -1)  # Draw color over the icon area
            
    return image

# Take a screenshot of the game window based on the crop_region
def take_screenshot(crop_region):
    activate_window()

    # Take screenshot
    left, top, width, height = crop_region
    
    pil_img = pyautogui.screenshot(region=(left, top, width, height))
    pil_img = pil_img.resize((pil_img.width * 2, pil_img.height * 2), Image.BICUBIC)
    pil_img = pil_img.convert("L")
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.5)


    # Convert from PIL.Image to numpy array
    screen = np.array(pil_img)
    # Convert color channel from RGB to BGR (because OpenCV uses BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    return screen