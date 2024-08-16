# بسم الله الرحمن الرحيم
# برنامج أين الطريق لقناة سنحيا كراما
# هذا البرنامج يتبع حقوق وقف
# Created on 9 Safar 1445 - 13 August 2024
# Authors: Aamer and Ismail

from neura import TelegramBotConfig, TelegramBotGUI,SplashScreen
#Adding the Class for web scrapping



if __name__ == "__main__":
    config = TelegramBotConfig()
    splash = SplashScreen("splash_image.jpg", display_time=5000)
    splash.show()
    gui = TelegramBotGUI(config)
