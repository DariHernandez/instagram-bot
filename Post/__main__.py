from postbot import PostBot

# Image folder
directory = "To Publish" 

# Xlsx files with data to post
filename = "Bot Manager.xlsx"

# Instance of bot
bot = PostBot(xlsx_file=filename, img_dir=directory, debug_mode=False, headless=True)

# Run bot
bot.autopost()
