from flask_login import current_user
from flask import Flask, Response
from flask_login import LoginManager, UserMixin, login_required
from flask import Response, request
from app.user import get_login_form_html
from os.path import join as path_join
from configs.config import parameter
from flask import send_from_directory, url_for
from os.path import join as path_join
from app.staff_only_login import LoginProcess, User
from app.home_page import get_app, get_sudo_app
from app.util.interesting_app import InterestingClass
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

app = Flask(__name__)

DEFAULT_SESSION_DURATION = 12 #minutes

login_process_obj = LoginProcess()

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.session_protection = "strong"

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    TESTING=False,
    LOGIN_DISABLED=False
)



@app.route("/", methods=['GET', 'POST'])
def index():
    # try:
    password = request.form.get("password")
    username = request.form.get("username")
    print(username, password)
    if (username is None) or (password is None):
        return Response(get_login_form_html())
    else:
        return login_process_obj.login(username, password)


@login_manager.user_loader
def load_user(id):
     if login_process_obj.username_check(id):
        return User(id)
     else:
         return None

@app.route('/home/', methods=['GET', 'POST'])
@login_required
def fk():
    print("try enter stuff room")
    print("exactly ", current_user.name)
    return interesting_d_app.index()
#
# @app.route('/create_protocols/', methods=['GET', 'POST'])
# @login_required
# def fchief():
#     print(current_user.name)
#     return interesting_d_app.index()

@app.route('/favicon.ico')
@login_required
def favicon():
    print(current_user.name)
    return send_from_directory(path_join(parameter["assets_dir"]), "favicon.ico", mimetype="image")

extra_files_lst = []

asset_dir = parameter["assets_dir"]
dummy_text = "СТОРІНКА ЗНАХОДИТСЯ НА СТАДІЇ РОЗРОБКИ"
many_thanks_text = "ДЯКУЄМО ЩО СКОРИСТАЛИСЯ СЕРВІСОМ!"

# app_home = get_app(app, "/home/")
interesting_d_obj = InterestingClass("/", """СТОРІНКА ДЛЯ ПОДАННЯ ЗАЯВОК
                                                            ТА СТВОРЕННЯ ПРОТОКОЛІВ ЗМАГАНЬ""",
                                     DEFAULT_SESSION_DURATION, fig_ext="jpg")
interesting_d_app = interesting_d_obj.get_app(app, "/home/")

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=DEFAULT_SESSION_DURATION)  # expire after DEFAULT_SESSION_DURATION min
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=DEFAULT_SESSION_DURATION)
app.config["SESSION_PERMANENT"] = False

if __name__ == '__main__':
    app.run(port=5550, debug=True)#, extra_files=extra_files_lst)
