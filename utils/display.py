import cv2
import queue
import time

frame_queue = queue.Queue(maxsize=1)
running = True

def display_scale(title, image, scale = 1.0):
    image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
    cv2.imshow(title, image)

def display_scale_list(title, images, scale = 0.0):
    for i in range(len(images)):
        display_scale(f"{title} {i}", images[i], scale)

def add_frame(image):
    try:
        frame_queue.put(image)
    except queue.Full:
        _ = frame_queue.get_nowait
        frame_queue.put(image)

def display_loop(title):
    while running:
        try:
            frame = frame_queue.get(timeout=0.03)
            cv2.imshow(title, frame)
        except queue.Empty:
            pass
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def stop_display():
    global running 
    running = False