import os.path
from calendar import month_name
from os.path import basename
import dash_daq as daq
import dash
from click import style
from dash import dash_table
from dash import callback_context
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import Dash, ALL
from flask_login import current_user
# from database import data_access
from app.dummy_page_pattern import Dummy
# from templates import navigation as nav
# import time
from dash.dcc import Markdown as dash_dangerously_set_inner_html
from configs import config
from urllib.parse import quote as urlquote
from configs.config import parameter
# import flask_login
# from additional import security as sec
from dash.dependencies import Input, Output, State
# import uuid
from flask import redirect
# from os import remove
# from os.path import join as path_join
import base64
# import pandas as pd
# import dash_table as dt
# from urllib import parse
from os.path import join as path_join, curdir, abspath
from os.path import exists as path_exists
from os.path import isfile, getsize
from os import mkdir, remove, listdir, utime
import shutil
from time import sleep
from dash.dependencies import ALL
from datetime import datetime, timedelta, time
import dash_bootstrap_components as dbc
# import re
import dash_daq
from app.util.mailer import MailSender
import secrets
import string
import json
from glob import glob
# from dash import CeleryManager
# import celery
from dash import DiskcacheManager
import diskcache
# from chardet import detect
from app.util.excel_writer import ExcelWriter
import zipfile
import dash_mantine_components as dmc

TOGGLE_LABEL_DICT= {False: "Учасники чекають на запрошення", True: "Запрошення розіслані!"}
LATTER_PATTERN ="""Шановний LEADER_COACH_NAME!
        Маю за честь запросити Вас і Вашу команду до участі у змаганнях "COMPETITION_TITLE".
        Дата проведення змагань COMPETITION_DATE
        Останній день подачі заявок DEADLINE 
        Для подання заявки скористайтеся сервісом на https://olimpsecretary.pythonanywhere.com/create_protocols/
        Для входу скористайтеся 
            логіном:
            
                LEADER_COACH_EMAIL
                  
            та паролем:
        
                LEADER_COACH_PASSWORD
        
        З повагою,
        Романець Тетяна Борисівна"""

MAIL_WARNING_MASSAGE ="КІЛЬКІСТЬ ІМЕН ТА ЕМЕЙЛІВ РІЗНА!!!"
MIN_DATE = (datetime.now()-timedelta(days=1)).date()
MAX_DATE = (datetime.now()+timedelta(days=300)).date()
DATE_END = (datetime.now()+timedelta(days=3)).date()
DATE_NOW = datetime.now().date()

OPT_CHIEFSECRETARY_LST = ["Романець Т.Б.", "Романець Тетяна Борисівна", "Романець Тетяна", "Тетяна Романець", "Т.Б. Романець"]
OPT_CHIEFJUDGE_LST = ["Світко О.В.", "Світко Олег Володимирович", "О.В. Світко", "Олег Володимирович Світко", "Олег Світко",
                      "Романець Т.Б.", "Романець Тетяна Борисівна", "Романець Тетяна", "Тетяна Романець", "Т.Б. Романець"]
OPT_COACHES_LST = ["Романець Т.Б.", "Шуляк В.О.", "Науменко", "Сельвестров"]
OPT_TEAMS_LST = ["Олімп", "Олімп-1", "Олімп-2", "Олімп-3", "Тайгер"]
OPT_GIRLS_NAME = ["Анна", "Софія", "Марія", "Катерина", "Соломія", "Поліна", "Вікторія", "Мілана", "Емілія", "Єва",
                  "Вероніка", "Аліса", "Анастасія", "Ангеліна", "Дарина", "Злата", "Стефанія", "Уляна", "Мирослава",
                  "Аліна", "Діана", "Єлизавета", "Лілія", "Надія", "Яна", "Марта", "Олександра", "Ольга", "Ірина",
                  "Юлія", "Оксана", "Віра", "Тетяна", "Людмила", "Світлана", "Наталія", "Даша", "Ульяна", "Ксенія", "Марічка",
                  "Калина", "Зоряна", "Інна", "Олена", "Валерія", "Варвара", "Марина", "Лариса", "Наталя", "Любов", "Маша"]

OPT_BOYS_NAME = ["Артем", "Максим", "Богдан", "Дмитро", "Михайло", "Андрій",
"Денис", "Данило", "Тимофій", "Макар", "Марк", "Олександр",
"Матвій", "Дамір", "Остап", "Тарас", "Мирон", "Гліб", "Назар",
"Ярослав", "Артемій", "Лев", "Адам", "Олівер", "Лука", "Раян",
"Олексій", "Іван", "Петро", "Оріон",
"Юрій", "Юрко", "Віктор", "Ілля", "Єгор", "Степан", "Ростислав",
"Володимир", "Сергій", "Павло", "Мирослав", "Святослав", "Радомир",
"Добриня", "Єлисей", "Зореслав", "Пантелеймон", "Святогор", "Еней",
"Аскольд", "Євген" , "Сиверин", "Василь", "Владислав", "Любомир", "Валерій"]



