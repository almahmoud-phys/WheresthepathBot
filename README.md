# WheresthepathBot

## Usage

Since the program still in beta you can go to ./neura/Constants.py and chage telegram API parameters

## Contribution

All gui should be in ./neura/TelegramBotGUI.py and work with API in ./neura/TelegramBot.py

the TelegramBot Class give three objects :
- admin : is a Telethon client
- group  : the group that you choose to work with
- users : all users in that goup

## TODO
- [ ] switch from **tkinter** to better library since tk doesn't support arabic or  Asynchronous functions
- [ ] use **pyistaler** to create a standalone executable file


