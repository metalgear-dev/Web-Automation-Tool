conf = {
    'driver_name' : "MyDriver",         # your driver name
    'used_proxy': False,                # use proxy or not
    'is_maximized': True,               # whether window is maximized or not
    'js_loaded': True,                  # whether javascript is loaded or not
    'img_loaded': True,                 # whether image is loaded or not
    'browser_name': 'chrome',           # chrome or firefox
    'cur_proxy' : '',                   # eg. 173.192.170.97:5329
    'window_pos' : [0, 0],              # browser window position
    'folder_path' : ""                  # absolute folder path of selenium driver execution file
}

class selenium_option(object):
    def __init__(self, initial_conf={}):
        self._config = conf # set it to conf
        if initial_conf != dict():
            for key in initial_conf:
                if key in self._config.keys():
                    self._config[key] = initial_conf[key]

    def get_property(self, property_name):
        if property_name not in self._config.keys(): # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]
