# Import Packages
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time, os, sys
from scraping_manager.automate import Web_scraping

class LogIn (Web_scraping):
    
    def __init__(self, user, password, headless=False, mobile=True):
        
        self.host = "https://www.instagram.com/"
        
        # Set user agent for mobile and desktop
        self.mobile = mobile
        if self.mobile:
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1"
        else: 
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Create selenium instance
        super().__init__(web_page=self.host, 
                         headless=headless, 
                         user_agent=user_agent)
        
        print ("Login to Instagram...")
        
        self.user = user
        self.password = password
        
        self.__auth__()
                
    def __auth__(self):
        
        # Accept cookies
        selector_cookies = "body > div.RnEpo.Yx5HN._4Yzd2 > div > div > button.aOOlW.bIiDR"
        try:
            self.wait_load(selector_cookies)
        except: 
            pass
        else: 
            self.click_js(selector_cookies)
            
        
        # Change language to english
        self.refresh_selenium()
        selector_lan = 'option[value="en"]'
        self.wait_load(selector_lan)
        self.click(selector_lan)
        
        # Go to login page in mobile
        if self.mobile: 
            selector_login = "button:nth-child(1)._aicz._acan._acao._acas"
            self.click_js(selector_login)
            self.refresh_selenium()
        
        # Send user and password
        selector_user = 'input[type="text"]'
        selector_pass = 'input[type="password"]'
        
        self.send_data(selector_user, self.user)
        self.send_data(selector_pass, self.password)
        
        # Submit crdentials
        selector_submit = 'button[type="submit"]'
        self.click_js(selector_submit)
        
        # Dont save login
        selector_not_save = "#react-root > section > main > div > div > div button"
        try:
            self.wait_load(selector_not_save)
        except: 
            pass 
        else:
            self.click(selector_not_save)
        
        # Dont add instagram to home screen
        if self.mobile:
            selector_not_add = "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm"
            try: 
                self.wait_load(selector_not_add)
            except: 
                pass
            else: 
                self.click(selector_not_add)
        
        self.refresh_selenium()
            
    