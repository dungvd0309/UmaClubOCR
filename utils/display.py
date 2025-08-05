import cv2
import queue

frame_queue = queue.Queue(maxsize=1)
running = True

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