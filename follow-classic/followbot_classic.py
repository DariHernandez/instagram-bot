# Move path directory, for import modules in parent folder
import os, sys, inspect, json
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import time as t

from scraping_manager.followbot import FollowBot

class FollowBotClassic (FollowBot):
    
    def __init__ (self):
        super ().__init__()
        
    def __get_profiles__ (self, user, followers): 
        """
        Return the profile link of the followers, from specific user
        """
                
        print("Taking follower's link...")
        
        # read followed file
        followed_path = os.path.join (os.path.dirname(__file__), "followed.txt")
        with open (followed_path) as file: 
            followed_text = file.read()
            followed_list = followed_text.split("\n")

        # Print data and save in log file
        
        # Open followers pop 
        selector_followers = "ul.x78zum5.x1q0g3np.xieb3on > li:nth-child(2) > a"
        self.scraper.click(selector_followers)
        self.scraper.refresh_selenium()
            
        # Load more followers
        selector_link = ".x7r02ix.xf1ldfh.x131esax .xt0psk2 > .xt0psk2 > a"
        selector_down = '[role="dialog"] ._aano'
        self.__get_links__(selector_link, selector_down, scroll_by=3000)

        # Get all profile links
        self.scraper.refresh_selenium()
        t.sleep(1)
        links = self.scraper.get_attribs(selector_link, "href", allow_duplicates=False, allow_empty=False)
        
        # Validate each link
        profile_links = []
        for link in links: 
            
            # Skip tag links
            if "explore/tags" in link: 
                continue
                
            if (link not in followed_list and link not in profile_links): 
                profile_links.append(link)
                
            # Detect limit of user
            if len(profile_links) >= self.max_follow: 
                break
            
        # Update followed file
        all_followed = profile_links + followed_list
        all_followed_text = "\n".join(all_followed)
        with open (followed_path, "w") as file:
            file.write(all_followed_text)
            
        # Return data
        return profile_links