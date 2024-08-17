# بسم الله الرحمن الرحيم
# برنامج أين الطريق لقناة سنحيا كراما
# هذا البرنامج يتبع حقوق وقف
# Created on 9 Safar 1445 - 13 August 2024
# Authors: Aamer and Ismail

from neura import  SplashScreen, TelegramBotConfig, TelegramBotGUI , TeClient
import tkinter as tk
import os
# Adding the Class for web scrapping



def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

if __name__ == "__main__":

    # remove the config file if it exists
    if os.path.exists("config.json"):
        os.remove("config.json")

    root = tk.Tk()



    root.withdraw()  # Hide the main window initially
    splash = SplashScreen(root, "splash_image.jpg", display_time=1000)

    root.wait_window(splash.splash)
    # root.withdraw()  # Hide the main window initially
    config = TelegramBotConfig(root)

    root.wait_window(config.splash)

    client = TeClient(root , config)

    gui = TelegramBotGUI(root, config, client)
    root.wait_window(gui.root)

    # root.mainloop()
    # root.destroy()
    # one root tk object
    # https://www.google.com/search?client=firefox-b-d&q=use+many+root+in+tk
    # TODO : discuss this
