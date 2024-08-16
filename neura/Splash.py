import tkinter as tk
from PIL import Image, ImageTk

class SplashScreen:
    def __init__(self, image_path, display_time=3000):
        self.image_path = image_path
        self.display_time = display_time  # Time in milliseconds

        # Initialize the splash screen window
        self.splash_root = tk.Tk()
        self.splash_root.overrideredirect(True)  # Hide the title bar

        # Set window size to 800x800
        self.splash_root.geometry("800x800")

        # Load the image
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((800, 800), Image.ANTIALIAS)  # Resize the image to fit the window
        self.splash_image = ImageTk.PhotoImage(self.image)

        # Add the image to a label
        splash_label = tk.Label(self.splash_root, image=self.splash_image)
        splash_label.pack()

        # Center the window
        self.center_window()

    def center_window(self):
        # Get the dimensions of the screen
        screen_width = self.splash_root.winfo_screenwidth()
        screen_height = self.splash_root.winfo_screenheight()

        # Calculate position to center the window
        position_right = int(screen_width / 2 - 800 / 2)
        position_down = int(screen_height / 2 - 800 / 2)

        # Set the geometry to the calculated position
        self.splash_root.geometry(f"800x800+{position_right}+{position_down}")

    def show(self):
        # Display the splash screen for the specified time
        self.splash_root.after(self.display_time, self.splash_root.destroy)
        self.splash_root.mainloop()

if __name__ == "__main__":
    splash = SplashScreen("splash_image.jpg", display_time=3000)
    splash.show()
