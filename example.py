# this is the example python file for using selenium driver
from selenium_driver import selenium_driver, wait_between
from selenium_driver import Keys

def main():
    # this option should be like the variable 'conf' in selenium_option.py file
    # but you need to define some of them if you want them to be changed
    my_options = {
        'driver_name' : 'MyExampleDriver',         # your driver name
        'browser_name' : 'chrome'
    }

    # create and open browser
    my_driver = selenium_driver(my_options)

    # now open the url
    if not my_driver.open_url('https://www.google.com'):
        my_driver.close_driver()
        exit()
    else:
        # remove the following code and to do your code
        input_tag = my_driver.wait_tag(30, "input[name='q']", 2)
        if input_tag:
            input_tag.send_keys('selenium')
            wait_between(0.5, 0.8)
            input_tag.send_keys(Keys.ENTER)
            wait_between(3,5)




if __name__ == "__main__":
    main()