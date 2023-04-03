# Move path directory, for import modules in parent folder
import os, sys, inspect, json
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 


import os
import abc
import random
import getpass
import time as t
import config 
from login import LogIn

class FollowBot(metaclass=abc.ABCMeta):
    """ Auto follow users
    
    Follow a certain number of followers of the specified users, 
    and like the last three posts of the followed users.
    """

    def __init__(self):  
        
        # Save class vars
        self.debug_mode = config.get_credential("debug_mode")
        self.headless = config.get_credential("headless")
        self.total_followed = 0
        self.profile_links = []
        self.followed_list = []
        
        print (f"Follow bot advanced: debug_mode: {self.debug_mode}, headless: {self.headless}")

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
        print ("Start login...")
        self.scraper = LogIn(self.user, self.password, self.headless, mobile=False, debug=self.debug_mode)
        self.driver = self.scraper.driver 
        

    def __get_followers_num__ (self, user): 
        """
        Get the number of the total followers, from the main user page, 
            and return the number
        """
        
        print ("Getting number of followers...")
        
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
            print("User '{}' not found.".format(os.path.basename(user)))
            return None
        

    def __get_links__ (self, selector_link, selector_down, load_more_selector="", scroll_by=0): 
        """
        Extract links from specific selects, and go down in the page for load the next links
        Save links in class variable "profile_links"
        """
        
        # Get unfollowed users from file
        current_folder = os.path.dirname(__file__)
        parent_folder = os.path.dirname(current_folder)
        unfollowed_file = os.path.join (parent_folder, "unfollow", "unfollowed.txt")
        with open (unfollowed_file, "r") as file:
            unfollowed = file.read().split ("\n")
                
        print ("Getting links...")
        
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
                
                if link not in self.followed_list and link not in self.profile_links and link not in unfollowed: 
                    self.profile_links.append(link)
                    
                # Count number of links
                links_num = len (self.profile_links)
                if links_num >= self.max_follow: 
                    more_links = False
                    break
            
            
            # Go down with js
            try:
                elem = self.scraper.get_elem (selector_down)
            except:
                pass
            else:
                self.scraper.driver.execute_script(f"arguments[0].scrollBy (0, {scroll_by});", elem)
            
            # Click button for load more results
            if load_more_selector:
                try:
                    load_more_btn = self.scraper.get_elem (load_more_selector)
                except:
                    pass
                else:
                    self.scraper.click_js (load_more_selector)
                    t.sleep(3)
        

    @abc.abstractmethod
    def __get_profiles__ (self, user, followers): 
        """
        Return the profile link of the followers, from specific user
        """
        
        pass
        
    def __get_post__ (self, max_post = 100): 
        """
        Get the post links of the current user
        """
        
        print ("Getting post...")
        
        # Get number of post of the user 
        selector_post = "._ac7v._al3n ._aabd._aa8k._al3l a"
        post_links = self.scraper.get_attribs(selector_post, "href")
        if len(post_links) > max_post: 
            post_links = post_links[:max_post]

        return post_links
        

    def __like_post_follow__ (self, profile, profile_index, profile_limit):
        """
        Like the last 3 post from specific user profile, and follow 
        """
        
        print ("Starting likes and follow...")
        
        # Go to user page
        self.scraper.set_page(profile)
        self.scraper.refresh_selenium()

        msg = "Current profile ({}/{}): {}".format(profile_index, profile_limit, profile)
        print(msg)
        
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
        print("\tUser followed")
        t.sleep(secs)

        # Like each post (the last three)
        for post_link in post_links: 
            
            self.scraper.set_page(post_link)
            t.sleep(secs)
            selector_like = ".x78zum5 > span.xp7jhwk:first-child > button"
            print(f"\tPost {post_links.index(post_link) + 1} / 3 liked")
            try:
                self.scraper.click_js(selector_like)
            except:
                print ("\t\tlike button not found")
            t.sleep(secs)

    def autofollow (self): 
        """
        Main flow of the follow script
        """
        
        print("Running autofollow")

        # Loop for each user in list
        for user in self.user_list: 
            
            print(f"Target user: {user}")

            # Get the number of followers and validate user
            followers = self.__get_followers_num__(user) 

            # Only continue with valid users
            if followers: 

                # Print data and save in log fileº
                print ("\n")
                print("User '{}'".format(os.path.basename(user)))
                print("Followers Number: {}".format(followers))
                print("Limit: {}".format(self.max_follow))
                
                profiles = self.__get_profiles__(user, followers)
                
                # Print data and save in log file
                print("Initiating auto following and upvoting...")

                # Loop for each profile of followers 
                profile_limit = len(profiles)
                for profile in profiles: 

                    profile_index = profiles.index(profile) + 1
                    self.__like_post_follow__(profile, profile_index, profile_limit)

        # Print data and save in log file
        print ("\n")
        print("Total users followed: '{}'".format(self.total_followed))
        self.scraper.end_browser()


