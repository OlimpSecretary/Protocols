import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
import time
from configs import config
from app import menu_values as mv
# from app.navigations import navigation as nav
import os
from os.path import join as path_join
import random
import base64
# import dash_dangerously_set_inner_html
# os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


def get_base_template(server, body, title, user_name):
    current = 'current'

    app = Dash(name='home', url_base_pathname='/home/', server=server, static_folder='assets')
    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    })
    app.scripts.append_script({"external_url": '/assets/my.css'})
    app.scripts.append_script({"external_url": '/assets/theme.css'})

    app.layout = html.Div(children=[

            html.Link(href='/assets/my.css' + "?t=" + str(time.time()), rel='stylesheet'),
            get_header(title),
            get_main_menu(current),
            get_dropdown_menu(),
            body,
            get_footer(user_name)
        ])

    return app


def get_main_menu(current):
    return html.Div(children=[], className="float-clear")


def get_dropdown_menu():
    return [
        dcc.Dropdown(
            id='branch-dropdown',
            options=mv.get_branches(),
            placeholder='Будь-ласка, оберіть відділення чи напишіть у полі для пошуку потрібного відділення'.upper()
        ),
        dcc.Dropdown(
            id='service-dropdown',
            options=mv.get_service_type(),
            value="all",
            placeholder='Будь-ласка, оберіть тип послуги'

        ),
        dcc.Dropdown(
            id='cargo-dropdown',
            options=mv.get_cargo_type(),
            value="all",
            placeholder='Будь-ласка, оберіть тип відправленя'

        ),

        dcc.Dropdown(
            id='direction-dropdown',
            options=mv.get_directions(),
            value="all",
            placeholder='Будь-ласка, оберіть напрямок трафіку'
        ),

        dcc.Dropdown(
            id='location-dropdown',
            options=mv.get_locations(),
            value="all",
            placeholder='Будь-ласка, оберіть географію'
        ),

        dcc.Dropdown(
            id='time-dropdown',
            options=mv.get_time_frame(),
            value="day",
            placeholder='Будь-ласка, оберіть часовий інтервал'
        )


    ]


def get_header(title):
    assets_folder = config.parameter["assets_dir"]

    image_filename = path_join(assets_folder, "logo.png")

    #################################################

    # image_filename = path_
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())

    # path_css1 = path_join(assets_folder, "my.css")
    # path_css2 = path_join(assets_folder, "theme.css")
    # path_js = path_join(assets_folder, "custom-script.js")
    # #################################################
    # css_code1 = open(path_css1, 'r').read()
    # css_code2 = open(path_css2, 'r').read()
    # js_code = open(path_js, 'r').read()
    # html_css1 = dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
    #     f""" <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    #          <style type="text/css">
    #          {css_code1}
    #          </style>""")
    # html_css2 = dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
    #     f""" <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    #          <style type="text/css">
    #          {css_code2}
    #          </style>""")
    # html_js = dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
    #     f""" <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    #          <script>
    #          {js_code}
    #          <script>""")
    return html.Div(children=[
        # html.Link(href=assets_folder+'my.css' + "?t=" + str(time.time()), rel='stylesheet'),
        # html_css1, html_css2, html_js,
        #html.Link(href=assets_folder+'theme.css' + "?t=" + str(time.time()), rel='stylesheet'),
        # html.Script(src=assets_folder+'custom-script.js' + "?t=" + str(time.time())),

        html.Div([html.Img(src=f'data:image/png;base64,{encoded_image.decode()}', className="logo", width="64", height="64", style={"margin-right": "15px"}),
        html.H1(children=title)], style={'display': 'flex'}),
        html.H3(children='Гідних сувпротивників та цікавих змагань!!!')
    ], style={ 'margin-left': '9%', 'margin-right': '1%'})


def get_footer(user_name):
    if user_name != "None":
        return html.Div(className="footer", children=[
            "Версія додатку: " + str(config.application_version) + " | user: " + user_name + " | " +
            config.parameter["server-version"]])
    else:
        return html.Div(className="footer", children=[
            "Версія додатку: " + str(config.application_version) + " | " +
            config.parameter["server-version"]])



def custom_index(self, *args, **kwargs):  # pylint: disable=unused-argument

    scripts = self._generate_scripts_html()
    css = self._generate_css_dist_html()
    config = self._generate_config_html()
    title = getattr(self, 'title', 'Dash')

    js = "/assets/custom-script.js?ts=" + str(random.random())

    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{}</title>
            {}
            <link rel="icon" type="image/png" href="/static/favicon-16x16.png" sizes="16x16" />

        </head>
        <body>
            <div id="react-entry-point">
                <div class="_dash-loading">
                    Loading...
                </div>
            </div>
            <div id="pop-div" class="pop-div" style="display: none;">
            </div>
            <footer>
                {}
                {}
            </footer>
        </body>
        <script src="{}"></script>
    </html>
    '''.format(title, css, config, scripts, js)