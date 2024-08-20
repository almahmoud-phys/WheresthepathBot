# WheresthepathBot

## Usage

1. `pip install -r requirements.txt`
2. Since the program still in beta you can go to [Constants](./neura/Constants.py) and chage telegram API parameters
3. `python main.py`

## Contribution

All gui should be in [TelegramBotGUI](./neura/TelegramBotGUI.py) and work with API in [TelegramBot](./neura/TelegramBot.py)

the TelegramBot Class give three objects :
- admin : is a Telethon client
- group  : the group that you choose to work with
- users : all users in that goup

## TODO
- [ ] ~switch from **tkinter** to better library since tk doesn't support arabic or  Asynchronous functions~ , we find a workaround using tkinter
- [ ] use **pyistaler** to create a standalone executable file
- [ ] Main Window ues Tabs insted of buttons

