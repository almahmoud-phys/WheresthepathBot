import tkinter as tk

from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, root, image_path, display_time=3000):
        self.root = root
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(
            True
        )  # Remove window decorations (title bar, etc.)

        # Load and display the image
        image = Image.open(image_path)  # Replace with your image file path
        photo = ImageTk.PhotoImage(image)

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_width = photo.width()
        splash_height = photo.height()
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

        # Create a label to display the image
        label = tk.Label(self.splash, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        # Close the splash screen after a delay
        self.splash.after(display_time, self.close_splash)

    def close_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    splash = SplashScreen(root, "splash_image.jpg", display_time=3000)
    splash.show()
