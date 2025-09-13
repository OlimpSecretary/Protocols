import json
import os
from datetime import datetime

cwd = os.path.dirname(__file__)


with open(os.path.join(cwd ,"config.json")) as f:
    parameter = json.load(f)

#
# with open(os.path.join(cwd ,"config_users.json")) as f:
#     user_parameter = json.load(f)
# the application version will be replace during release via GIT
application_version = str(datetime.today())

# load users from config file