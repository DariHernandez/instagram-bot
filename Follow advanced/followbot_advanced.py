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

    def __init__(self, debug_mode=False, headless=True):  
        
        
        # Save class vars
        self.debug_mode = debug_mode
        self.headless = headless
        self.total_followed = 0
        self.profile_links = []
        self.followed_list = []
        
        # logs instance
        self.logs = Log(os.path.basename(__file__))
        self.logs.info (f"Follow bot advanced: debug_mode: {debug_mode}, headless: {headless}")

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

        # selector_followers = "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span"
        selector_followers = "li:nth-child(2) span._ac2a > span"
        
        # Get number of followers
        followers = self.scraper.get_text (selector_followers)

        # Validate user
        if followers: 
            return followers
        else: 
            # Print data and save in log file
            self.logs.info("User '{}' not found.".format(os.path.basename(user)), print_text=True)
            return None
        

    def __get_links__ (self, selector_link, selector_down, scroll_js=False, load_more_selector=""): 
        """
        Extract links from specific selects, and go down in the page for load the next links
        Save links in class variable "profile_links"
        """
                
        self.logs.info ("Getting links...")
        
        more_links = True
        last_links = []
        while more_links: 
            
            # Get all profile links
            self.scraper.refresh_selenium()
            t.sleep(3)
            links = self.scraper.get_attribs(selector_link, "href", allow_duplicates=False, allow_empty=False)
            
            # Break where no new links
            if links == last_links: 
                break
            else: 
                last_links = links
            
            # Validate each link
            for link in links: 
                
                # Skip tag links
                if "explore/tags" in link: 
                    continue
                
                if link not in self.followed_list and link not in self.profile_links: 
                    self.profile_links.append(link)
                    
                # Count number of links
                links_num = len (self.profile_links)
                if links_num >= self.max_follow: 
                    more_links = False
                    break
            
            
            # Go down with js
            if scroll_js:
                elem = self.scraper.get_elem (selector_down)
                self.scraper.driver.execute_script("arguments[0].scrollBy (0, 2500);", elem)
                
            # try to go down with selenium
            else:
                try: 
                    for _ in range (5):
                        self.scraper.go_down(selector_down)
                        t.sleep(2)
                except: 
                    continue
                else:
                    t.sleep(1)
                
            # Click button for load more results
            if load_more_selector:
                load_more_btn = self.scraper.get_elem (load_more_selector)
                if load_more_btn:
                    self.scraper.click_js (load_more_selector)
        

    def __get_profiles__ (self, user, followers): 
        """
        Return the profile link of the followers, from specific user
        """
        
        # Print data and save in log file
        self.logs.info("Taking follower's link from post likes and comments...", print_text=True)
        
        # read followed file
        followed_path = os.path.join (os.path.dirname(__file__), "followed.txt")
        with open (followed_path) as file: 
            followed_text = file.read()
            self.followed_list = followed_text.split("\n")
        
        post_links = self.__get_post__()
        
        for post_link in post_links: 
            
            status = f"post {post_links.index(post_link) + 1} / 10: {post_link}"
            self.logs.info (status, print_text=True)
            
            # End loop when found all max profile links
            links_num = len (self.profile_links)
            if links_num >= self.max_follow: 
                more_links = False
                break
            
            # Go to post page
            self.scraper.set_page(post_link)
            t.sleep(1)
            self.scraper.refresh_selenium()
            
            # Get comments profile links
            selector_link = "ul._a9ym .xt0psk2 > a"
            selector_down = "._ae5q._akdn._ae5r._ae5s ul._a9z6._a9za"
            selector_load_more = "div._ae5q._akdn._ae5r._ae5s > ul > li > div > button"
            self.__get_links__(selector_link, selector_down, scroll_js=True, load_more_selector=selector_load_more)
            
            # Get likes profile links
            t.sleep(1)
            self.scraper.refresh_selenium()
            selector_likes = "article > div.eo2As > section.EDfFK.ygqzn > div > div > a"
            try:
                self.scraper.click_js(selector_likes)
            except: 
                pass
            else: 
                self.scraper.refresh_selenium()
                t.sleep(1)
                
                # Get like profiles
                selector_link = "div div span > a"
                selector_down = "body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div:last-child > div.Igw0E.rBNOH.YBx95.ybXk5._4EzTm.soMvl > button"
                self.__get_links__(selector_link, selector_down)
                            
        # Update followed file
        all_followed = self.profile_links + self.followed_list
        all_followed_text = "\n".join(all_followed)
        with open (followed_path, "w") as file:
            file.write(all_followed_text)
            
        # Print data and save in log file
        self.logs.info('Follow List Length {}'.format(len(self.profile_links)), print_text=True)
        return self.profile_links

    def __get_post__ (self, max_post = 10): 
        """
        Get the post links of the current user
        """
        
        self.logs.info ("Getting post...")
        
        # Get number of post of the user 
        # selector_post = ".Nnq7C.weEfm > .v1Nh3.kIKUG._bz0w > a"
        selector_post = "._ac7v._al3n ._aabd._aa8k._al3l a"
        post_links = self.scraper.get_attribs(selector_post, "href")
        total_post = len(post_links)
        if total_post < max_post:
            max_post = total_post
            

        return post_links[:max_post]
        

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
        selector_follow = "header button._acan._acap._acas._aj1-"

        self.total_followed += 1

        # Get number of post of the user 
        post_links = self.__get_post__(3)
            
        # Generate wait time
        secs = random.randint(30, 180)
        if self.debug_mode:
            secs = 5
            
        # Click follow button
        try:
            self.scraper.click_js(selector_follow)
        except:
            pass
        self.logs.info("\tUser followed", print_text=True)
        t.sleep(secs)

        # Like each post (the last three)
        for post_link in post_links: 
            
            self.scraper.set_page(post_link)
            t.sleep(secs)
            selector_like = "._aamu._ae3_._ae47._ae48 button:first-child._abl-"
            self.logs.info(f"\tPost {post_links.index(post_link) + 1} / 3 liked", print_text=True)
            self.scraper.click_js(selector_like)
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


