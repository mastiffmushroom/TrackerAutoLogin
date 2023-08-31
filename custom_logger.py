import os
import logging
import json
import sys
from init_configs import read_valid_json_file

dir_ = os.path.join(os.getcwd(), "config/logs/")
if os.path.isdir(dir_) == False:
    os.makedirs(dir_)

log_filename = os.path.join(dir_, "trackerautologin.log")

user_config = read_valid_json_file(os.path.join(os.getcwd(), "config/user_config.json"), 'r')

assert(user_config["LogLevel"].lower() in ["debug", "error", "warning"]),"LogLevel must be ['debug', 'warning', 'error']"

assert(user_config["LogType"].lower() in ["file", "stderr"]),"'LogType' must be ['file', 'stderr']"

if user_config["LogType"].lower() != "file":

    if user_config["LogLevel"].lower() == "debug":
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    elif user_config["LogLevel"].lower() == "warning":
        logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    else:
        logging.basicConfig(logging=logging.ERROR, stream=sys.stdout)

else:
    if user_config["LogLevel"].lower() == "debug":                                
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)
    elif user_config["LogLevel"].lower() == "warning":
        logging.basicConfig(filename=log_filename, level=logging.WARNING)
    else:
        logging.basicConfig(filename=log_filename, level=logging.ERROR)
