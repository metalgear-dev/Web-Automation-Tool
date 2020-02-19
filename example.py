# this is the example python file for using selenium driver
from selenium_driver import selenium_driver



def main():
    # this option should be like the variable 'conf' in selenium_option.py file
    # but you need to define some of them if you want them to be changed
    my_options = {
        'driver_name' : "MyExampleDriver"         # your driver name       
    }

    # create and open browser
    my_driver = selenium_driver(my_options)

    # now open the url
    if not my_driver.open_url('google.com'):
        my_driver.close_driver()
        exit()
    else:
        # to do your code
        my_driver.wait_tag(30, "", 2)


if __name__ == "__main__":
    main()