class InterestingClass:
    def __init__(self,  home_url, title, default_session_duration, fig_ext="png"):
        self.title = title
        self.url = None
        self.dummy = Dummy(home_url, "ВИХІД")
        self.assets_dir_path = parameter["assets_dir"]
        self.tmp_assets_dir_path = path_join(self.assets_dir_path, "tmp")
        self.fig_ext = fig_ext
        self.default_session_duration = default_session_duration

    @staticmethod
    def progress_input(progress_percent):
        return (f" {"|" * (progress_percent)}{progress_percent} % ")

    @staticmethod
    def split_opponents(df):

        # Sort for max and min streams
        df_max = df.sort_values(["count", "team-lead", "Учасник"], ascending=False).reset_index(drop=True)
        df_min = df.sort_values(["count", "team-lead", "Учасник"], ascending=True).reset_index(drop=True)
        n = df.shape[0] // 2
        df_interleaved = pd.concat([df_max.iloc[:n], df_min.iloc[:n]]).sort_index(kind="merge").reset_index(drop=True)
        if 2*n < df.shape[0]:
            df_interleaved = pd.concat([df_interleaved, df_max.iloc[n:n+1,:]]).reset_index(drop=True)
        if df_interleaved.duplicated().any():
            print(df_interleaved.iloc[:,:3])
        return df_interleaved

    @staticmethod
    def str_to_date(str_):
        return datetime.strptime(str_, "%Y-%m-%d").date()

    @staticmethod
    def date_to_str(date):
        return str(date)


    def compose_protocols_(self, full_dict):
        dict_ = {}
        for key in full_dict.keys():
            # if key == "Куміте Хлопці (категорія B,  10-11 років  30-59кг)":
            #     print("stop")
            df_ = pd.concat(full_dict[key])
            df = self.split_opponents(df_)
            dict_[key] = df
        return dict_

    @staticmethod
    def get_submission_dir(deadline, competition_date):
        path = os.path.join(parameter["submission_dir"], f"D{deadline}CD{competition_date}")
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def get_protocols_dir(deadline, competition_date):
        path = os.path.join(parameter["protocols_dir"], f"D{deadline}CD{competition_date}")
        if not os.path.exists(path):
            os.mkdir(path)
        return path


    @staticmethod
    def get_massage_on_submission(n_members, n_sections, n_only_one_section, competition_title):
        s = f"""Дякуємо, ваша заявка прийнята!
        В вашій команді {n_members} учасників,
         що боротимуться всього {n_sections} разів за першість 
         у змаганнях "{competition_title}". Кількість учасників,
          що змагатимуться лише в одному розділі {n_only_one_section}.
         Успішних змагань!"""
        if n_members == 1:
            s.replace("учасників", "учасник")
        if n_sections == 1:
            s.replace("разів", "раз")
        return s

    @staticmethod
    def get_bins(str_sequence):
        str_lst = str_sequence.split(",")
        max_number = int(str_lst[-1].replace("+", "").replace(" ", ""))
        bins = pd.IntervalIndex.from_tuples([tuple(int(it) for it in s.replace(" ", "").split("-"))
                                             for s in str_lst[:-1]] + [(max_number, 3*max_number)], closed="both")
        return bins, str_lst

    @staticmethod
    def modify_config_file(key, value):
        with open(parameter["config-path"], "r") as f:
            users_json = json.load(f)
            users_json[key] = value
            with open(parameter["config-path"], "w") as f_:
                json.dump(users_json, f_, indent=4)



    @staticmethod
    def process_and_write_credits(login, name, password):
        with open(parameter["user-json-file"], "r") as f:
            users_json = json.load(f)
            users_json["users"][login] = password
            users_json["users_names"][login] = name
            users_json["users_permissions"][login] = "user"
            users_json["users_classes"][login] = "user"
            with open(parameter["user-json-file"], "w") as f_:
                json.dump(users_json, f_, indent=4)

    @staticmethod
    def generate_secure_password(length=6):
        """Generates a cryptographically secure random password."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        return password

    @staticmethod
    def compose_mail(names, mails, competition_date, deadline, title, pattern, password, idx=0):
        latter_p = pattern
        participants_number = 0
        if (names is not None):
            names_ = names.split(",")
            participants_number = len(names_)
            name = names_[idx].rstrip().lstrip()
            for name_part_ in name.split():
                name_part = name_part_.rstrip().lstrip()
                if name_part in OPT_GIRLS_NAME:
                    latter_p = latter_p.replace("Шановний", "Шановна")
                    break
                elif name_part in OPT_BOYS_NAME:
                    break
                else:
                    latter_p = latter_p.replace("Шановний ", "Шановний(на) ")

            latter_p = latter_p.replace("LEADER_COACH_NAME", name)
        if (mails is not None):
            mails_ = mails.split(",")
            if participants_number != len(mails_):
                return MAIL_WARNING_MASSAGE
            mail = mails_[idx].rstrip().lstrip()
            latter_p = latter_p.replace("LEADER_COACH_EMAIL", mail)
        if (competition_date is not None):
            latter_p = latter_p.replace("COMPETITION_DATE", str(competition_date))
        if (deadline is not None):
            latter_p = latter_p.replace("DEADLINE", str(deadline))
        if (title is not None):
            latter_p = latter_p.replace("COMPETITION_TITLE", title)
        if (password is not None):
            latter_p = latter_p.replace("LEADER_COACH_PASSWORD", password)
        return latter_p

    @staticmethod
    def get_help(title, issue):
        help_ = [
                dbc.ModalHeader(dbc.ModalTitle(title)),
                dbc.ModalBody([html.Div(f"""{issue}
                 Скористайтесь формою нижче для створення заявки:""")

                 ,html.Div("""1. Введіть назву команди та ім'я тренера. В полі "Учасник" запишіть призвище та ім'я учаника;""")
                 ,html.Div("""2. При потребі, виправте гендерну приналежність;""")
                 ,html.Div("""3. Задайте вік та вагу (наступні поля - "Вік" та "Вага");""")
                 ,html.Div("""4. Виберіть розділи в яких прийме участь (список розділів нижче - натискайте на порожні квадрати);""")
                 ,html.Div("""5. Виберіть категорію учасника (останній вертикальний список);""")
                 ,html.Div("""6. Натисьніть "Додати до команди". Учаник має з'явитись в таблиці зправа;""")
                 ,html.Div("""7. Після того як додано всіх учасників (корректність перевірте в таблиці зправа) натисніть "Подати заявку".""")
                 ,html.Div("""Для регування параметрів учаника: виберіть його в таблиці зправа, натисніть "Редагувати",
                  виправте потрібні поля, натисніть "Додати до команди".""")
                 ,html.Div("""Для видалення учасника : виберіть його в таблиці зправа, натисніть "Видалити".
                 """)])
            ]
        return help_

    @staticmethod
    def get_sections_lists_(sex_, options, children_checklists):
        """options, sex_, children_checklists
        """
        if not options:
            return dash.no_update
        if sex_ in options:
            options.remove(sex_)
        sex = options[0]
        lists_ = []
        for id_idx, checklist in enumerate(children_checklists):
            if checklist["props"]["children"]:
                lists_ += [item for item in checklist["props"]["children"]["props"]["value"] if item.find(sex) == -1]
        return lists_

    def _copy_all_to_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_files_list():
            src_path = path_join(self.assets_dir_path, file)
            desc_path = path_join(self.tmp_assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _copy_all_from_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_tmp_files_list():
            src_path = path_join(self.tmp_assets_dir_path, file)
            if getsize(src_path) == 0:
                continue
            desc_path = path_join(self.assets_dir_path, file)
            shutil.copy(src_path, desc_path)

    def _delete_tmp(self):
        if path_exists(self.tmp_assets_dir_path):
            shutil.rmtree(self.tmp_assets_dir_path)

    def _empty_tmp(self):
        if not path_exists(self.tmp_assets_dir_path):
            mkdir(self.tmp_assets_dir_path)

        for file in self._get_tmp_files_list():
            target_path = path_join(self.tmp_assets_dir_path, file)
            remove(target_path)

    def _get_weightless_checklists(self, list_, label_=None):
        children_ = []
        if label_ is not None:
            children_.append(html.Div(label_))
        children_.append(dbc.Col(dcc.Checklist(
                list_,
                list_
                , persistence=True
                , style={"margin-left": "10%"}, id="Weightless-check")
                , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"))
        return children_

    def _get_checklists(self, lists_):
        children_ = []
        for idx, lst_ in enumerate(lists_):
            children_.append(dbc.Col(dcc.Checklist(
                lst_,
                lst_
                , style={"margin-left": "10%"}, id={"type": "Section-check", "index": idx})
                , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"))
        return children_


    def get_layout(self):

        container_children = []
        admin_container_children = []
        left_admin_container_children = []
        right_admin_container_children = []
        left_admin_container_children.append(dbc.Row([dbc.Col([dbc.Label("Назва змагань")], width='auto'), dbc.Col([ dcc.Textarea(
            id="CompetitionTitle",
            value=parameter["competition_title"],
            persistence=True,
            persistence_type="local",
            style={'width': '70%', 'height': 60, 'minWidth': '200px'} # Adjust height as needed
        )], width='auto'),], className="mb-3"))
        ############## ДАТА ЗМАГАНЬ ########################
        left_admin_container_children.append(
            dbc.Row([

                dbc.Col(
                    html.Div([
                        dbc.Label("Останній день подачі заявок"),
                        dcc.Input(
                    id='SubmissionDeadline',
                    type="date",
                    min=MIN_DATE,
                    max=MAX_DATE,
                    # min_date_allowed=MIN_DATE,
                    # max_date_allowed=MAX_DATE,
                    # initial_visible_month=MIN_DATE,
                    # minDate=
                    value=parameter["deadline"],
                    # persistence = True,
                    # persistence_type = 'local'
                    )
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    width='auto'
                ),

                dbc.Col(
                    html.Div([
                        dbc.Label("Дата змагань"),
                        dcc.Input(
                            id="CompetitionDate",
                            type="date",
                            min=MIN_DATE,
                            max=MAX_DATE,
                            value=parameter["competition_date"],
                            persistence = True,
                            persistence_type = 'local'
                        )
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    width='auto'
                )

            ], className="mb-3")
        )
        ############## КАТЕГОРІЇ ########################
        left_admin_container_children.append(
            dbc.Row([

                dbc.Col(
                    html.Div([
                        dbc.Label("Кількість категорій"),
                        dcc.Input(
                            id='CategoriesNumber',
                            value=4,
                            type='number',
                            min=1,
                            max=10,
                            style={'width': '42%', 'height': 30, 'minWidth': '40px'}
                        , persistence=True)
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    width='auto'
                ),

                dbc.Col(
                    html.Div([html.Div(hidden=True, id="CategoriesNamesHidden"),
                        dbc.Label("Назви категорій"),
                        dcc.Input(
                            id="CategoriesNames",
                            value=", ".join(parameter["categories_names_lst"]),
                            style={'width': '200px', 'height': 30, 'minWidth': '200px'}
                        # , persistence=True
                        )
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    width='auto'
                )

            ], className="mb-3")
        )

        ############## ВІКОВІ КАТЕГОРІЇ ########################
        left_admin_container_children.append(dbc.Row([dbc.Col([dbc.Label("Суміжний вік",
                                                             style={'display': 'inline-block',
                                                                    'margin-left': '5%', 'margin-right': '2%'}),
                                                    dcc.Input(
                                                        id='AgeCuts',
                                                        value=2,
                                                        type='number',
                                                        min=2,
                                                        max=4,
                                                        style={'width': '10%', 'height': 30, 'minWidth': '40px'}  # Adjust height as needed
                                                    , persistence=True),
                                                    dbc.Label("Мінімальний вік",
                                                             style={'display': 'inline-block',
                                                                    'margin-left': '5%',
                                                                    'margin-right': '2%'}),
                                                    dcc.Input(
                                                        id='MinAge',
                                                        value=6,
                                                        type='number',
                                                        min=4,
                                                        max=14,
                                                        style={'width': '10%', 'height': 30, 'minWidth': '40px'}
                                                        # Adjust height as needed
                                                    , persistence=True),

                                                    ],
                                           width = 4,
                                            style = {"display": "flex", "alignItems": "center"}),

                                                    dbc.Col([html.Div(hidden=True, id="CategoriesAgeHidden"),
                                                    dbc.Label("Вікові категорії", style={'display': 'inline-block',
                                                                                       'margin-left': '5%',
                                                                                       'margin-right': '2%'}),
                                                    dcc.Input(id="CategoriesAge", value=", ".join(parameter["categories_age_lst"]),
                                                              style={'width': '40%', 'height': 30, 'minWidth': '30px'}
                                                              # , persistence=True
                                                              )], width=5
                                                   , style={'display': 'flex', 'alignItems': 'center'})], className="mb-3"))
        ############## ВАГОВІ КАТЕГОРІЇ ########################
        ################ дівчата
        left_admin_container_children.append(dbc.Row([dbc.Col([dbc.Label("Кількість(дівчата)",
                                                             style={'display': 'inline-block',
                                                                    'margin-left': '5%', 'margin-right': '2%'}),
                                                    dcc.Input(
                                                        id='WeightNumberGirl',
                                                        value=4,
                                                        type='number',
                                                        min=1,
                                                        max=10,
                                                        style={'width': '16%', 'height': 30, 'minWidth': '40px'}  # Adjust height as needed
                                                        , persistence=True),
                                                    dbc.Label("Супер-тяж-вага(дівчата)",
                                                             style={'display': 'inline-block',
                                                                    'margin-left': '5%',
                                                                    'margin-right': '2%'}),
                                                    dcc.Input(
                                                        id='MaxWeightGirl',
                                                        value=60,
                                                        type='number',
                                                        min=30,
                                                        max=120,
                                                        style={'width': '11%', 'height': 30, 'minWidth': '40px'}
                                                        # Adjust height as needed
                                                        , persistence=True),

                                                    ],
                                                   width='auto',
                                                   style={"display": "flex", "alignItems": "center"}),

                                           dbc.Col([html.Div(hidden=True, id="CategoriesWeightHiddenGirl"),
                                               dbc.Label("Вагові категорії(дівчата)"),
                                               dcc.Input(id="CategoriesWeightGirl",
                                                         value=", ".join(parameter["categories_weight_lst"]),
                                                         style={'width': '40%', 'height': 30, 'minWidth': '200px'}
                                                         # , persistence=True
                                                         )], width='auto'
                                               , style={'display': 'flex', 'alignItems': 'center'})], className="mb-3"))
        ################ хлопці
        left_admin_container_children.append(dbc.Row([dbc.Col([dbc.Label("Кількість(хлопці)",
                                                                         style={'display': 'inline-block',
                                                                                'margin-left': '5%',
                                                                                'margin-right': '2%'}),
                                                               dcc.Input(
                                                                   id='WeightNumberBoy',
                                                                   value=4,
                                                                   type='number',
                                                                   min=1,
                                                                   max=10,
                                                                   style={'width': '16%', 'height': 30,
                                                                          'minWidth': '40px'}  # Adjust height as needed
                                                                   , persistence=True),
                                                               dbc.Label("Супер-тяж-вага(хлопці)",
                                                                         style={'display': 'inline-block',
                                                                                'margin-left': '5%',
                                                                                'margin-right': '2%'}),
                                                               dcc.Input(
                                                                   id='MaxWeightBoy',
                                                                   value=60,
                                                                   type='number',
                                                                   min=30,
                                                                   max=120,
                                                                   style={'width': '11%', 'height': 30,
                                                                          'minWidth': '40px'}
                                                                   # Adjust height as needed
                                                                   , persistence=True),

                                                               ],
                                                              width='auto',
                                                              style={"display": "flex", "alignItems": "center"}),

                                                      dbc.Col([html.Div(hidden=True, id="CategoriesWeightHiddenBoy"),
                                                               dbc.Label("Вагові категорії(хлопці)"),
                                                               dcc.Input(id="CategoriesWeightBoy",
                                                                         value=", ".join(
                                                                             parameter["categories_weight_lst"]),
                                                                         style={'width': '40%', 'height': 30,
                                                                                'minWidth': '200px'}
                                                                         # , persistence=True
                                                                         )], width='auto'
                                                              , style={'display': 'flex', 'alignItems': 'center'})],
                                                     className="mb-3"))

        left_admin_container_children.append(dbc.Row([dbc.Col([html.Div(hidden=True, id="SexCutsHidden"),
                                                               dbc.Label("Гендерні категорії"),
                                                    dcc.Input(
                                                        id='SexCuts',
                                                        value=", ".join(parameter["sex_cuts_lst"]),
                                                        style={'width': '40%', 'height': 30, 'minWidth': '180px'}  # Adjust height as needed
                                                        , persistence=True
                                                        , persistence_type='local'
                                                    ),
                                                    ],
                                                   width='auto',
                                                   style={"display": "flex", "alignItems": "center"}),
                                           dbc.Col([html.Div(hidden=True, id="SectionsHidden"),
                                               dbc.Label("Розділи", style={'display': 'inline-block',
                                                                                   'margin-left': '5%',
                                                                                   'margin-right': '2%'}),
                                               dcc.Input(id="Sections",
                                                         value=", ".join(parameter["sections_all_lst"]),
                                                         style={'width': '50%', 'height': 30, 'minWidth': '200px'}
                                                         , persistence=True)], width='auto'
                                               , style={'display': 'flex', 'alignItems': 'center'})], className="mb-3"))
##################### weightless ####################
        left_admin_container_children.append(
            dbc.Row([], id="WeightlessSections"))


######################################################
        left_admin_container_children.append(
dbc.Row([dbc.Col(dcc.Checklist(
    ['Ката Дівчата', 'Ката Хлопці', 'Ката Мікс'],
    ['Ката Дівчата', 'Ката Хлопці', 'Ката Мікс']
,style={"margin-left": "10%"}, id="Section-1-check")
    , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"),
dbc.Col([]
        , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3")], id="SectionLists"))

        left_admin_container_children.append(
            dbc.Row([dbc.Col([dbc.Label("Головний Суддя", style={'display': 'inline-block',
                                                                    'margin-left': '10%', 'margin-right': '2%'}),
                              dcc.Input(id="ChiefJudge", value="Романець Т.Б.",
                                        type="text", list="chiefjudge-options",
                                        style={'width': '50%', 'height': 30, 'minWidth': '200px'}),
            html.Datalist(id="chiefjudge-options", children=[
                html.Option(value=fruit) for fruit in OPT_CHIEFJUDGE_LST
            ])]
                                 , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"),
                     dbc.Col([dbc.Label("Головний Секретар", style={'display': 'inline-block',
                                                                    'margin-left': '10%', 'margin-right': '2%'}),
                              dcc.Input(id="ChiefSecretary", value="Романець Т.Б.",type="text",
                                        list="chiefsecretary-options",
                                        style={'width': '50%', 'height': 30, 'minWidth': '200px'}),
            html.Datalist(id="chiefsecretary-options", children=[
                html.Option(value=fruit) for fruit in OPT_CHIEFSECRETARY_LST
            ])]
                                 , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3")]))

        left_admin_container_children.append(html.Hr(style={'margin-top': '20px', 'margin-bottom': '20px', 'borderWidth': '1px', 'borderColor': 'gray',
                       'borderStyle': 'solid'}))
        admin_container_children = dbc.Row([dbc.Col(left_admin_container_children, width='auto', style={'alignItems': 'center'},
                                                    className="mb-3"), dbc.Col([dbc.Row(dbc.Label("ПІБ тренерів команд")),
                                                                                dbc.Row([dcc.Input(type="text",
                                                                                                   list="coachName-options",
                                                                                                   persistence=True,
                                                                                                   id="TeamLeadsNames",
                                                                                                   style={'width': '50%', 'height': 30, 'minWidth': '200px'}),
                                                                                         html.Datalist(id="coachName-options", children=[
                    html.Option(value=name) for name in OPT_COACHES_LST+OPT_GIRLS_NAME+OPT_BOYS_NAME
                ])]),
                                                                                     dbc.Row(dbc.Label("Введіть e-mail тренерів команд в тому ж порядку")),
                                                                                dbc.Row(dcc.Input(type="text", persistence=True, id="TeamLeadsEmails",
                                                                                                  style={'width': '50%', 'height': 30, 'minWidth': '200px'})),
                                                                                dbc.Row(dbc.Label("Шаблон листа")),
                                                                                dbc.Row(dcc.Textarea(
        id="LatterPattern",
        value=LATTER_PATTERN,
        style={'width': '100%', 'height': 350, 'display': 'flex','minWidth': '200px'},
        persistence=True
    ),),  dbc.Row(dcc.Textarea(
        id="LatterExample",
        value=LATTER_PATTERN,
        style={'width': '100%', 'height': 350, 'display': 'none'},
        persistence=True,
        readOnly=True,
            ),),
            dbc.Row(dcc.RadioItems(['Шаблон', 'Зразок'], 'Шаблон', inline=True, id="PatternOrExample",
                                   style={'display': 'inline-block','margin-left': '5px', 'margin-right': '5px',
                                          'margin-bottom': '15px', 'margin-top': '5px'},
                                   labelStyle={'margin-left': '1px', 'margin-right': '5px'})
            ), dbc.Row(html.Button("Розіслати запрошення", id="SendInvitations")),
    dbc.Row(daq.ToggleSwitch(
        id="InvitationsSent",
        label=TOGGLE_LABEL_DICT[False],
        labelPosition='bottom',
        value=False,
        style={"margin-top":"20px"}
    ))
                                                                                ], width='auto', style={'alignItems': 'center'}, className="mb-3")])

        container_children.append(html.Div(children=admin_container_children, id="admin_only_tools", hidden=True))
################################################################# КОМАНДИ #########################################################
        left_column_container = []
        container_children.append(dash_daq.LEDDisplay(
            id="CountDownDisplay",
            value="0:0",
            label={
                "label": "Прийом заявок буде обмежено через:",
                "style": {"font-size": "1rem", "text-align": "center"},
            },
            backgroundColor="blue",
            color="black",
            labelPosition="top",
            size=30,
            style={'margin-top': '20px', 'margin-bottom': '20px'}
        ))

        left_column_container.append(
            dbc.Row([dbc.Col([dbc.Label("Назва команди", style={'display': 'inline-block',
                                                                    'margin-left': '10%', 'margin-right': '2%'})
                                 , dcc.Input(id="Teams",
                                                         value="Олімп",
                                                         style={'width': '50%', 'height': 30, 'minWidth': '200px'},
                                                                   type="text"
                                                                   , list="teams-options"
                                                         , persistence=True), html.Datalist(id="teams-options", children=[
                html.Option(value=fruit) for fruit in OPT_TEAMS_LST
            ])], width='auto'
                                               , style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"),

                     dbc.Col([dbc.Label("Тренер команди", style={'display': 'inline-block',
                                                               'margin-left': '10%', 'margin-right': '2%'})
                                 , dcc.Input(id="CoachName",
                                             value="Т.Б. Романець",
                                             style={'width': '50%', 'height': 30, 'minWidth': '200px'},
                                             type="text"
                                             , list="coach-options"
                                             , persistence=True), html.Datalist(id="coach-options", children=[
                             html.Option(value=fruit) for fruit in OPT_COACHES_LST
                         ])], width='auto'
                             , style={'display': 'flex', 'alignItems': 'center'}, className="mb-3")
                     ]))

        left_column_container.append(
            dbc.Row([dbc.Col([dbc.Label("Учасник", style={'display': 'inline-block',
                                                               'margin-left': '10%', 'margin-right': '2%'})
                                 , dcc.Input(id="MemberName",
                                             value="",
                                             style={'width': '50%', 'height': 30, 'minWidth': '200px'},
                                             type="text"
                                             , list="memberName-options"
                                             , persistence=True), html.Datalist(id="memberName-options", children=[
                    html.Option(value=name) for name in OPT_GIRLS_NAME+OPT_BOYS_NAME
                ]), dcc.RadioItems(['Дівчата', 'Хлопці'], 'Хлопці', inline=True, id="MemberSex",
                                   style={'display': 'inline-block','margin-left': '5px', 'margin-right': '5px'},
                                   labelStyle={'margin-left': '1px', 'margin-right': '5px'})], width='auto'
                             , style={'display': 'flex', 'alignItems': 'center'}, className="mb-3"),

                     dbc.Col([
                                 dbc.Label("Дата народження")
                                           # style={'display': 'inline-block',
                                           #                      'margin-left': '10%', 'margin-right': '2%'})
                                 , dcc.Input(id="MemberAge",
                                             value=11,
                                             min=4,
                                             max=18,
                                             style={'display': 'none'},#{'width': '11%', 'height': 30, 'minWidth': '200px'},
                                             type="number",
                                             persistence=True
                                             ),
                         dcc.Input(
                             id="MemberBirthDate",
                             type="date",
                             min=str((datetime.now()-timedelta(days=365*19)).date()),
                             max=str((datetime.now() - timedelta(days=365 * 4)).date()),
                             persistence=True,
                             persistence_type='local',
                        ),

                         dbc.Label("Вага")
                                  # , style={'display': 'inline-block',
                                  #                               'margin-left': '10%', 'margin-right': '2%'})
                                 , dcc.Input(id="MemberWeight",
                                             value=40,
                                             min=8,
                                             max=90,
                                             style={'width': '11%', 'height': 30, 'minWidth': '100px'},
                                             type="number"
                                             , persistence=True),], width='auto'
                             , style={'display': 'flex', 'alignItems': 'center'}, className="mb-3")
                     ]))

        ###################### Member Section List: #################
        left_column_container.append(
        dbc.Row([dbc.Col([dcc.Checklist(
    [],
    [],
    style={"margin-left": "10%"},
    id="SectionMemberCheck"   # fixed: Latin C
)]
            , width='auto', style={'display': 'flex', 'alignItems': 'center'}, className="mb-3", id="MemberSectionLists"),
            dbc.Col([dcc.RadioItems(
                [],
                []
                , style={"margin-left": "10%"}, id="CategoryMemberCheck")],id="MemberCategoryLists")]))
        left_column_container.append(dbc.Row([dbc.Col([html.Button("Додати до команди", id="AddMemberButton")
                                                       , html.Button("Редагувати учасника ", id="EditMemberButton")
                                                       ,html.Button("Видалити учасника ", id="RemoveMemberButton")
                                                       , html.Button("Інструкція", id="HelpButton")
                                                       , html.Button("Подати заявку", id="SubmitTeamButton")]

            , width='auto',
                                                      style={'display': 'flex',
                                                            "alignItems": "stretch",   # all same height
                                                            "gap": "6px"               # modern spacing between buttons
                                                             },
                                                      className="mb-3", id="TeamButtons")]))
        right_column_container = []
        right_column_container.append(dash_table.DataTable(
                    row_selectable="single",
                    id="TeamTable",
                    data=[],#[{'Учасник': 'Романець Вероніка', 'Вік': 14, 'Вага': 39, 'Категорія': None, 'Стать': 'Дівчата', 'Ката Дівчата': '+', 'Ката Хлопці': '-', 'Ката Мікс': '+', 'Куміте Дівчата': '+', 'Куміте Хлопці': '-', 'Куміте Мікс': '+', 'Командне ката Дівчата': '+', 'Командне ката Хлопці': '-', 'Командне ката Мікс': '+', 'Іпон-Шобу Дівчата': '+', 'Іпон-Шобу Хлопці': '-', 'Іпон-Шобу Мікс': '-'}, {'Учасник': 'Романець Вероніка', 'Вік': 14, 'Вага': 39, 'Категорія': None, 'Стать': 'Дівчата', 'Ката Дівчата': '+', 'Ката Хлопці': '-', 'Ката Мікс': '+', 'Куміте Дівчата': '+', 'Куміте Хлопці': '-', 'Куміте Мікс': '+', 'Командне ката Дівчата': '+', 'Командне ката Хлопці': '-', 'Командне ката Мікс': '+', 'Іпон-Шобу Дівчата': '+', 'Іпон-Шобу Хлопці': '-', 'Іпон-Шобу Мікс': '-'}, {'Учасник': 'Романець Оріон', 'Вік': 14, 'Вага': 39, 'Категорія': None, 'Стать': 'Хлопці', 'Ката Дівчата': '-', 'Ката Хлопці': '+', 'Ката Мікс': '+', 'Куміте Дівчата': '-', 'Куміте Хлопці': '+', 'Куміте Мікс': '+', 'Командне ката Дівчата': '-', 'Командне ката Хлопці': '+', 'Командне ката Мікс': '+', 'Іпон-Шобу Дівчата': '-', 'Іпон-Шобу Хлопці': '+', 'Іпон-Шобу Мікс': '-'}]
                    selected_rows = []
                    # columns=[{"name": i, "id": i} for i in df.columns],
                    ,style_table={
                        "height": "50vh",   # take ~90% of vertical screen
                        "overflowY": "auto" # scroll inside
                    },
                    style_cell={"textAlign": "right"}
                ))
        container_children.append(dbc.Row([dbc.Col(left_column_container, style={'alignItems': 'center',
                                                                                 "paddingRight":0}, width='auto')
                                              , dbc.Col(right_column_container, style={'alignItems': 'center',
                                                                                       "paddingRight":0}, width='auto')], className="g-0"))
        container_children.append(dcc.Input("", id="SetSexDirectly", style={"display": "none"}))
        container_children.append(dcc.Store(id="SetSectionDirectly", data=[]))
        container_children.append(dcc.Store(id="StoreTeamTable", data=[], storage_type="local"))
        container_children.append(dcc.Location(id="url"))
        container_children.append(dcc.Interval(interval=60000, id="Interval"))
        container_children.append(html.Div([dbc.Modal(
            [],
            id="MassageOnAdd",
            size="lg",
            is_open=False,
        ), dbc.Modal(
            [],
            id="MassageOnSubmit",
            size="lg",
            is_open=False,
        )
            , dbc.Modal(
                [],
                id="MassageOnBirthdate",
                size="lg",
                is_open=False,
            )
        ], className="modalDiv")
        )
        container_children.append(html.Div(children=[html.Button("Сформувати протоколи", id="ComposeProtocols"),
                                                     dcc.Download(id="ProtocolsOutput"),
                                                     html.Div(children=[],id="ComposeProtocolsProgress")],
                                           id="ComposeProtocolsContainer",
                                           hidden=True))
        children_ = self.dummy.get_children(self.title, container_children)
        return html.Div(children_, style={"margin-left": "5%"})

    def get_app(self, server, url):
        self.url = url
        cache = diskcache.Cache("./cache")
        long_callback_manager = DiskcacheManager(cache)
        app = Dash(__name__, url_base_pathname=url,
                   server=server,
                   background_callback_manager=long_callback_manager,
                   # external_stylesheets=[dbc.themes.LITERA])#
        assets_folder=parameter["assets_dir"])
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.layout = self.get_layout()
        app.config['suppress_callback_exceptions'] = True

        @app.callback([Output("LatterPattern", "style"),
                       Output("LatterExample", "style")],
                      Input("PatternOrExample", "value"))
        def pattern_or_example(radio):
            style_hidden = {'width': '100%', 'height': 350, 'display': 'none'}
            style_visible = {'width': '100%', 'height': 350, 'display': 'flex'}
            if radio == "Зразок":
                return style_hidden, style_visible
            else:
                return style_visible, style_hidden

        @app.callback(Output("LatterExample", "value"),
                      [Input("CompetitionTitle", "value")
            , Input("TeamLeadsEmails", "value")
                          , Input("TeamLeadsNames", "value")
                      , Input("SubmissionDeadline", "value")
                          , Input("CompetitionDate", "value"),
                       Input("LatterPattern", "value")])
        def compose_invitations(title, emails, names, deadline, competition_date, pattern):
            if callback_context.triggered_id == "CompetitionTitle":
                with open(parameter["config-path"], "r") as conf_:
                    conf_json = json.load(conf_)
                    conf_json["competition_title"] = title
                    parameter["competition_title"] = title
                    with open(parameter["config-path"], "w") as f_:
                        json.dump(conf_json, f_, indent=4)

            if callback_context.triggered_id == "SubmissionDeadline":
                with open(parameter["config-path"], "r") as conf_:
                    conf_json = json.load(conf_)
                    conf_json["deadline"] = deadline
                    parameter["deadline"] = deadline
                    with open(parameter["config-path"], "w") as f_:
                        json.dump(conf_json, f_, indent=4)
            if callback_context.triggered_id == "CompetitionDate":
                with open(parameter["config-path"], "r") as conf_:
                    conf_json = json.load(conf_)
                    conf_json["competition_date"] = competition_date
                    parameter["competition_date"] = competition_date
                    with open(parameter["config-path"], "w") as f_:
                        json.dump(conf_json, f_, indent=4)

            password = self.generate_secure_password()
            return self.compose_mail(names, emails, competition_date, deadline, title, pattern, password, idx=0)


        @app.callback([Output("InvitationsSent", "value"),
                       Output("InvitationsSent", "label")],
                      [Input("SendInvitations", "n_clicks"),
                          State("CompetitionTitle", "value")
            , Input("TeamLeadsEmails", "value")
                          , State("TeamLeadsNames", "value")
                      , State("SubmissionDeadline", "value")
                          , State("CompetitionDate", "value"),
                       State("LatterPattern", "value")], prevent_initial_callback=True)
        def send_invitations(n_clicks, title, emails, names, deadline, competition_date, pattern):
            this_competition_inv_dir = os.path.join(parameter["invitations_dir"], f"D{deadline}CD{competition_date}")
            names_ = [name_.lstrip().rstrip() for name_ in names.split(",")]
            emails_ = [email.lstrip().rstrip() for email in emails.split(",")]

            if not os.path.exists(this_competition_inv_dir):
                os.mkdir(this_competition_inv_dir)
            if callback_context.triggered_id == "SendInvitations":
                for idx_ in range(len(names_)):
                    sender = MailSender(parameter["mailer"], [emails_[idx_], parameter["club_email"]])
                    password = self.generate_secure_password()
                    message = self.compose_mail(names, emails, competition_date, deadline, title, pattern, password, idx=idx_)
                    files = []
                    sender.send_mail(f"Запрошення на змагання", message, files)
                    self.process_and_write_credits(emails_[idx_], names_[idx_], password)
                    with open(os.path.join(this_competition_inv_dir, emails_[idx_]), "w") as f:
                        f.write(message)
                return True, TOGGLE_LABEL_DICT[True]
            else:
                if os.path.exists(this_competition_inv_dir):
                    users_lst = glob(this_competition_inv_dir+"/*")
                    if emails_:
                        have_not_receive_msg = [e for e in set(emails_).difference(set(u.split("/")[-1] for u in users_lst))]
                        if have_not_receive_msg:
                            return False, TOGGLE_LABEL_DICT[False] +":"+", ".join(have_not_receive_msg)
                        else:
                            return True, TOGGLE_LABEL_DICT[True]
                return dash.no_update, dash.no_update


        @app.callback(Output("MemberCategoryLists", "children"),
                      [Input("CategoriesNames", "value"), State("MinAge", "value")
                       , State("MemberAge", "value")])
        def submit_member_category(str_categories, min_age, member_age):
            list_ = [s.rstrip().lstrip()  for s in str_categories.split(",")]

            if not list_:
                list_ = ["A"]
            return dcc.RadioItems(
                list_,
                list_[0]
                , style={"margin-left": "10%"}, id="CategoryMemberCheck")

        @app.callback(Output("CoachName", "value")
                      ,Input("url", "pathname"))
        def set_coach_name(url):
            with open(parameter["user-json-file"], "r") as f:
                users_json = json.load(f)
                print(current_user.id)
                print(list(users_json["users_names"].keys()))
                print(current_user.id in users_json["users_names"].keys())
                if current_user.id in users_json["users_names"].keys():
                    return users_json["users_names"][current_user.id]
            return dash.no_update

        # TeamLeadsName
        @app.callback(Output("coachName-options", "children"),
                      Input("TeamLeadsNames", "value"), prevent_initial_callback=True)
        def submit_coach_name_opt(name):
            if name is None:
                return dash.no_update
            if name == "":
                return dash.no_update
            name_lst = name.split()
            if len(name_lst) > 1:
                return [html.Option(value=f"{' '.join(name_lst[:-1])} {name}") for name in
                             OPT_GIRLS_NAME + OPT_BOYS_NAME]
            else:
                return [html.Option(value=name) for name in OPT_GIRLS_NAME + OPT_BOYS_NAME]
        # "MemberName"
        @app.callback([Output("MemberSex", "value"),Output("memberName-options", "children")],
                      [Input("MemberName", "value"),
                       State("SexCuts", "value")#State("MemberSex", "options")
                       ,Input("SetSexDirectly", "value"),
                       Input("url", "pathname")])
        def submit_member_sex(name, sex_cuts, directly, url):
            opt = [g.rstrip().lstrip() for g in sex_cuts.split(",")[:2]]
            if callback_context.triggered_id == "SetSexDirectly":
                return directly, dash.no_update
            sex = dash.no_update

            for name_part in name.split(" "):

                if name_part.rstrip().lstrip() in OPT_GIRLS_NAME:
                    sex = opt[0]
                elif name_part.rstrip().lstrip() in OPT_BOYS_NAME:
                    sex = opt[1]
                else:
                    continue
            name_lst = name.split()
            if len(name_lst) > 1:
                return sex, [html.Option(value=f"{' '.join(name_lst[:-1])} {name}") for name in OPT_GIRLS_NAME+OPT_BOYS_NAME]
            else:
                return sex, [html.Option(value=name) for name in OPT_GIRLS_NAME+OPT_BOYS_NAME]

        @app.callback(Output("MemberSectionLists", "children"),
                      [Input("MemberSex", "value"), Input("MemberSex", "options"),
                       Input("SectionLists", "children"), Input({"type": "Section-check","index": ALL}, "value")
                       , Input("SetSectionDirectly", "data")])
        def submit_member_section(sex_, options, children_checklists, triger, sections_values):

            lists_ = self.get_sections_lists_(sex_, options, children_checklists)
            if lists_:
                return dcc.Checklist(
                lists_,
                sections_values
                , style={"margin-left": "10%"}, id="SectionMemberCheck")
            else:
                return dash.no_update
            return [g.rstrip().lstrip() for g in sex_cuts.split(", ")[:2]]

        @app.callback(Output("MemberSex", "options"),
                      [Input("SexCuts", "value")])
        def submit_member_sex_options(sex_cuts):
            sex_cuts_lst = [g.rstrip().lstrip()  for g in sex_cuts.split(",")]
            return [g.rstrip().lstrip()  for g in sex_cuts.split(",")[:2]]

        @app.callback([Output("SectionLists", "children"),
                       Output("WeightlessSections", "children")],
                      [Input("Sections", "value"),
                       Input("SexCuts", "value")
                       ])
        def submit_sections(sections, sex_cuts):
            lists_ = []
            weightless_lst = []
            for id_idx, sec in enumerate(sections.split(",")):
                weightless_lst.append(sec.rstrip().lstrip())
                lists_.append([f"{sec.rstrip().lstrip()} {g.rstrip().lstrip()}" for g in sex_cuts.split(",")])
            if lists_:
                return self._get_checklists(lists_), self._get_weightless_checklists(weightless_lst, "Без ваги")
            else:
                return dash.no_update,  dash.no_update

        ################################################################
        @app.callback(Output("CategoriesNames", "value"),
                      [Input("CategoriesNumber", "value")], prevent_initial_callback=True)
        def submit_categories(categories_number):
            categories_names_lst = [chr(i + ord("A")) for i in range(categories_number)]
            return ", ".join(categories_names_lst)

        @app.callback(Output("CategoriesAge", "value"),
                      [Input("MinAge", "value"),
                       Input("AgeCuts", "value")], prevent_initial_callback=True)
        def submit_ages(min_age, age_step):
            max_age = 18
            categories_age_lst = [f"{a1}-{min(a2, max_age)-1}" for a1, a2 in zip(range(min_age, max_age, age_step), range(min_age+age_step, 18+age_step, age_step)) if (a1 != min(a2,max_age)-1)]
            if (max_age-min_age)% age_step != 0:
                max_age = 17
            categories_age_lst.append(f"{max_age}+")
            return ", ".join(categories_age_lst)

        @app.callback(Output("CategoriesWeightGirl", "value"),
                      [Input("MaxWeightGirl", "value"),
                       Input("WeightNumberGirl", "value")], prevent_initial_callback=True)
        def submit_weights(max_weight, weights_number):
            step = max_weight//weights_number
            start = max_weight % weights_number
            categories_weight_lst = [f"{a1}-{min(a2, max_weight)-1}" for a1, a2 in zip(range(start, max_weight, step), range(step+start, max_weight+step, step)) if (a1 != min(a2, max_weight)-1)]
            categories_weight_lst.append(f"{max_weight}+")
            return ", ".join(categories_weight_lst)

        @app.callback(Output("CategoriesWeightBoy", "value"),
                      [Input("MaxWeightBoy", "value"),
                       Input("WeightNumberBoy", "value")], prevent_initial_callback=True)
        def submit_weights(max_weight, weights_number):
            step = max_weight // weights_number
            start = max_weight % weights_number
            categories_weight_lst = [f"{a1}-{min(a2, max_weight) - 1}" for a1, a2 in
                                     zip(range(start, max_weight, step), range(step + start, max_weight + step, step))
                                     if (a1 != min(a2, max_weight) - 1)]
            categories_weight_lst.append(f"{max_weight}+")
            return ", ".join(categories_weight_lst)

        @app.callback([Output("TeamTable", "data"),
                       Output("MassageOnAdd", "children"),
                       Output("MassageOnAdd", "is_open")],
                      [Input("AddMemberButton", "n_clicks"),
                       Input("RemoveMemberButton", "n_clicks"),
                        Input("url", "pathname")],
                       [State("TeamTable", "selected_rows"),
                       State("MemberWeight", "value")
                      , State("MemberBirthDate", "value"), State("MemberName", "value")
                      , State("MemberSex", "value"), State("CategoryMemberCheck", "value")
                      , State("MemberSectionLists", "children")
                          , State({"type": "Section-check", "index": ALL}, "value")
                      , State("TeamTable", "data"), State("TeamTable", "columns")
                       , State("StoreTeamTable", "data")])
        def add_to_team(n_click_add, n_click_remove, url_fire, selected_rows, weight, birthdate, name, sex, category, sections_ch,
                        sections_all, table_data, table_columns, saved_data):
            if not hasattr(current_user, "name"):
                redirect("/")
            if table_data is None:
                table_data = []
            if (table_data == []) and (callback_context.triggered_id == "url"):
                if(current_user.name in saved_data):
                    return saved_data[current_user.name], dash.no_update, dash.no_update
                else:
                    return dash.no_update, dash.no_update, dash.no_update
            if not isinstance(table_data, list):
                table_data = [table_data]

            if (callback_context.triggered_id == "RemoveMemberButton") and selected_rows:
                table_data.pop(selected_rows[0])
                return  table_data, dash.no_update, dash.no_update
            # if not n_click:
            #     return dash.no_update, dash.no_update
            # print(sections_ch)
            if isinstance(sections_ch, list):
                sections_ch = sections_ch[0]
            sections = sections_ch["props"].get("value", [])
            if not sections:
                return dash.no_update, [
                dbc.ModalHeader(dbc.ModalTitle("Не надано інформацію")),
                dbc.ModalBody("Виберіть розділи для участі (принайні один)."),
            ], True
            if sex is None:
                return dash.no_update, [
                dbc.ModalHeader(dbc.ModalTitle("Не надано інформацію")),
                dbc.ModalBody("Виберіть стать учасника."),
            ], True
            # print(sections)
            sections_all = sum(sections_all, [])
            columns = (["Учасник", "Дата народження", "Вага", "Категорія", "Стать"] + sections_all) if  (table_columns is None) else dash.no_update
            dict_ = {"Учасник": name, "Дата народження": str(birthdate), "Вага": weight, "Категорія": category, "Стать": sex}

            for sec in sections_all:
                dict_[sec] = "+" if sec in sections else "-"


            table_data.append(dict_)
            df = pd.DataFrame(table_data, columns=columns)
            df.drop_duplicates(subset=["Учасник"], keep="last", inplace=True)
            return df.to_dict("records"), dash.no_update, dash.no_update

        @app.callback([Output("MemberName", "value")
                      , Output("MemberBirthDate", "value")
                      , Output("MemberWeight", "value")
                      , Output("CategoryMemberCheck", "value")
                      , Output("SetSectionDirectly", "data")
                      , Output("SetSexDirectly", "value")]
                      ,[State("TeamTable", "selected_rows"),
                        State("TeamTable", "data"),
                        Input("EditMemberButton", "n_clicks"),
                        State("MemberSex", "options"),
                        State("SectionLists", "children"),], prevent_initial_call=True)
        def correction(selected_rows, data, n_clicks, options, children_checklists):
            sex_ = data[selected_rows[0]]['Стать']
            options = self.get_sections_lists_(sex_, options, children_checklists)
            if (len(selected_rows)>0) and (n_clicks is not None):
                print(data[selected_rows[0]], n_clicks)
                sections = [sec for sec in options if data[selected_rows[0]].get(sec, "-") == '+']
                return (data[selected_rows[0]]["Учасник"], self.str_to_date(data[selected_rows[0]]["Дата народження"]), data[selected_rows[0]]["Вага"]
                        ,data[selected_rows[0]]["Категорія"], sections, data[selected_rows[0]]["Стать"])

        @app.callback(Output("StoreTeamTable", "data"),
                     [Input("TeamTable", "data")], prevent_initial_call=True)
        def save_app(table_data):
            if hasattr(current_user, "name"):
                data_dict = {current_user.name: table_data}
                return data_dict
            else:
                redirect("/")
        @app.callback(Output("CountDownDisplay", "value"), [Input("Interval", "n_intervals"),
                                 Input("SubmissionDeadline", "value"),] )
        def deadline_countdown(interval, deadline_date):
            if not hasattr(current_user, "name"):
                redirect("/")
            deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date()
            specific_time = time(0, 0, 0)
            dtime_seconds = (datetime.combine(deadline_date, specific_time)-datetime.now()).total_seconds()
            hh = dtime_seconds//3600
            mm = (dtime_seconds%3600)//60
            return f"{int(hh)}:{int(mm):02}"

        # id = "damin_only_tools", style = {"display": "none"}
        @app.callback([Output("admin_only_tools", "hidden"),
                       Output("ComposeProtocolsContainer", "hidden")],
                      Input("url", "pathname"))
        def verify_user_permissions(url):
            if not hasattr(current_user, "permission"):
                redirect("/")
            else:
                if current_user.permission == "admin":
                    return False, False
                else:
                    return dash.no_update, dash.no_update

        @app.callback([Output("MassageOnSubmit", "children"),
                       Output("MassageOnSubmit", "is_open")],
                      [Input("SubmitTeamButton", "n_clicks")
                          ,Input("HelpButton", "n_clicks")
                       ,State("TeamTable", "data")
                          , State("SubmissionDeadline", "value")
                                   , State("CompetitionDate", "value")
                          , State("CompetitionTitle", "value")
                       ,State("CoachName", "value")
                       ], prevent_initial_call=True)
        def on_submit(n_clicks, help_clicks, team_table_data, deadline, competition_date, competition_title, coach_name):
            if not hasattr(current_user, "permission"):
                redirect("/")
            if callback_context.triggered_id == "HelpButton":
                title = "Інструкція"
                issue = "Для створення Заявки на участь у змаганнях виконуйте послідовність дій зазначену нижче."
                return self.get_help(title, issue), True

            if team_table_data:

                # df.to_csv(os.path.join(parameter["data_dir"],current_user.name+".cvs"))
                this_competition_submission_dir = self.get_submission_dir(deadline, competition_date)

                df = pd.DataFrame(team_table_data)
                # df_ = df.set_index.iloc[5:]
                df["total_sections"] = df.apply(lambda l: (l == "+").sum(), axis=1)
                if (df["total_sections"] == 0).any():
                    names_lst = df.loc[df["total_sections"] == 0, "Учасник"].to_list()
                    return [
                        dbc.ModalHeader(dbc.ModalTitle("Не надано інформацію")),
                        dbc.ModalBody(f"Виберіть розділи для участі (принайні один для {', '.join(names_lst)}"),
                    ], True
                else:
                    members_lst = ",".join(df["Учасник"].str.strip().to_list()).split(",")
                    n_members = len(set(members_lst))
                    n_sections = df["total_sections"].sum()
                    n_only_one_section = (df["total_sections"] == 1).sum()
                    sender = MailSender(parameter["mailer"], [current_user.id, parameter["club_email"]])
                    message = self.get_massage_on_submission(n_members, n_sections, n_only_one_section, competition_title)
                    df.drop(columns=["total_sections"], inplace=True)
                    file = os.path.join(this_competition_submission_dir, current_user.id + ".csv")
                    df.to_csv(file)
                    files = [file]
                    sender.send_mail(f"Заявка прийнята", message, files)
                return [
                dbc.ModalHeader(dbc.ModalTitle("Дякуємо!")),
                dbc.ModalBody(message),
            ], True
            else:
                title = "Заявка не містить учасників!"
                issue = "Для створення Заявки на участь у змаганнях виконуйте послідовність дій зазначену нижче."
                return self.get_help(title, issue), True

        @app.callback(Output("ProtocolsOutput", "data"),
                      inputs=[Input("ComposeProtocols", "n_clicks")
                        , State("SubmissionDeadline", "value")
                        , State("CompetitionDate", "value")
                          , State("CategoriesAge", "value")
                          , State("CategoriesWeightGirl", "value")
                          , State("CategoriesWeightBoy", "value")
                          , State("CategoriesNames", "value")
                          ,  State({"type": "Section-check", "index": ALL}, "value")
                          , State("Weightless-check", "value")
                          , State("CompetitionTitle", "value")
                          , State("ChiefSecretary", "value")
                          , State("ChiefJudge", "value")
                          , State("SexCuts", "value")
                       ]
            , ranning=[(Output("ComposeProtocols", "disabled"), True, False), ],
                      progress=[
                          Output("ComposeProtocolsProgress", "children")
                      ],
                      prevent_initial_callback=True
                      , background=True)
        def compose_protocols(progress, n_clicks, deadline, competition_date, ages, weights_girls, weights_boys, categories, sections,
                              weightless, competition_title, chief_secretary, chief_judge, sex_cuts):
            sex_cuts_lst_ = [g.rstrip().lstrip() for g in sex_cuts.split(",")]
            sections = sum(sections, [])
            path_ = self.get_submission_dir(deadline, competition_date)
            submission_files = glob(os.path.join(path_, "*.csv"))
            if n_clicks is None:
                return dash.no_update
            full_dic = {}
            files_total = len(submission_files)
            for n_fl, file_ in enumerate(submission_files):
                df_ = pd.read_csv(file_)
                df_["team-lead"] = basename(file_)
                df_["Вік"] = df_["Дата народження"].map(lambda birthdate: int((self.str_to_date(competition_date) - self.str_to_date(birthdate)).days/365.25))
                age_bins, age_labels = self.get_bins(ages)
                df_["age_cuts"] = pd.cut(df_["Вік"], age_bins, labels=age_labels)
                weight_girls_bins, weight_girls_labels = self.get_bins(weights_girls)
                df_["weight_girls_cuts"] = pd.cut(df_["Вага"], weight_girls_bins, labels=weight_girls_labels)

                weight_boys_bins, weight_boys_labels = self.get_bins(weights_boys)
                df_["weight_boys_cuts"] = pd.cut(df_["Вага"], weight_boys_bins, labels=weight_boys_labels)


                for n,sec in enumerate(sections):
                    is_weightless = any([sec.find(w)!=-1 for w in weightless])
                    is_girl = sec.find(sex_cuts_lst_[0]) != -1
                    is_boy = sec.find(sex_cuts_lst_[1]) != -1
                    is_mixed_sex = (not is_boy) and (not is_girl)
                    progress_percent = int(90*(n+1)*(n_fl+1)/(len(sections)*files_total))
                    progress(self.progress_input(progress_percent))
                    for cat in categories:
                        for age, age_b in zip(age_labels, age_bins):
                            if is_weightless or is_mixed_sex:
                                title_ = f"{sec} (категорія {cat}, {age} років)"
                                mask = ((df_["age_cuts"] == age_b)
                                        & (df_["Категорія"] == cat) & (df_[sec] == "+"))
                                df__ = df_.loc[mask]
                                df__["count"] = df__.shape[0]
                                if not df__.empty:
                                    if title_ in full_dic:
                                        full_dic[title_].append(df__)
                                    else:
                                        full_dic[title_] = [df__]
                            elif is_girl:
                                for weight, weight_b in zip(weight_girls_labels, weight_girls_bins):
                                    mask = ((df_["age_cuts"] == age_b) & (df_["weight_girls_cuts"] == weight_b)
                                            & (df_["Категорія"] == cat) & (df_[sec] == "+"))
                                    df__ = df_.loc[mask]
                                    df__["count"] = df__.shape[0]
                                    title_ = f"{sec} (категорія {cat}, {age} років {weight}кг)"

                                    if not df__.empty:
                                        if title_ in full_dic:
                                            full_dic[title_].append(df__)
                                        else:
                                            full_dic[title_] = [df__]
                            elif is_boy:
                                for weight, weight_b in zip(weight_boys_labels, weight_boys_bins):
                                    mask = ((df_["age_cuts"] == age_b) & (df_["weight_boys_cuts"] == weight_b)
                                            & (df_["Категорія"] == cat) & (df_[sec] == "+"))
                                    df__ = df_.loc[mask]
                                    df__["count"] = df__.shape[0]
                                    title_ = f"{sec} (категорія {cat}, {age} років {weight}кг)"

                                    if not df__.empty:
                                        if title_ in full_dic:
                                            full_dic[title_].append(df__)
                                        else:
                                            full_dic[title_] = [df__]

            protocols_dir = self.get_protocols_dir(deadline, competition_date)
            excel_writer = ExcelWriter(competition_title, chief_secretary, chief_judge, protocols_dir)
            protocol_dict = self.compose_protocols_(full_dic)
            files_attach = []
            progress_percent = 92
            progress(self.progress_input(progress_percent))
            for key in protocol_dict.keys():
                df = protocol_dict[key]
                # file_ = os.path.join(protocols_dir, key+".csv")
                # df.to_csv(file_, index=False)
                excel_writer.write_style(df, key)

            sender = MailSender(parameter["mailer"], [parameter["club_email"], "pn_romanets@yahoo.com"])
            message = """
            Привітики. Протоколи в додатку.
            Цьом.
            """
            zip_path = f"{protocols_dir}.zip"
            # Create a zip file
            progress_percent = 95
            progress(self.progress_input(progress_percent))

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(protocols_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        files_attach.append(file)
                        # Add file to the zip, maintaining directory structure
                        arcname = os.path.relpath(file_path, protocols_dir)
                        zipf.write(file_path, arcname)
            progress_percent = 98
            progress(self.progress_input(progress_percent))
            sender.send_mail(f"Протоколи {datetime.now()}", message, [zip_path])
            progress_percent = 100
            progress(self.progress_input(progress_percent))
            # Return the zip file for download
            return dcc.send_file(zip_path)

        # @app.callback([Output("MemberAge", "value"),
        #                Output("MassageOnBirthdate", "children")],
        #               [
        #               Input("MemberBirthDate", "value")
        #               , State("CompetitionDate", "value")
        #               , State("MinAge", "value")]
        #               )
        # def birthday(birthdate, competition_date, min_age):
        #     member_age = int((competition_date - birthdate).days/365.25)
        #     if (member_age >= min_age) and (member_age <= 18):
        #         return member_age, dash.no_update
        #     else:
        #         return dash.no_update, f"Не правильна дата народження учасника. Вік учасника може бути від {min_age} до 18"

        @app.callback(Output("CategoriesNamesHidden", "children"),
                      Input("CategoriesNames", "value"))
        def dump_categories(categories):
            self.modify_config_file("categories_names_lst", [c.lstrip().rstrip() for c in categories.split(",")])
            return dash.no_update

        @app.callback(Output("CategoriesWeightHidden", "children"),
                      Input("CategoriesWeight", "value"))
        def dump_category_weight(categories):
            self.modify_config_file("categories_weight_lst", [c.lstrip().rstrip() for c in categories.split(",")])
            return dash.no_update

        @app.callback(Output("CategoriesAgeHidden", "children"),
                      Input("CategoriesAge", "value"))
        def dump_category_age(categories):
            self.modify_config_file("categories_age_lst", [c.lstrip().rstrip() for c in categories.split(",")])
            return dash.no_update

        @app.callback([Output("SectionsHidden", "children")]
            , [Input("Sections", "value"), Input("SexCuts", "value")])
        def dump_sections(sections, sex_cuts):
            self.modify_config_file("sections_all_lst", [s.rstrip().lstrip() for s in sections.split(",")])
            # lists_ = []
            # for id_idx, sec in enumerate(sections.split(",")):
            #     lists_.append([f"{sec.rstrip().lstrip()} {g.rstrip().lstrip()}" for g in sex_cuts.split(",")])
            # if lists_:
            #     self.modify_config_file("sections_all_lst", lists_)
            return dash.no_update

        @app.callback([Output("SexCutsHidden", "children")]
            , [Input("SexCuts", "value")])
        def dump_sections(sex_cuts):
            self.modify_config_file("sex_cuts_lst", [s.lstrip().rstrip() for s in sex_cuts.split(",")])
            return dash.no_update


        return app


if __name__ == "__main__":
    df = pd.DataFrame({
    "Учасник": ["Aba", "Bao", "Ceo", "Leo", "Gven", "Tetera", "Moana", "Dudya", "Klerk"],
    "team-lead": ["t1", "t1", "t1", "t1", "t2", "t2", "t2", "t3", "t3"],
    "count": [4, 4, 4, 4, 3, 3, 3, 2, 2]
})

    obj = InterestingClass("", "", 100)
    t0 = datetime.now()
    for i in range(33):
        df_res = obj.split_opponents(df)
    print(df_res)
    print(datetime.now()-t0)