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
        self.unfullowed_path = os.path.join (self.current_folder, "unfollowed.txt")
        
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
        
        # Read followed file
        if option == "1": 
            followed_path = os.path.join (self.parent_folder, "follow-advanced", "followed.txt")
        elif option == "2":
            followed_path = os.path.join (self.parent_folder, "follow", "followed.txt")
            
        with open (followed_path) as file: 
            followed_text = file.read()
            followed_list = followed_text.split("\n")
            
        # Read unfollowed file
        with open (self.unfullowed_path, encoding='UTF-8') as file: 
            unfollowed_text = file.read()
            unfollowed_list = unfollowed_text.split("\n")
            
        # Remove unfollowed users from followed list
        user_to_unfollow = list(filter (lambda user: user not in unfollowed_list, followed_list))
            
        return user_to_unfollow
            
    def __get_unfollowed_users__ (self) -> list:
        """ Load list of unfollowed users from text file

        Returns:
            list: lis of already unfollowed users
        """
        
        with open (self.unfullowed_path, encoding='UTF-8', newline="") as file: 
            unfollowed_list = file.read().split("\n")
            
        return unfollowed_list
    
    def __wait__ (self, message=""):
        t.sleep (random.randint(30, 180))
        if message:
            print (message)
        
            
    def unfollow (self):
        """ Unfollow users from followed list """
        
        print ("Starting unfollow process...")
                    
        for link in self.followed_list: 
            
            already_unfollowed = False
                        
            # Skip if already unfollowed
            if link in self.unfollowed:
                self.__wait__ (f"Already unfollowed: {link}")
                already_unfollowed = True
            
            if not already_unfollowed:
                # Load page
                self.set_page (link)
                t.sleep (2)
                self.refresh_selenium()
                
                # Validate follow text
                selector_follow = "header button._acan._acap._aj1-"
                follow_text = self.get_text (selector_follow)
                
                # Skip already unfollowed user
                if follow_text.lower().strip() == "follow":
                    self.__wait__ (f"Already unfollowed: {link}")
                    already_unfollowed = True
            
            if not already_unfollowed:
                # Click unfollow button
                self.click_js (selector_follow)
                self.refresh_selenium()
                
                # Confirm unfollow (if the follow status its on "request")
                selector_confirm = ".x78zum5.xdt5ytf > button:nth-child(2)"
                try:
                    self.get_elem (selector_confirm)
                except:
                    pass
                else:
                    self.click_js (selector_confirm)
                    
                # Confirm unfollow (alredy followed users)
                selector_confirm = '.x1cy8zhl .x9f619 > div[role="button"]:last-child'
                try:
                    self.get_elem (selector_confirm)
                except:
                    pass
                else:
                    self.click_js (selector_confirm)
                              
            # Save in unfollowed file
            with open (self.unfullowed_path, "a", encoding='UTF-8') as file: 
                file.write (f"\n{link}")
                
            self.__wait__ (f"Unfollowed: {link}")
        

    