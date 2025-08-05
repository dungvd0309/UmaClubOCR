import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
from PIL import Image, ImageEnhance

from .window import activate_window
 
def mask_info_icon(image):
    """
    Mask info icons (i) for cropped images (preprocessing for OCR)
    """
    # Calculate minRadius based on the width of the image
    minRadius = image.shape[1]//40 

    # Find rounded (i) icons
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                            param1=60, param2=35, minRadius=minRadius, maxRadius=int(minRadius*1.5))

    # Cover the icon with a colored circle
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (cx, cy, r) in circles:
            r = int(r * 1.2) # Increase radius to fully cover the icon
            cv2.circle(image, (cx, cy), r, (0, 255, 0), -1)  # Draw color over the icon area
            
    return image

def take_screenshot(region):
    """
    Take a screenshot of the game window based on the region
    """
    activate_window()
    left, top, width, height = region

    # Take screenshot
    pil_img = pyautogui.screenshot(region=(left, top, width, height))
    pil_img = pil_img.resize((pil_img.width * 2, pil_img.height * 2), Image.BICUBIC) # x2 scale
    pil_img = pil_img.convert("L") # Greyscale
    pil_img = ImageEnhance.Contrast(pil_img).enhance(1.5) # Increase contract

    # Convert from PIL.Image to numpy array
    screen = np.array(pil_img)
    # Convert color channel from RGB to BGR (because OpenCV uses BGR)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    return screen