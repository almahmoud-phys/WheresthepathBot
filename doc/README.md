# Documentation


## get telegram api keys

first you need API keys ([here](https://core.telegram.org/api/obtaining_api_id))

## Install

1. `git clone https://github.com/Aamerbassmaji/WheresthepathBot`
1. `pip install -r requirements.txt`
2. Since the program still in beta you can go to [Constants](./neura/Constants.py) and chage telegram API parameters and phne number , **don't change the group id**
3. run `python main.py`
4. if it's the first run the app will ask for code send to you telegram app to confirm login




## Contribution

to add new features only two files need to be modified : All gui should be in [TelegramBotGUI](./neura/TelegramBotGUI.py) and work with API in [TelegramBot](./neura/TelegramBot.py)


**Note** ; Don't modify files other than  [TelegramBotGUI](./neura/TelegramBotGUI.py) and [TelegramBot](./neura/TelegramBot.py) without contacting the owner


the TelegramBot Class give three objects :
- admin : is a [ Telethon client ](https://docs.telethon.dev/en/stable/modules/client.html) , you can do all telegram tasks with it (send messages , make phone calls .....)
- group  : the group that you choose to work with
- users : a dictionary Constants all users in that group

with these three objects you can do basically anything in telegram


to display arabic correctly use [display_arabic_text](./neura/utils.py) function


