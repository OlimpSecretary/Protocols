from os.path import join as path_join
import os
import base64
from configs.config import parameter

assets_path = parameter["assets_dir"]
path_svg = path_join(assets_path, "logo.png")
# print(path_svg)
# print(os.path.exists(path_svg))
path_css = path_join(assets_path, "my.css")
#################################################
css_code = open(path_css, 'r').read()
image_filename = path_svg
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


# <img src="data:image/svg;base64,{encoded_image}" alt="logo" height="100" width="100">
def get_login_form_html():
    return f'''
            <center>
            <br>
            <br>
            <br>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
             <style type="text/css">
             {css_code}
             </style>
            <img src="data:image/png;base64,{encoded_image.decode()}" alt="logo" height="100" width="100">
            <br>
                <h1>Вхід у тренерську спортивного клубу "Олімп" </h1>
            <br>
            <br>
            <h1>логін</h1>
            <form action="" method="post">
                <table border=0 style="border: 0px;">
                    <tr>
                        <td style="border: 0px;">користувач:</td>
                        <td style="border: 0px;"><input type=text name=username></td>                
                    </tr>
                    <tr>
                        <td style="border: 0px;">пароль:</td>
                        <td style="border: 0px;"><input type=password name=password></td>               
                    </tr>            
                </table>                
            <!--/form-->
            <!--form action="" method="post"-->
            <p><input type=submit value="логін" style="margin: 0px 0 0 -75px;"></p>
            </form>
            </center>
                '''


def get_logout_html():
    return f"""
    <br>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
     <style type="text/css">
     {css_code}
     </style>
    <br>   
    <center>
        <img src="data:image/png;base64,{encoded_image.decode()}" alt="logo" height="100" width="100">
        <br>   
        <br>   
            <h1>Ви успішно вийшли зі свого акаунту!</h1>
        <br>
        <p>
            <a href="/login">УВІЙТИ ЗНОВУ</a>
        </p> 
    </center>

    """

