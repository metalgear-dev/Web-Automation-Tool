from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as firefoxOptions

from time import sleep
from random import uniform, randrange
from pynput.keyboard import Controller
import pyautogui
import threading
from os import path
from os import getcwd, getlogin, listdir
import psutil

from selenium_option import selenium_option

# wait beween two times
def wait_between(a, b):
    rand = uniform(a, b) 
    sleep(rand)

class selenium_driver():
    def __init__(self, initial_option):
        self.options = selenium_option(initial_conf=initial_option)
        self.print_log("now creating web driver...")
        self.driver = self.create_driver()

    def create_driver(self):
        cur_config = self.options._config

        # get executable driver absolute path
        folder_path = ""
        if cur_config['folder_path'] != "":
            folder_path = cur_config['folder_path']
        else:
            folder_path = path.join(path.dirname(path.realpath(__file__)), cur_config['browser_name'])

        file_lists = listdir(folder_path)
        self.driver_path = ""
        for file_item in file_lists:
            if file_item[-3:] == 'exe':
                self.driver_path = path.join(folder_path, file_item)               
        if self.driver_path == "":
            self.print_log("driver name not found")
            return None
        else:
            self.print_log("your driver exe path is {0}".format(self.driver_path))
            
        if cur_config['browser_name'] == "chrome":
            # settings for chrome
            chrome_options = Options()

            # Private browsing
            chrome_options.add_argument("--incognito")
            if cur_config['is_maximized']:
                chrome_options.add_argument("start-maximized")

            # for automation
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])            
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # javascript or image loaded option
            if not cur_config['js_loaded']:
                chrome_options.add_experimental_option( "prefs", {'profile.managed_default_content_settings.javascript': 2})
            if not cur_config['img_loaded']:
                chrome_options.add_experimental_option( "prefs", {"profile.managed_default_content_settings.images": 2})

            # To use my default extension
            # user_data_path = "C:\\Users\\" + getlogin() + "\\AppData\\Local\\Google\\Chrome\\User Data"
            # user_data_setting = "user-data-dir=" + user_data_path
            # chrome_options.add_argument(user_data_setting)

            if cur_config['used_proxy']:
                self.print_log("current proxy ip is : " + cur_config['cur_proxy'])
                chrome_options.add_argument('--proxy-server=' + cur_config['cur_proxy'])
            else:
                self.print_log("Now opening Google Chrome with no proxy...")
            
            driver = wd.Chrome(executable_path = self.driver_path, options=chrome_options)            
            
        elif cur_config['browser_name'] == "firefox":
            # create firefox options
            options = firefoxOptions()
            firefox_profile = wd.FirefoxProfile()

            if not cur_config['js_loaded']:
                options.preferences.update({'javascript.enabled': False})
            if not cur_config['img_loaded']:
                firefox_profile.set_preference('permissions.default.image', 2)
                firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

            if cur_config['used_proxy']:
                self.print_log("current proxy ip is : " + cur_config['cur_proxy'])
                # set proxy
                firefox_capabilities = wd.DesiredCapabilities.FIREFOX
                firefox_capabilities['marionette'] = True
                firefox_capabilities['proxy'] = {
                    'proxyType': "MANUAL",
                    'httpProxy': cur_config['cur_proxy'],
                    'ftpProxy': cur_config['cur_proxy'],
                    'sslProxy': cur_config['cur_proxy']        
                }
                self.print_log("Now opening Firefox browser...")
                driver = wd.Firefox(executable_path = self.driver_path, capabilities = firefox_capabilities, options=options, firefox_profile=firefox_profile)
            else:
                self.print_log("Now opening Firefox browser with no proxy...")
                driver = wd.Firefox(executable_path=self.driver_path, options=options, firefox_profile=firefox_profile)

            if cur_config['is_maximized']:
                driver.maximize_window()
            
        else:
            self.print_log("Unrecognized Browser")
            return None

        if cur_config['window_pos'] != [0, 0]:
            driver.set_window_position(cur_config['window_pos'][0], cur_config['window_pos'][1])
        return driver

    # open url in broser, delay time is the limit time for the broswer will wait for responses
    def open_url(self, cur_url, delay_time = 60):
        if self.driver:
            self.driver.set_page_load_timeout(delay_time)
            try:
                self.driver.get(cur_url)                
            except TimeoutException:
                self.print_log("Too much time taken to open {0}".format(cur_url))                
                return False
            except Exception as e:
                self.print_log("Error Occured")
                print(e)
                self.print_log("Something went wrong. Please check the error!")
                return False
            self.print_log("Successfully opened the url : {0}".format(cur_url))
            return True
        else:
            self.print_log("driver not created yet!")
            return False

    def print_log(self, print_str):
        print("{0} says : {1}".format(self.options._config['driver_name'], print_str))

    def wait_tag(self, wait_time, by_string, limit_count = 1, clickable = False, by_type = "css"):
        if not hasattr(self, 'driver'):
            return None
        times = 0
        while True:
            if times < limit_count:
                times = times + 1
            else:
                return None
            try:
                print("waiting tag : {0}...".format(by_string))         
                if clickable:
                    if by_type == "css":
                        return_tag = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, by_string)))
                    else:
                        return_tag = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, by_string)))
                else:
                    if by_type == "css":
                        return_tag = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, by_string)))
                    else:
                        return_tag = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, by_string)))
                print("found the tag...")
                return return_tag
            except TimeoutException:
                continue
            except:
                continue

    def find_tag(self, tag_str, wait_time = 0.5, limit_count = 1):
        if not hasattr(self, 'driver'):
            return None
        limit_counts = 0
        while True:
            if limit_counts < limit_count:
                limit_counts = limit_counts + 1
            else:
                print("Could not find the tag")
                return None
            if wait_time > 0.2:
                wait_between(wait_time - 0.2, wait_time + 0.2)
            print("waiting tag {0}...".format(tag_str))
            try:
                cur_tag = self.driver.find_element_by_css_selector(tag_str)        
                return cur_tag
            except:
                continue

    # mouse click the dom element localized by selenium
    def click_element(self, cur_element):
        browser_navigation_panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')    
        cur_x = cur_element.location['x']
        cur_y = cur_element.location['y'] + browser_navigation_panel_height
        cur_size = cur_element.size    
        center_x = cur_x + int(cur_size['width'] / 2)
        center_y = cur_y + int(cur_size['height'] / 2)
        
        offset_x = int(cur_size['width']/3)
        offset_y = int(cur_size['height']/3)
        
        pyautogui.click(center_x + randrange(-offset_x, offset_x), center_y + randrange(-offset_y, offset_y))
        print("clicked the element")
        wait_between(0.5, 1)

    # type something in input dom tag 
    def type_content(self, cur_content, start_delay = 0.03, end_delay = 0.05):
        keyboard = Controller()
        for char in cur_content:
            keyboard.press(char)
            keyboard.release(char)
            wait_between(start_delay, end_delay)
        wait_between(0.5, 1)

    # get web element rect
    def get_element_rect(self, cur_element):
        browser_navigation_panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')    
        cur_x = cur_element.location['x']
        cur_y = cur_element.location['y'] + browser_navigation_panel_height
        cur_size = cur_element.size
        return [cur_x, cur_y, cur_size['width'], cur_size['height']]

    # mouse move to the element
    def move_to_element(self, element):
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()

    # select select box
    def select_some_option(self, select_str, option_str):
        
        select_item = self.find_tag(self.driver, select_str, 0.6)
        select_item.click()
        print("select box {0} clicked".format(select_str))

        wait_between(0.5, 0.7)
        option_item = select_item.find_element_by_css_selector(option_str)
        option_item.click()
        print("option {0} clicked".format(option_str))

    # scroll down to element
    def scroll_down_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView", element)
        wait_between(0.8, 1)

    # wait for element to be enabled
    def wait_until_enabled(self, element, wait_time = 1.0):
        while True:
            wait_between(wait_time - 0.2, wait_time + 0.2)
            if element.is_enabled():
                break
        return

    def close_driver(self):
        # now close driver
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.print_log('quit the driver')

    def __del__(self):        
        self.print_log("Now closing, bye... ^0^")

    