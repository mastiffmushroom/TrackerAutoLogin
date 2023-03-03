import os
import logging
import json

dir_ = os.path.join(os.getcwd(), "config/logs/")
if os.path.isdir(dir_) == False:
    os.makedirs(dir_)

log_filename = os.path.join(dir_, "trackerautologin.log")

with open(os.path.join(os.getcwd(), "config/user_config.json"), 'r') as f:
    user_config = json.load(f)
    
assert(user_config["LogLevel"].lower() in ["debug", "error", "warning"]),"LogLevel must be ['debug', 'warning', 'error']"

if user_config["LogLevel"].lower() == "debug":                                
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)
elif user_config["LogLevel"].lower() == "warning":
    logging.basicConfig(filename=log_filename, level=logging.WARNING)
else:
    logging.basicConfig(filename=log_filename, level=logging.ERROR)
