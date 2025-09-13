# import os
# import flask
# from flask import Response, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json
from configs import config
from flask import Response, request
import flask
from datetime import datetime
from configs.config import parameter


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.password = "secret"
        self.permission = self._get_user_permission()
        self.user_class = self._get_user_class()
        # print("User(UserMixin): created user: " + self.name)

    def _get_user_permission(self):
        try:
            cfg_file = config.parameter["user-json-file"]
            with open(cfg_file) as f:
                user_json = json.load(f)
            permission = "user"
            if "users_permissions" in user_json:
                if self.name in user_json["users_permissions"]:
                    permission = user_json["users_permissions"][self.name]
            print("users permission:", permission)
            return permission
        except FileNotFoundError as ex:
            print(f"{ex}. Failed to get user permission field from user-json-file (verify json)")
            return "user"
        except KeyError as ex:
            print(f"{ex}. Failed to get user permission field from user-json-file (verify json)")
            return "user"

    def _get_user_class(self):
        try:
            cfg_file = config.parameter["user-json-file"]
            with open(cfg_file) as f:
                user_json = json.load(f)
            user_class = "guest"
            if "users_permissions" in user_json:
                if self.name in user_json["users_classes"]:
                    user_class = user_json["users_classes"][self.name]
            print("users class:", user_class)
            return user_class
        except FileNotFoundError as ex:
            print(f"{ex}. Failed to get user class field from user-json-file (verify json)")
            return "user"
        except KeyError as ex:
            print(f"{ex}. Failed to get user class field from user-json-file (verify json)")
            return "user"

    def __repr__(self):
        # return "%d/%s/%s" % (self.id, self.name, self.password)

        # print("User(UserMixin): returning user: " + str(self.name))

        return "%s" % (self.name)

class LoginProcess:
    def __init__(self):
        self.user = None

    @staticmethod
    def username_check(username):
        cfg_file = config.parameter["user-json-file"]

        with open(cfg_file) as f:
            user_json = json.load(f)

        print("updating login dictionaries")
        users_local = user_json["users"]
        print("check user name: ", str(username).strip())
        name_check = str(username).lower().strip() in users_local
        return name_check

    def login_check(self, username, password):
        login_check = False
        cfg_file = config.parameter["user-json-file"]

        with open(cfg_file) as f:
            user_json = json.load(f)

        print("updating login dictionaries")
        users_local = user_json["users"]

        print("user trying to log in: ", str(username).strip())

        if len(str(username).strip()) < 4:
            print("login() user name too short:  '" + str(username).strip() + "'")
            print("login failed !")
            return flask.redirect("/")

        if len(str(password).strip()) < 4:
            print("login() password too short. Length was: " + str(len(str(password).strip())))
            print("login failed !")
            return flask.redirect("/")

        if str(username).lower().strip() in users_local:

            cfg_pwd = users_local[str(username).lower().strip()]

            if cfg_pwd == str(password).strip():
                login_check = True
                print("login_check user via config'" + username + "'")
                print("login_check via config = " + str(login_check))

            if ((datetime.strptime(parameter["deadline"], "%Y-%m-%d")<=datetime.now())
                    and (user_json["users_classes"][username] != 'admin')):
                print("deadline reached")
                login_check = False

        return login_check

    def login(self, username, password):

        login_check = self.login_check(username, password)

        if login_check:
            print("log in successfull for: ", str(username).strip())
            self.user = User(str(username))
            login_user(self.user)
            print("login successful")
            tst = str(request.args.get("next"))
            user_class = self.user._get_user_class()
            if len(tst) > 0:
                if tst != "None":
                    return flask.redirect(request.args.get("next"))
                else:
                    return flask.redirect(f"/home/")#flask.redirect(f"/stuff_room_{user_class}/")
            else:
                return flask.redirect(f"/home/")#flask.redirect(f"/stuff_room_{user_class}/")
        else:
            print("log in failed for: ", str(username).strip())
            print("user used the user '" + username + "'")
            print("login failed !")
            return flask.redirect("/")#flask.redirect(f"/home/")
