import os
import urllib.request
import json
import numpy as np

tracker_file = os.path.join(os.getcwd(), "config/tracker_config.json")
tracker_file_temp = os.path.join(os.getcwd(), "config/temp_tracker_config.json")

user_file = os.path.join(os.getcwd(), "config/user_config.json")
user_file_temp = os.path.join(os.getcwd(), "config/temp_user_config.json")

tconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/tracker_config.json"
uconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/user_config_sample.json"
    
if os.path.isfile(tracker_file) == False:
    urllib.request.urlretrieve(tconfig_url, tracker_file)
else:
    urllib.request.urlretrieve(tconfig_url, tracker_file_temp)
    
    with open(tracker_file, 'r') as f:
        u_dict = json.load(f)
        
    with open(tracker_file_temp, 'r') as f:
        t_dict = json.load(f)
        
    for key in t_dict.keys():
        u_dict[key] = t_dict[key]
        
    with open(tracker_file, 'w') as f:
        json.dump(u_dict, f, indent=4, sort_keys=True)

if os.path.isfile(user_file) == False:
    urllib.request.urlretrieve(uconfig_url, user_file)
else:
    urllib.request.urlretrieve(uconfig_url, user_file_temp)
    
    with open(user_file, 'r') as f:
        u_dict = json.load(f)
        
    with open(user_file_temp, 'r') as f:
        t_dict = json.load(f)
        
    for key in t_dict.keys():
        if key not in u_dict.keys():
            u_dict[key] = t_dict[key]
            
    with open(tracker_file, 'r') as f:
        trackers = list(json.load(f).keys())
        
    ut_dict = {}    
            
    for key in t_dict.keys():
        if key not in trackers:
            if key in u_dict.keys():
                ut_dict[key] = u_dict[key]
            else:
                ut_dict[key] = t_dict[key]
            
    for track in trackers:
        if track in u_dict.keys():
            ut_dict[track] = u_dict[track]
            
    with open(user_file, 'w') as f:
        json.dump(ut_dict, f, indent=4)
