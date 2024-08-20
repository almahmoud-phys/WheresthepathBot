# WheresthepathBot

## Usage

1. `pip install -r requirements.txt`
2. Since the program still in beta you can go to [Constants](./neura/Constants.py) and chage telegram API parameters
3. `python main.py`

## Contribution

first you need API keys ([here](https://core.telegram.org/api/obtaining_api_id))


to add new features only two files need to be modified : All gui should be in [TelegramBotGUI](./neura/TelegramBotGUI.py) and work with API in [TelegramBot](./neura/TelegramBot.py)

the TelegramBot Class give three objects :
- admin : is a [ Telethon client ](https://docs.telethon.dev/en/stable/modules/client.html) , you can do all telegram tasks with it (send messages , make phone calls .....)
- group  : the group that you choose to work with
- users : a dictionary Constants all users in that group

with these three objects you can do basically anything in telegram


to display arabic correctly use [display_arabic_text](./neura/utils.py) function


## TODO
- [ ] ~switch from **tkinter** to better library since tk doesn't support arabic or  Asynchronous functions~ , we find a workaround using [insolor/async-tkinter-loop](https://github.com/insolor/async-tkinter-loop)
- [ ] use **pyistaler** to create a standalone executable file
- [ ] Main Window ues Tabs insted of buttons

