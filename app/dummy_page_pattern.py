import dash_core_components as dcc
from dash import html
from dash import Dash
from dash.dcc import Markdown
import time
# import dash_dangerously_set_inner_html
# from configs import config
from configs.config import parameter
from app import base
# import dash_dangerously_set_inner_html


class Dummy:
    def __init__(self, home_url, home_name):
        self.home_url = home_url
        self.home_name = home_name


    def get_children(self, text, inter_part):
        children_ = [

            html.Link(href='/assets/my.css' + "?t=" + str(time.time()), rel='stylesheet'),
            base.get_header(text), html.Div(id="js"),
            html.A(html.Button(self.home_name, id='btn', n_clicks=0), href=self.home_url),
            html.Div(id='output-container', className="home-text", children=[

                Markdown("""
                """)

            ])]
        if inter_part:
            children_ = children_ + inter_part

        children_.append(html.Div(style=parameter["footer_style"],
                                  children=[" дзвоніть нам: " + str(parameter["main_mobile_phone_number"])
                                            , " пішіть у Viber:" + str(parameter["viber_phone_number"])
                                            ,  " пішіть на електронну пошту:" + str(parameter["club_email"])]))
        return children_

    def get_app(self, server, url, text):
        app = Dash(__name__, url_base_pathname=url, server=server, assets_folder=parameter["excel-path"])
        self.layout = html.Div(children=self.get_children(text, []), style={"margin-left": "25%"})
        app.layout = self.layout
        app.config['suppress_callback_exceptions'] = True
        return app
