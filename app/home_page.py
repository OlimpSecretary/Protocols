import json

import dash_html_components as html
from dash import Dash, Output, Input, dcc
from app.navigations import get_navigation
import time
from configs import config
# import dash_dangerously_set_inner_html
from app import base
# import flask_login
import flask
# import dash
# def get_base_template(server, body, title, user_name):
from flask_login import LoginManager
from configs.config import parameter
from os.path import join as path_join
from os.path import exists as path_exists
import base64
# from config.config import user_parameter
# from cached_property import cached_property
import requests
from glob import glob
import pandas as pd

def get_layout():
    background_ = []
    assets_dir_path = parameter["assets_dir"]
    image_filename = path_join(assets_dir_path, f"home_background.jpg")
    if path_exists(image_filename):
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        img_child = html.Img(src=f'data:image/jpj;base64,{encoded_image.decode()}', className=f"img",
                             id=f"img_id")
        background_.append(img_child)
    return html.Div(children=[
        html.Link(href='/assets/my.css' + "?t=" + str(time.time()), rel='stylesheet'),
        base.get_header("ДИТЯЧО-ЮНАЦЬКИЙ СПОРТИВНИЙ КЛУБ \"ОЛІМП\""),
        html.Div(children=get_navigation(), className="float-clear"),
        html.Div(id='output-container',
                 className="home-text",
                 children=[html.H1("""РАДО ПРОВЕДЕМ ВАС У СВІТ СПОРТУ!""")])
        ,html.Div(children=[html.Div(children=[html.Div(children=[dcc.Input(id="input_id"),
    html.Button("Submit", id="submit_id")]),
                              html.Div(children=[],id="output_id")])])
        , html.Div(children=background_)
        ,html.Div(style=parameter["footer_style"],
                 children=[" дзвоніть нам: " + str(parameter["main_mobile_phone_number"])
                     , " пішіть у Viber:" + str(parameter["viber_phone_number"])
                     , " пішіть на електронну пошту:" + str(parameter["club_email"])])
    ])


def get_sudo_layout():
    background_ = []
    assets_dir_path = parameter["assets_dir"]
    image_filename = path_join(assets_dir_path, f"keys.png")
    if path_exists(image_filename):
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        img_child = html.Img(src=f'data:image/jpj;base64,{encoded_image.decode()}', className=f"img",
                             id=f"img_id")
        background_.append(img_child)
    return html.Div(children=[
        html.Link(href='/assets/my.css' + "?t=" + str(time.time()), rel='stylesheet'),
        base.get_header("ДИТЯЧО-ЮНАЦЬКИЙ СПОРТИВНИЙ КЛУБ \"ОЛІМП\""),
        html.Div(children=get_sudo_navigation(), className="float-clear"),
        html.Div(id='output-container',
                 className="home-text",
                 children=[html.H2("""ВИ ЗНАХОДИТЕСЬ У ТРЕНЕРСЬКІЙ. У ВАС Є МОЖЛИВІСТЬ РЕДАГУВАТИ ДЕЯКІ СТОРІНКИ САЙТУ""")
                           ,html.H3("""ДОТРИМУЙТЕСЬ НАСТУПНИХ ПРАВИЛ:""")
                           ,html.H3("""1.ВЕСЬ ТЕКСТ МАЄ БУТИ НАПИСАНИЙ ТІЛЬКИ УКРАЇНСЬКОЮ МОВОЮ!""")
                             , html.A(children="ПЕРЕВІРКУ ПРАВОПИСУ РАДИМО ЗДІЙСНЮВАТИ ЗА ДОПОМОГОЮ ЦЬОГО ПОСИЛАННЯ"
                                      ,href="https://ukr-mova.in.ua/perevirka-tekstu")
                           ,html.H3("""2.ІНФОРМАЦІЯ МАЄ БУТИ РОЗРАХОВАНА НА ШИРОКИЙ ЗАГАЛ (КОРОТКО, ЗРОЗУМІЛО, ПОЛІТКОРЕКТНО).""")
                           ,html.H3("""3.РОЗМІР МАЛЮНКІВ (ФОТО) НЕ МАЄ ПЕРЕВИЩУВАТИ 300 KБ!""")
                           ,html.H3("""3.РАДИМО РЕДАГУВАТИ ЛИШЕ ПО 1 СТОРІНЦІ ЗА РАЗ.""")
                           ,html.H3("""4.У РАЗІ НЕПЕРЕДБАЧУВАНОГО РОЗВИТКУ ПОДІЙ ЗВЕРНІТЬСЯ ДО АДМІНІСТРАЦІЇ САЙТУ.""")])
        , html.Div(children=background_)
        ,html.Div(style=parameter["footer_style"],
                 children=[" дзвоніть нам: " + str(parameter["main_mobile_phone_number"])
                     , " пішіть у Viber:" + str(parameter["viber_phone_number"])
                     , " пішіть на електронну пошту:" + str(parameter["club_email"])])
    ])


