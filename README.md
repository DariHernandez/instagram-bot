# INSTAGRAM BOT
**python version: 3.9**

Bot to publish and interact with users, on instagram, with seleium.

# Install
## Tird party modules

Install all modules from pip: 

``` bash
$ pip install -r requirements.txt
```

## Programs

To run the project, the following programs must be installed:: 

* [Google Chrome](https://www.google.com/intl/es/chrome) last version

# Run the program

---

## Follow advanced
Follow users (follow and like their last 3 publications), who have interacted (like and comments) in the last 10 publications of the target user.

### Run bot
Run the file **instagram bot\Follow advanced\__main__.py** with your python 3.9 interpreter.

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
Run the file **instagram bot\Follow classic\__main__.py** with your python 3.9 interpreter.

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
Run the file **instagram bot\Post\__main__.py** with your python 3.9 interpreter.

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

# Configuration / setting

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
