import cv2
import os
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time

TIME_INTERVAL = 100  # Time interval in milliseconds
GESTURE_NAME = "Smth"
START_INDEX = 1  # Start naming images from 250.jpg
NUM_PICS = 800  # Maximum number of pictures to capture

class ImageCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Capture App")

        self.label = ttk.Label(root)
        self.label.grid(row=0, column=0, columnspan=2)
        
        self.cap = cv2.VideoCapture(0)
        self.capture_thread = threading.Thread(target=self.update_video_feed, daemon=True)
        self.capture_thread.start()

        self.current_index = START_INDEX
        self.root.after(TIME_INTERVAL, self.capture_image)

    def update_video_feed(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                cv2.rectangle(frame, (100, 100), (302, 302), (0, 255, 0), 2)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.configure(image=photo)
                self.label.image = photo

    def capture_image(self):
        # Stop capturing images if the maximum limit is reached
        if self.current_index >= START_INDEX + NUM_PICS:
            print(f"Captured {NUM_PICS} images. Stopping capture.")
            self.cap.release()
            return

        create_directory(GESTURE_NAME)
        image_name = os.path.join(GESTURE_NAME, f"{self.current_index}.jpg")
        ret, frame = self.cap.read()
        if ret:
            frame = frame[100:300, 100:300, :]  # Crop the ROI
            cv2.imwrite(image_name, frame)
            print(f"Image captured and saved as {image_name}")
        self.current_index += 1
        self.root.after(TIME_INTERVAL, self.capture_image)

if __name__ == "__main__":
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    root = tk.Tk()
    app = ImageCaptureApp(root)
    app.root.mainloop()