def get_promts():
    basic_info = f"""
    Адреса спортивного клубу "Олімп": {parameter["club_address"]},
    Елктронна пошта: {parameter["club_email"]}
    Телефони: {parameter["main_mobile_phone_number"]},
    {parameter["viber_phone_number"]} (Viber)
    """
    file_ = path_join(parameter["assets_dir"], f"about_politics", "body1.txt")
    with open(file_) as fl:
        txt = fl.read()

        basic_info += f"""Поліика клубу "Олімп":
    {txt}    
    """
    promts_lst = []
    for key in parameter["sport_types_inv"]:
        sport = parameter["sport_types_inv"][key]
        dir = path_join(parameter["assets_dir"], f"about_instructors_{key}")
        txt = f"####### {sport} #######"
        if path_exists(dir):
            for idx, coach_key in enumerate(parameter[key]):
                file_ = path_join(dir, f"body{idx+1}.txt")
                txt += f"\n *** тренер  {parameter[key][coach_key]} ***\n"
                if path_exists(file_):
                    with open(file_, "r") as fl:
                        txt += fl.read()
                        # promts_lst.append(txt)
                schedule_file = path_join(parameter["data_dir"],
                                           f"schedule_{key}_{idx}.csv")
                if path_exists(schedule_file):
                    df = pd.read_csv(schedule_file)
                    txt += f"\n Розклад занять з {sport}:\n" + df.to_string().replace("--", " - ")
        promts_lst.append(txt)

    info = basic_info+"\n\n".join(promts_lst)
    role_dic = {"role": "system",
        "content": f"""
        Ви досвідчений та ввічливий адміністратор спортивного клубу "Олімп",
         що допомагає клієнтам або їхнім дітям обрати вид спорту в нашому клубі. 
          Наразі для дорослих активно працює Йога,
           а для дітей - карате і художня гімнастика (для дівчаток). Якщо клієнт цікавиться іншими видами спорту ви маєте запропонувати,
            найбільш близький з перечислиних вище. Ви маєте навтупну інформацію про спортивний клуб:
            
            {info} 
        """
                }
    with open("Promt.txt", "w") as fl:
        fl.write(json.dumps(role_dic))



def get_app(server, url_path):

    assets_folder = config.parameter["assets_dir"]
    app = Dash(name='home', url_base_pathname=url_path, server=server, assets_folder=assets_folder)

    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    app.layout = get_layout()

    app.config['suppress_callback_exceptions'] = True

    @app.callback(Output(f"output_id", 'children'),
                  [Input(f"submit_id", "n_clicks"),
                   Input(f"input_id", "value")], prevent_initial_call=True)
    def submit(n_clicks, query):
        if n_clicks:
            # try:
            print(query)
            response = requests.post('https://digitalolimp.pythonanywhere.com/compute', json={'value': query})
            result = response.json().get('result')
            print(result)
            return f'Result from worker: {result}'

    return app


def get_sudo_app(server, url_path):

    assets_folder = config.parameter["assets_dir"]
    app = Dash(name='home', url_base_pathname=url_path, server=server, assets_folder=assets_folder)

    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    app.layout = get_sudo_layout()

    app.config['suppress_callback_exceptions'] = True

    return app


def update_output():
    return None


if __name__ == "__main__":
    s = get_promts()
    with open("Promt.txt") as fl:
        txt = fl.read()
        dic_ = json.loads(txt)
        print(dic_)
        print(type(dic_))
    # server = flask.Flask(__name__)
    #
    # server.secret_key = 'xxxxyyyyyzzzzz'
    #
    # login_manager = LoginManager()
    # login_manager.init_app(server)
    # login_manager.login_view = 'login'
    # app = get_app(server, "/home/")
    # app.run_server(debug=True)
    # # app = dash.Dash(__name__, server=server)

