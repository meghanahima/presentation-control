import tkinter as tk
from queue import Queue, Empty
import cv2
from PIL import Image, ImageTk

class Overlay:
    def __init__(self):
        self.command_queue = Queue()
        
        # Create main window for camera
        self.camera_root = tk.Tk()
        self.camera_root.attributes('-topmost', True)
        self.camera_root.overrideredirect(True)
        
        # Create caption window
        self.caption_root = tk.Tk()
        self.caption_root.attributes('-topmost', True)
        self.caption_root.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = self.camera_root.winfo_screenwidth()
        screen_height = self.camera_root.winfo_screenheight()
        
        # Setup camera window
        self.camera_frame = tk.Label(self.camera_root, bg="black")
        self.camera_frame.pack(padx=5, pady=5)
        
        # Position camera window at bottom right
        camera_width = 330  # 320 + padding
        camera_height = 250  # 240 + padding
        camera_x = screen_width - camera_width - 20  # 20px from right edge
        camera_y = screen_height - camera_height - 20  # 20px from bottom
        self.camera_root.geometry(f"{camera_width}x{camera_height}+{camera_x}+{camera_y}")
        
        # Setup caption window with improved styling
        self.caption_frame = tk.Frame(self.caption_root, bg="#1a1a1a", padx=15, pady=8)
        self.caption_frame.pack(fill=tk.BOTH, expand=True)
        
        self.label = tk.Label(
            self.caption_frame,
            text="",
            fg="white",
            bg="#1a1a1a",
            font=("Segoe UI", 16, "bold"),
            padx=10,
            pady=5
        )
        self.label.pack()
        
        # Position caption window at bottom center
        caption_width = 500
        caption_height = 60
        caption_x = (screen_width - caption_width) // 2
        caption_y = screen_height - caption_height - 50  # 50px from bottom
        self.caption_root.geometry(f"{caption_width}x{caption_height}+{caption_x}+{caption_y}")
        
        # Initialize camera-related variables
        self.current_photo = None
        self.camera_error = False
        
        # Show both windows immediately
        self.camera_root.deiconify()
        self.caption_root.deiconify()
        
        self._poll()  # Start polling both caption and commands

    def update_camera(self, frame):
        if frame is None:
            if not self.camera_error:
                self.camera_frame.configure(text="No camera feed")
                self.camera_error = True
            return
            
        try:
            # Resize frame to 320x240
            frame = cv2.resize(frame, (320, 240))
            # Convert to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to PhotoImage
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            
            # Update camera frame
            self.camera_frame.configure(image=photo, text="")
            self.camera_frame.image = photo  # Keep a reference
            self.current_photo = photo
            self.camera_error = False
            
        except Exception as e:
            if not self.camera_error:
                print(f"❌ Error updating camera frame: {e}")
                self.camera_frame.configure(text="Camera error")
                self.camera_error = True

    def _poll(self):
        # Handle captions
        try:
            msg, duration = self.command_queue.get_nowait()
            if isinstance(msg, str):
                self.label.config(text=msg)
                self.caption_root.deiconify()
                self.caption_root.after(int(duration * 1000), self._clear_caption)
            elif callable(msg):  # command is a function like next_slide
                msg()  # run the command in the main thread
        except Empty:
            pass
        except Exception as e:
            print("❌ Error executing main thread command:", e)

        self.camera_root.after(100, self._poll)

    def _clear_caption(self):
        self.label.config(text="")
        self.caption_root.withdraw()

    def show_message(self, msg, duration=2):
        self.command_queue.put((msg, duration))

    def push_command(self, fn):  # fn = lambda: next_slide()
        self.command_queue.put((fn, 0))

    def run(self):
        self.camera_root.mainloop()

overlay = Overlay()

def show_caption(message, duration=2):
    overlay.show_message(message, duration)
