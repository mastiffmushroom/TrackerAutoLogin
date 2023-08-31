import os
import urllib.request
import json
import numpy as np
import shutil

# Basic JSON validation of the files. 
# TODO: Actually validate this against a schema.
def read_valid_json_file(filename, permission):
    try:
        with open(filename, permission) as f:
            try:
                json_file = json.load(f)
            except ValueError as e:
                # Invalid JSON found in the file. Throw an error
                print("Invalid JSON structure found in " + filename + ". Exiting the app.")
                exit()

            return json_file
    except IOError:
        print("Your " + filename + " file is missing. Exiting the app.")
        exit()

tracker_file = os.path.join(os.getcwd(), "config/tracker_config.json")
tracker_file_temp = os.path.join(os.getcwd(), "config/temp_tracker_config.json")

tconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/tracker_config.json"

if os.path.isfile(tracker_file) == False:
    urllib.request.urlretrieve(tconfig_url, tracker_file)
else:
    urllib.request.urlretrieve(tconfig_url, tracker_file_temp)
    
    u_dict = read_valid_json_file(tracker_file, 'r')
    t_dict = read_valid_json_file(tracker_file_temp, 'r')
        
    for key in t_dict.keys():
       u_dict[key] = t_dict[key]
    
    # tracker_file has already been validated, shouldn't be a need to do it again
    with open(tracker_file, 'w') as f:
       json.dump(u_dict, f, indent=4, sort_keys=True)

# Remove the temp tracker file if it still exists
if os.path.isfile(tracker_file_temp) == True:
    os.remove(tracker_file_temp)

# Check if the user_config.json file exists, if not create the initial version with no trackers
user_file = os.path.join(os.getcwd(), "config/user_config.json")
if os.path.isfile(user_file) == False:
    user_file_default = os.path.join(os.getcwd(), "user_config_default.json")
    shutil.copyfile(user_file_default, user_file)

# Check if the user_config_sample.json file exists, if not download it
user_file_sample = os.path.join(os.getcwd(), "config/user_config_sample.json")
uconfig_url = "https://raw.githubusercontent.com/mastiffmushroom/TrackerAutoLogin/main/config/user_config_sample.json"

if os.path.isfile(user_file_sample) == False:
    urllib.request.urlretrieve(uconfig_url, user_file_sample)
