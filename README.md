# custom-selenium-tool

### Summary
This project is for automating using selenium.
The selenium_driver class is made in this project, you can use it to automate browsing process easily including waiting for tags, scrolling, clicking elements, typing content in input tags, select the option in selector, and so on.
You can use google or firefox browser, according the option you can give ahead.
Using the option, you can disable javascript or image loading, change browser position, use proxy ips when it's opened.

### Anaconda Environment Setup
First you need to download or git clone this project.
I use [Anaconda](https://www.anaconda.com/distribution/) because it comes with many Python
packages already installed and it is easy to work with. After installing Anaconda,
you should create a [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

Open the terminal at your project folder
Type the following command:

    conda env create -f environment.yml --prefix <Your Environment Folder Path>

Note: The anaconda environment file is in github repository

After creating conda environment, activate it using the following command:

    conda activate <Your Enviroment Folder Path>

### How To Run The Sample Code
And execute the following command:

    python example.py

This file opens the google chrome and search for the keyword 'selenium'

Note: chromedriver.exe file is needed when using selenium and it's version must be the same as your google browser

For example
If your browser version is 80, then copy the 'chromedriver80.exe' file in the 'drivers' folder and paste it into 'chrome' folder.
Or you can specify the absolute path when creating option file like the following way:

    ... 
    my_options = {
        'driver_name' : 'MyExampleDriver',         # your driver name
        'browser_name' : 'chrome',
        'folder_path' : 'D:\chrome_driver\chromedriver.exe'
    }

    my_driver = selenium_driver(my_options)
    ...

The attributes in the option you can set is defined in selenium_option.py

Enjoy it, thanks.
