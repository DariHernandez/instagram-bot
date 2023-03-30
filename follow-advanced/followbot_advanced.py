# Move path directory, for import modules in parent folder
import os, sys, inspect, json
currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 

import time as t

from scraping_manager.followbot import FollowBot

class FollowBotAdvanced (FollowBot):
    
    def __init__ (self):
        super ().__init__()
        
    def __get_profiles__ (self, user, followers): 
        """
        Return the profile link of the followers, from specific user
        """
                
        # Print data and save in log file
        print("Taking follower's link from post likes and comments...")
        
        # read followed file
        followed_path = os.path.join (os.path.dirname(__file__), "followed.txt")
        with open (followed_path) as file: 
            followed_text = file.read()
            self.followed_list = followed_text.split("\n")
        
        post_links = self.__get_post__()
        
        for post_link in post_links: 
            
            status = f"post {post_links.index(post_link) + 1} / {len(post_link)}: {post_link}"
            print (status)
            
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
            self.__get_links__(selector_link, selector_down, load_more_selector=selector_load_more)
            
            # Get likes profile links
            t.sleep(1)
            self.scraper.refresh_selenium()
            selector_likes = "._ae5m._ae5n._ae5o a"
            try:
                self.scraper.click_js(selector_likes)
            except: 
                pass
            else: 
                self.scraper.refresh_selenium()
                t.sleep(1)
                
                # Get like profiles
                selector_link = ".x7r02ix.xf1ldfh.x131esax .xt0psk2 > .xt0psk2 > a"
                selector_down = '[role="dialog"] [style^="height: 356px;"]'
                self.__get_links__(selector_link, selector_down)
                            
        # Update followed file
        all_followed = self.profile_links + self.followed_list
        all_followed_text = "\n".join(all_followed)
        with open (followed_path, "w") as file:
            file.write(all_followed_text)
            
        # Print data and save in log file
        print('Follow List Length {}'.format(len(self.profile_links)))
        return self.profile_links
