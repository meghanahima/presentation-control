import tkinter as tk
from queue import Queue, Empty

class Overlay:
    def __init__(self):
        self.command_queue = Queue()
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.geometry("+500+650")  # Position near bottom
        self.root.configure(bg="black")

        self.label = tk.Label(self.root, text="", fg="white", bg="black", font=("Helvetica", 18))
        self.label.pack()

        self._poll()  # Start polling both caption and commands

    def _poll(self):
        # Handle captions
        try:
            msg, duration = self.command_queue.get_nowait()
            if isinstance(msg, str):
                self.label.config(text=msg)
                self.root.deiconify()
                self.root.after(int(duration * 1000), self._clear)
            elif callable(msg):  # command is a function like next_slide
                msg()  # run the command in the main thread
        except Empty:
            pass
        except Exception as e:
            print("❌ Error executing main thread command:", e)

        self.root.after(100, self._poll)

    def _clear(self):
        self.label.config(text="")
        self.root.withdraw()

    def show_message(self, msg, duration=2):
        self.command_queue.put((msg, duration))

    def push_command(self, fn):  # fn = lambda: next_slide()
        self.command_queue.put((fn, 0))

    def run(self):
        self.root.withdraw()
        self.root.mainloop()

overlay = Overlay()

def show_caption(message, duration=2):
    overlay.show_message(message, duration)
