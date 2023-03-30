# Move path directory, for import modules in parent folder
import os 
import sys
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import shutil
import config
import getpass
import datetime
import time as t
import pandas as pd
from log import Log
from login import LogIn
from pytz import timezone

class PostBot():
    """ Auto post text or photo
    
    Post a text or image, from data in xlsx file. 
    After post an image, move this from folder "To Publish" to folder "Published"
    """

    def __init__(self, img_dir, xlsx_file):  


        # Save class vars
        self.debug_mode = config.get_credential("debug_mode")
        self.headless = config.get_credential("headless")
        
        # logs instance
        self.logs = Log(os.path.basename(__file__))
        print (f"Post bot: debug_mode: {self.debug_mode}, headless: {self.headless}")

        # Files and folders 
        self.pubDone = os.path.join(currentdir, "Published")
        self.directory = os.path.join(currentdir, img_dir)
        self.filename = os.path.join(currentdir, xlsx_file)

        if self.debug_mode:
            
            # Get seed phrase from config json file
            self.user = config.get_credential("debug_user")
            self.password = config.get_credential("debug_pass")
            
        else: 
            
            # Inputs and User Prompts in not debug mode
            print("""
            Welcome to PostBot by @Dango!

            Please make sure that the Bot Manager.xlsx file is close before running.

            Hope you enjoy it. Please reachout for any ideas/issues you may have.

            Cheers!
            -Dango
            """)

            self.user = input('Please enter your instagram user: ')
            self.password = getpass.getpass('Please enter your instagram password: ')
            

    def __post_photo__(self, caps):
        
        print ("Posting photo")
        
        for cap in caps:
            
            if self.imgPost.loc[self.imgPost.Insta == cap].Used.tolist()[0] != "Yes":
                self.imgPost.loc[self.imgPost.Insta == cap, "Used"] = "Yes"           
                
                # Open browser en make login in each loop
                print ("Start login...")
                self.scraper = LogIn(self.user, self.password, self.headless, mobile=False)
                self.driver = self.scraper.driver 
                
                # self.__write_text__(cap)

                img_id = str(self.imgPost.loc[self.imgPost.Insta == cap].PhotoID.tolist()[0])                
                
                # Get all images in folder
                photoname = ""
                current_folder = os.path.dirname(__file__)
                images_folder = os.path.join(current_folder, self.directory)
                images = os.listdir(images_folder)
                
                # Loop for each image in folder
                for image in images: 
                    image_name = image[:image.find(".")]
                    
                    # Select image with correct name
                    if image_name == img_id: 
                        photoname = os.path.join(images_folder, image)
                        
                if not photoname or not os.path.isfile(photoname):
                    print (f"File {photoname} doesn't exists..")
                    break
                
                
                # Click on upload image button
                selector_input = ".xh8yej3.x1iyjqo2 > div:nth-child(7) .x1n2onr6 .x1n2onr6 > a"
                self.scraper.click(selector_input)
                self.scraper.refresh_selenium ()
                
                # Upload image
                selector_input = ".x1n2onr6.x78zum5.x5yr21d.xh8yej3 form > input"
                filepath = photoname
                self.scraper.send_data(selector_input, filepath)                
                t.sleep(10)
                
                # Go next
                selector_next = "._ac7b._ac7d > .x9f619.xjbqb8w.x78zum5 > div"
                for _ in range (2):
                    self.scraper.wait_load(selector_next)
                    self.scraper.click(selector_next)
                
                # Write text
                selector_textarea = ".xw2csxc.x1odjw0f.x5dp1im.x1swvt13"
                self.scraper.wait_load(selector_textarea)
                self.scraper.send_data(selector_textarea, cap)
                    
                # Share post
                selector_share = selector_next
                self.scraper.wait_load(selector_share)
                self.scraper.click(selector_share)
                t.sleep (20)
                
                # save in published folder
                dirc = os.path.join(self.change_directory, os.path.basename(photoname))
                
                # No move images in no debug mode
                if not self.debug_mode: 
                    shutil.move(filepath, dirc)

                # End browser
                print ("Photo post uploaded...")
                t.sleep(1)
                break
            
        self.scraper.end_browser()

    def autopost(self):
        
        print ("Running auto post")
        root = os.path.dirname(__file__)
        self.change_directory = self.pubDone
        
        # Create to publish folder
        if not os.path.exists(self.change_directory):
            os.mkdir(self.change_directory)

        
        print ("Reading excel file...")
        xls = pd.ExcelFile(self.filename)
        self.imgPost = pd.read_excel(xls, "Photo Posts", keep_default_na=False)
        self.schedule = pd.read_excel(xls, "Schedule", keep_default_na=False)
        self.last_one = pd.read_excel(xls, "DO NOT TOUCH!")
        
        # essential datas
        # times = self.schedule["Time (EST)"].to_list()
        
        hours = self.schedule["Hour of Day (EST)"].to_list()
        minutes = self.schedule["Minute"].to_list()
        
        # ['01:53:00', '01:58:00']
        caps = self.imgPost["Insta"].to_list()

        tz = timezone('US/Eastern')
                        
        try:

            # Loop for each time in sheet
            for index_time in range(0, len(hours)):
                
                time_string = "{}:{}:00".format(hours[index_time], minutes[index_time])
                
                time_now = str(datetime.datetime.now(tz).time()).split('.')[0]
                                
                if self.debug_mode: 
                    print (time_string, time_now)

                # Convert hours string to date type
                time_formated = datetime.datetime.strptime(time_string, "%H:%M:%S")
                time_now_formated = datetime.datetime.strptime(time_now, "%H:%M:%S")
                
                # Convert hours to deltatime
                time_delta = datetime.timedelta(hours=time_formated.hour, minutes=time_formated.minute, seconds=time_formated.second)
                time_now_delta = datetime.timedelta(hours=time_now_formated.hour, minutes=time_now_formated.minute, seconds=time_now_formated.second)

                # Calculte the wait time
                wait_time = time_delta - time_now_delta
                wait_seconds = int(wait_time.total_seconds())
                
                if wait_seconds > 0 or self.debug_mode: 

                    if not self.debug_mode: 
                        print ("Waiting for time: {}...".format(time_string))
                        t.sleep(wait_seconds)
                                
                    # Post
                    if self.schedule.loc[index_time]["Type of Post"] != '':
                        if self.schedule.loc[index_time]["Type of Post"] == "Photo":
                            print("Calling photo function...")
                            self.__post_photo__(caps)
                        
                        t.sleep(10)
                        self.__save_excel__()
                else: 
                    # Skip negative times
                    print ("Post omitted. The current time is greater than: {}".format(time_string))


        except KeyboardInterrupt:
            self.__save_excel__()
            self.driver.quit()
            self.writer.close()
            a = False
                

    def __save_excel__(self):
        

        # Save in no debug
        if not self.debug_mode:
            print ("Saving data in file")
            writer = pd.ExcelWriter(
                self.filename, engine='openpyxl')
            self.imgPost.to_excel(
                writer, sheet_name="Photo Posts", index=False)
            self.schedule.to_excel(
                writer, sheet_name="Schedule", index=False)
            self.last_one.to_excel(
                writer, sheet_name="DO NOT TOUCH!", index=False)
            self.writer = writer
            self.writer.save()
            print ("File saved")

