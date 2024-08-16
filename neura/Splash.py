import tkinter as tk
from PIL import Image, ImageTk

class SplashScreen:
    def __init__(self, image_path, display_time=3000):
        self.image_path = image_path
        self.display_time = display_time  # Time in milliseconds

        # Initialize the splash screen window
        self.splash_root = tk.Tk()
        self.splash_root.overrideredirect(True)  # Hide the title bar

        # Load the image
        self.image = Image.open(self.image_path)
        self.splash_image = ImageTk.PhotoImage(self.image)

        # Add the image to a label
        splash_label = tk.Label(self.splash_root, image=self.splash_image)
        splash_label.pack()

        # Center the window
        self.center_window()

    def center_window(self):
        window_width = self.splash_root.winfo_reqwidth()
        window_height = self.splash_root.winfo_reqheight()
        position_right = int(self.splash_root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.splash_root.winfo_screenheight() / 2 - window_height / 2)
        self.splash_root.geometry(f"+{position_right}+{position_down}")

    def show(self):
        # Display the splash screen for the specified time
        self.splash_root.after(self.display_time, self.splash_root.destroy)
        self.splash_root.mainloop()