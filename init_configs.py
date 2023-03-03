import os
import urllib.request

tracker_file = os.path.join(os.getcwd(), "config/tracker_config.json")
user_file = os.path.join(os.getcwd(), "config/user_config.json")
tconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/tracker_config.json"
uconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/user_config_sample.json"
    
if os.path.isfile(tracker_file) == False:
    urllib.request.urlretrieve(tconfig_url, tracker_file)

if os.path.isfile(user_file) == False:
    urllib.request.urlretrieve(uconfig_url, user_file)
