import dash_core_components as dcc
import dash_html_components as html
import random
# from additional import security as sec
import flask_login
from configs.config import parameter

class sec:
    @staticmethod
    def can_see_navigation(user, element):
        return True

#
# def get_sudo_navigation():
#
#     user = str(flask_login.current_user)
#
#     ret = []
#
#     about_instructors = []
#     dic_ = parameter["sport_types_inv"]
#     for key_ in dic_.keys():
#         sport_kind = dic_[key_]
#         folder = html.Li(html.A(sport_kind, href=f'/sudo_about_instructors_{key_}'))
#         about_instructors.append(folder)
#
#     about_dropdown = []
#     about_dropdown.append(html.Li(html.A('ІСТОРІЯ', href=f'/sudo_club_history/')))
#     # about_dropdown.append(get_dropdown_menu_item("ПРО ТРЕНЕРІВ", about_instructors_K, '/about_instructors_K/'))
#     about_dropdown.append(html.Li(html.A('ВНУТРІШНЯ ПОЛІТИКА', href=f'/sudo_about_politics')))
#     about_dropdown.append(html.Li(html.A('УСТАТКОВАНЯ ПРИМІЩЕННЯ', href=f'/sudo_about_equipment')))
#
#     schedules_dropdown = []
#     schedules_dropdown.append(html.Li(html.A('РОЗКЛАД ТРЕНУВАНЬ', href=f'/schedules/')))
#     schedules_dropdown.append(html.Li(html.A('ВАЖЛИВІ ПОДІЇ', href=f'/sudo_events/')))
#     # schedules_dropdown.append(html.Li(html.A('ТРЕНЕРСЬКА', href=f'/staff_only/')))
#
#     # additional_reports = []
#     # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/contacts/')))
#     # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/interesting/')))
#     # additional_reports.append(html.Li(html.A('КОНТАКТИ', href=f'/stuff_only/')))
#
#     interesting_dropdown = []
#     interesting_dropdown.append(html.Li(html.A('СВІТ КАРАТЕ', href=f'/sudo_interesting_K/')))
#     interesting_dropdown.append(html.Li(html.A('СВІТ ЙОГИ', href=f'/sudo_interesting_Y/')))
#     interesting_dropdown.append(html.Li(html.A('СВІТ ТАНЦЮ', href=f'/sudo_interesting_D/')))
#     interesting_dropdown.append(html.Li(html.A('СВІТ АКРОБАТИКИ', href=f'/sudo_interesting_A/')))
#     ret.append(get_dropdown_menu_item("ПРО КЛУБ", about_dropdown, 'sudo_about/'))
#     ret.append(get_dropdown_menu_item("ПРО ТРЕНЕРІВ", about_instructors, 'sudo_about_instructors_K/'))
#     ret.append(get_dropdown_menu_item("НАШ КАЛЕНДАР", schedules_dropdown, 'sudo_calendar/'))
#     ret.append(get_dropdown_menu_item("РІЗНІ ЦІКАВИНКИ", interesting_dropdown, 'sudo_interesting/'))
#     ret.append(get_dropdown_menu_item("ЗБОРИ", [], 'sudo_summertime/'))
#     ret.append(get_dropdown_menu_item("ВИЙТИ З ТРЕНЕРСЬКОЇ", [], ''))
#
#
#     return ret


def get_navigation():

    user = str(flask_login.current_user)

    ret = []


    about_dropdown = []
    about_dropdown.append(html.Li(html.A('ІНСТРУКЦІЯ', href='/instruction/')))
    # about_dropdown.append(get_dropdown_menu_item("ПРО ТРЕНЕРІВ", about_instructors_K, '/about_instructors_K/'))
    about_dropdown.append(html.Li(html.A('СТВОРИТИ ПРОТОКОЛИ', href='/create_protocols/')))
    about_dropdown.append(html.Li(html.A('АРХІВ ПРОТОКОЛІВ', href='/archive_protocols/')))


    ret.append(get_dropdown_menu_item('ЗМАГАННЯ', about_dropdown, '/competitions/'))



    return ret


def get_dropdown_menu_item(title, folder_dropdown, href='#'):
    if folder_dropdown:
        return html.Ul(
            children=[
                # ul list components
                html.Li(
                    className='dropdown',
                    children=[
                        html.A(
                            title,
                            className='dropbtn'
                        ),
                        html.Div(
                            className='dropdown-content',
                            children=folder_dropdown
                        )
                    ]

                )
            ]
        )
    else:
        return html.Ul(
            children=[
                html.Li(
                    className='dropdown',
                    children=[
                        html.A(
                            title,
                            href='/' + str(href),
                            className='dropbtn'
                        )

                    ]

                )
            ]
        )
