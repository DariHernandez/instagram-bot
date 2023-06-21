<div><a href='https://github.com/darideveloper/instagram-bot/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/darideveloper/instagram-bot.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/instagram-bot/blob/master/logo.png?raw=true' alt='Instagram Bot' height='80px'/>

# Instagram Bot

Bot to publish and interact with users, on instagram, with seleium

Project type: **client**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#install'>Install</a></li>
<li><a href='#settings'>Settings</a></li>
<li><a href='#run'>Run</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://www.microsoft.com/es-mx/microsoft-365/excel/?rtc=1' target='_blank'> <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/2203px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png' alt='Excel' title='Excel' height='50px'/> </a><a href='https://www.selenium.dev/' target='_blank'> <img src='https://cdn.svgporn.com/logos/selenium.svg' alt='Selenium' title='Selenium' height='50px'/> </a></div>

# Install

## Tird party modules

Install all modules from pip: 

``` bash
$ pip install -r requirements.txt
```

## Programs

To run the project, the following programs must be installed:: 

* [Google Chrome](https://www.google.com/intl/es/chrome) last version

# Settings

## config.json

``` json
{
    "debug_user": "darialternative",
    "debug_pass": "@&97eJcAnf!NG>B",
    "debug_list_follow": ["elonrmuskk"],
    "debug_max_follow": 50
}
```

* debug_user: Login user for use in debug mode
* debug_pass: Login password for use in debug mode
* debug_list_follow: List of users target for get the list of user to follow, in deb ug mode
* debug_max_follow: Max number of user to follow, in debug mode

# Run

## Follow advanced
Follow users (follow and like their last 3 publications), who have interacted (like and comments) in the last 10 publications of the target user.

### Run bot
Run the file **instagram botFollow advanced__main__.py** with your python 3.9 interpreter.

### Regular mode
For run the bot in regular mode (in headless, without debug options), the main file should look like: 

``` python
from followbot_advanced import FollowBot

# Instance of bot
bot = FollowBot(debug_mode=False, headless=True)

# Run bot
bot.autofollow()
```

### Debug mode
The debugging mode will carry out the entire process of the bot, with the following differences:
* Will not update the **"followed.txt"** file (where currently followed users are stored).
* It will open the user profile, but will not press the follow button.
* Will open posts, but will not like.

For run the bot in debug mode the main file should look like: 

``` python
from followbot_advanced import FollowBot

# Instance of bot
bot = FollowBot(debug_mode=True, headless=False)

# Run bot
bot.autofollow()
```

---

## Follow classic
Follow users (follow and like their last 3 posts), who follow a target user.

### Run bot
Run the file **instagram botFollow classic__main__.py** with your python 3.9 interpreter.

### Regular mode
For run the bot in regular mode (in headless, without debug options), the main file should look like: 

``` python
from followbot_classic import FollowBot

# Instance of bot
bot = FollowBot(debug_mode=False, headless=True)

# Run bot
bot.autofollow()
```

### Debug mode
The debugging mode will carry out the entire process of the bot, with the following differences:
* Will not update the **"followed.txt"** file (where currently followed users are stored).
* It will open the user profile, but will not press the follow button.
* Will open posts, but will not like.

For run the bot in debug mode the main file should look like: 

``` python
from followbot_classic import FollowBot

# Instance of bot
bot = FollowBot(debug_mode=True, headless=False)

# Run bot
bot.autofollow()
```

---

## Post
Make publications based on schedules and settings saved in a spreadsheet.

### Run bot
Run the file **instagram botPost__main__.py** with your python 3.9 interpreter.

### Regular mode
For run the bot in regular mode (in headless, without debug options), the main file should look like: 

``` python
from postbot import PostBot

# Image folder
directory = "To Publish" 

# Xlsx files with data to post
filename = "Bot Manager.xlsx"

# Instance of bot
bot = PostBot(xlsx_file=filename, img_dir=directory, debug_mode=False, headless=True)

# Run bot
bot.autopost()

```

### Debug mode
The debug mode will ignore the publication times and immediately publish the scheduled photos.
it does not affect the spreadsheet or move the images folder after publishing.

For run the bot in debug mode the main file should look like: 

``` python
from postbot import PostBot

# Image folder
directory = "To Publish" 

# Xlsx files with data to post
filename = "Bot Manager.xlsx"

# Instance of bot
bot = PostBot(xlsx_file=filename, img_dir=directory, debug_mode=True, headless=False)

# Run bot
bot.autopost()

```

