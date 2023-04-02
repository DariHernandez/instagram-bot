# Move path directory, for import modules in parent folder
import os
import sys
import time as t
import random
import getpass

# Import modules from parent folder
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

from login import LogIn
import config

class Unfollow (LogIn):
    
    def __init__ (self):    
        
        # List of unfollowed users
        self.unfollowed = []
        
        # Paths
        self.current_folder = os.path.dirname(__file__)
        self.parent_folder = os.path.dirname(self.current_folder)
        self.unfullowed_path = os.path.join (self.parent_folder, "unfollowed.txt")
        
        # Get credentials from config file
        self.debug_mode = config.get_credential("debug_mode")
        self.headless = config.get_credential("headless")
        
        if self.debug_mode:
            
            # Get debug credentials
            self.user = config.get_credential("debug_user")
            self.password = config.get_credential("debug_pass")
        else:
            # Request credentials
            self.user = input('Please enter your instagram user: ')
            self.password = getpass.getpass('Please enter your instagram password: ')
        
        # Login
        super ().__init__(user=self.user, password=self.password, mobile=False, headless=self.headless, debug=self.debug_mode)
        
        # Load data
        self.followed_list = self.__get_followed_users__ ()
        self.unfollowed = self.__get_unfollowed_users__ ()
        
    def __get_followed_users__ (self) -> list:
        """ Request to the user and save as atribute the list of followed users from text files

        Returns:
            list: list of followed users to unfollow
        """
        
        # Request follow file to user
        manu_options = ["1", "2"]
        while True:
            print ("1. Follow Advanced")
            print ("2. Follow Classic")
            option = input ("Select folloed list, for unfollow: ")
            if option not in manu_options: 
                print ("\nInvalid option")
                continue
            else:
                break
            
        if option == "1": 
            followed_path = os.path.join (self.parent_folder, "follow-advanced", "followed.txt")
        elif option == "2":
            followed_path = os.path.join (self.parent_folder, "follow", "followed.txt")
            
        with open (followed_path) as file: 
            followed_text = file.read()
            self.followed_list = followed_text.split("\n")
            
    def __get_unfollowed_users__ (self) -> list:
        """ Load list of unfollowed users from text file

        Returns:
            list: lis of already unfollowed users
        """
        
        with open (self.unfullowed_path, encoding='UTF-8', newline="") as file: 
            self.unfollowed = file.read().split("\n")
            
    def unfollow (self):
        """ Unfollow users from followed list """
            
        for link in self.followed_list: 
            
            # Skip if already unfollowed
            if link in self.unfollowed:
                continue
            
            # Click unfollow button
            self.set_page (link)
            self.refresh_selenium()
            selector_follow = "header button._acan._acap._aj1-"
            self.click_js (selector_follow)
            
            # Confirm unfollow (if model exists)
            selector_confirm = ".x78zum5.xdt5ytf > button:nth-child(2)"
            try:
                self.get_elem (selector_confirm)
            except:
                pass
            else:
                self.click_js (selector_confirm)
                            
            print (f"Unfollowed: {link}")
            
            # Wait after unfollow
            t.sleep (random.randint(30, 180))
            
            # Save in unfollowed file
            with open (self.unfullowed_path, "a", encoding='UTF-8', newline="") as file: 
                file.write (f"{link}")
            
        

    