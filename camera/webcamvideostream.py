import cv2
from threading import Thread, Lock
import time


class WebcamVideoStream:
    _instance = None  # Singleton instance
    _lock = Lock()  # Lock for thread-safe access

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebcamVideoStream, cls).__new__(cls)
                cls._instance.__initialized = False
            return cls._instance

    def __init__(self, src=0,width=640, height=480):
        if not self.__initialized:  # Ensure initialization happens only once
            print("Initializing webcam...")
            self.src = src
            self.stream = cv2.VideoCapture(self.src)
            if not self.stream.isOpened():
                raise RuntimeError("Error: Could not open webcam. Please check the device.")

                
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.width = width
            self.height = height
            
            self.grabbed, self.frame = self.stream.read()
            self.stopped = False
            self.lock = Lock()  # Lock for thread-safe frame access
            self.thread = None
            time.sleep(1.0)  # Allow the camera to warm up if necessary
            self.__initialized = True

    def start(self):
        with self._lock:
            if self.thread is None or not self.thread.is_alive():
                print("Starting webcam thread...")
                self.stopped = False
                self.thread = Thread(target=self.update, daemon=True)
                self.thread.start()
        return self

    def update(self):
        while not self.stopped:
            grabbed, frame = self.stream.read()
            if not grabbed:
                print("Warning: Failed to grab frame.")
                continue

            with self.lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        with self._lock:
            if self.stopped:
                return  # Already stopped
            
            print("Stopping webcam...")
            self.stopped = True
            if self.thread is not None:
                self.thread.join()  # Ensure the thread finishes
            self.stream.release()  # Release the webcam resource
            WebcamVideoStream._instance = None  # Reset singleton instance
            self.__initialized = False
            print("Webcam released successfully.")
