# -*- coding: UTF-8 -*-
# بسم الله الرحمن الرحيم
# برنامج أين الطريق لقناة سنحيا كراما
# هذا البرنامج يتبع حقوق وقف
# Created on 9 Safar 1445 - 13 August 2024
# Authors: Aamer and Ismail

import os
import tkinter as tk

import neura.Constants as Constants
from neura import SplashScreen, TelegramBotConfig, TelegramBotGUI

if __name__ == "__main__":
    if Constants.DEBUG:
        # test the json file
        if os.path.exists(Constants.CONFIG_FILE):
            # os.remove(Constants.CONFIG_FILE)
            pass

    root = tk.Tk()
    root.withdraw()  # Hide the main window initially

    if not Constants.DEBUG:
        # don't show splash in debug mode
        splash = SplashScreen(root, "splash_image.jpg", display_time=3000)
        root.wait_window(splash.splash)

    bot = TelegramBotConfig(root)

    gui = TelegramBotGUI(root, bot)
    root.wait_window(gui.root)

    # one root tk object
    # https://www.google.com/search?client=firefox-b-d&q=use+many+root+in+tk
