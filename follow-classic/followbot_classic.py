# Move path directory, for import modules in parent folder
import os, sys, inspect, json
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import os
import random
import getpass
import time as t
import config 
from login import LogIn
from log import Log

class FollowBot():
    """ Auto follow users
    
    Follow a certain number of followers of the specified users, 
    and like the last three posts of the followed users.
    """

    def __init__(self):  
        
        # Save class vars
        self.debug_mode = config.get_credential("debug_mode")
        self.headless = config.get_credential("headless")
        self.total_followed = 0
        
        # logs instance
        self.logs = Log(os.path.basename(__file__))
        self.logs.info (f"Follow bot classic: debug_mode: {debug_mode}, headless: {headless}")

        if self.debug_mode:
            
            # Get credentials
            self.user = config.get_credential("debug_user")
            self.password = config.get_credential("debug_pass")
            
            # Get users to follow
            self.user_list = config.get_credential("debug_list_follow")
            self.max_follow =  config.get_credential("debug_max_follow")
            
        else: 
            
            # Inputs and User Prompts in not debug mode
            print("""
            Welcome to Follow Bot by @Dango!

            Please make sure that the Bot Manager.xlsx file is close before running.

            Hope you enjoy it. Please reachout for any ideas/issues you may have.

            Cheers!
            -Dango
            """)

            # Requests crdentials
            self.user = input('Please enter your instagram user: ')
            self.password = getpass.getpass('Please enter your instagram password: ')
            
            # Get users to follow 
            self.user_list = input('What user(s) do you want to follow? You can enter Multiple Usernames. ').split(' ')
            
            incorrect_input = True
            while True:
                try: 
                    # Ask again until a number is entered
                    self.max_follow = int(input('How many users do you want to follow? '))
                except: 
                    continue
                else: 
                    break
            
        # Login to driver
        self.logs.info ("Start login...")
        self.scraper = LogIn(self.user, self.password, self.headless, mobile=False)
        self.driver = self.scraper.driver 
        

    def __get_followers_num__ (self, user): 
        """
        Get the number of the total followers, from the main user page, 
            and return the number
        """
        
        self.logs.info ("Getting number of followers...")
        
        # Go to main user page 
        user_page = f"https://www.instagram.com/{user}/"
        self.scraper.set_page(user_page)
        t.sleep(5)

        selector_followers = "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span"
        
        # Get number of followers
        followers = self.scraper.get_text (selector_followers)

        # Validate user
        if followers: 
            return followers
        else: 
            # Print data and save in log file
            self.logs.info("User '{}' not found.".format(os.path.basename(user)), print_text=True)
            return None

    def __get_profiles__ (self, user, followers): 
        """
        Return the profile link of the followers, from specific user
        """
        
        self.logs.info("Taking follower's link...", print_text=True)
        
        # read followed file
        followed_path = os.path.join (os.path.dirname(__file__), "followed.txt")
        with open (followed_path) as file: 
            followed_text = file.read()
            followed_list = followed_text.split("\n")

        # Print data and save in log file
        
        # Open followers pop 
        selector_followers = "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a"
        self.scraper.click(selector_followers)

        profile_links = []
        more_links = True
        while more_links: 

            # Get all profile links
            self.scraper.refresh_selenium()
            t.sleep(1)
            selector_profile = "li div span > a"
            links = self.scraper.get_attribs(selector_profile, "href", allow_duplicates=False, allow_empty=False)
            
            # Validate each link
            for link in links: 
                
                # Skip tag links
                if "explore/tags" in link: 
                    continue
                    
                if (link not in followed_list
                    and link not in profile_links): 
                    profile_links.append(link)
                    
                # Count number of links
                links_num = len (profile_links)
                if links_num == self.max_follow: 
                    more_links = False
                    break
                
            # Focus on user list
            selector_last_profile = f".PZuss"
            self.scraper.go_bottom(selector_profile)
            t.sleep(1)
            
        # Update followed file
        all_followed = profile_links + followed_list
        all_followed_text = "\n".join(all_followed)
        with open (followed_path, "w") as file:
            file.write(all_followed_text)
            
        # Print data and save in log file
        self.logs.info('Follow List Length {}'.format(len(profile_links)), print_text=True)
        return profile_links

    def __like_post_follow__ (self, profile, profile_index, profile_limit):
        """
        Like the last 3 post from specific user profile, and follow 
        """
        
        self.logs.info ("Starting likes and follow...")

        # Go to user page
        self.scraper.set_page(profile)
        self.scraper.refresh_selenium()

        msg = "Current profile ({}/{}): {}".format(profile_index, profile_limit, profile)
        self.logs.info(msg, print_text=True)
        
        # Follow and like only not followed users 
        selector_follow = "div.Igw0E div div button"

        # Validate profile
        follow_text = self.scraper.get_text(selector_follow)
        if follow_text:
            
            self.total_followed += 1

            # Get number of post of the user 
            post_to_like = 3
            selector_post = "#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div > a"
            post_links = self.scraper.get_attribs(selector_post, "href")
            total_post = len(post_links)
            if total_post < 3:
                post_to_like = total_post
            
            
            # Click follow button
            secs = random.randint(30, 180)
            t.sleep(secs)
            if not self.debug_mode:
                self.scraper.click_js(selector_follow)
                self.logs.info("\tUser followed", print_text=True)
            secs = random.randint(30, 180)
            t.sleep(secs)

            # Like each post (the last three)
            for post_link in post_links[:post_to_like]: 
                
                self.scraper.set_page(post_link)
                secs = random.randint(30, 180)
                t.sleep(secs)
                if not self.debug_mode:
                    selector_like = "div.eo2As > section.ltpMr.Slqrh > span.fr66n > button"
                    self.logs.info(f"\tPost {post_links.index(post_link) + 1} / 3 liked", print_text=True)
                    self.scraper.click_js(selector_like)
                secs = random.randint(30, 180)
                t.sleep(secs)
                

    def autofollow (self): 
        """
        Main flow of the follow script
        """
        
        self.logs.info("Running autofollow")

        # Loop for each user in list
        for user in self.user_list: 
            
            self.logs.info(f"Target user: {user}")

            # Get the number of followers and validate user
            followers = self.__get_followers_num__(user) 

            # Only continue with valid users
            if followers: 

                # Print data and save in log file
                print ("\n")
                self.logs.info("User '{}'".format(os.path.basename(user)), print_text=True)
                self.logs.info("Followers Number: {}".format(followers), print_text=True)
                self.logs.info("Limit: {}".format(self.max_follow), print_text=True)
                
                profiles = self.__get_profiles__(user, followers)

                # Print data and save in log file
                self.logs.info("Initiating auto following and upvoting...", print_text=True)

                # Loop for each profile of followers 
                profile_limit = len(profiles)
                for profile in profiles: 

                    profile_index = profiles.index(profile) + 1
                    self.__like_post_follow__(profile, profile_index, profile_limit)

        # Print data and save in log file
        print ("\n")
        self.logs.info("Total users followed: '{}'".format(self.total_followed), print_text=True)
        self.scraper.end_browser()


