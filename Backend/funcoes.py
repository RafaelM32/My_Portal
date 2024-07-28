import urllib.request
from datetime import datetime
from database import*
import jwt
from flask import json


def html_from_url(url):
   return str(urllib.request.urlopen(url).read())


#This function extracts the url from the videos in the page
def list_of_videos_and_images(url):
    qtd = load_video_list()['videos_qtd']
    videos_list = []
    tumb_list = []
    tittle_list = []
    page = html_from_url(url)
    images = page.split('{"thumbnails":[{"url":')[1:-2]
    aux = 0
    for i in range(0,len(images)):
        if aux < qtd:
            tumb_link = take_tumb(images[i])
            if '://i.ytimg.com/vi' in tumb_link:
                tittle_list.append(take_title(images[i]))
                videos_list.append(take_video_code(tumb_link))
                tumb_list.append(tumb_link)
                aux +=1
    return {'videos_list': videos_list, 'tumb_list':  tumb_list, 'tittle_list': tittle_list}


#This function cheks if has bem passed more than x minutes
def is_more_the_x_minutes(x):
    now = datetime.now()
    last_load = load_video_list()['time']
    total_minutes = ((now - last_load).total_seconds())/60
    if total_minutes >= x:
        return True
    else:
        return False




#This function cheks is a chennel alrely is in the chennels list
def channel_is_saved(channel):
    return channel_is_saved_in_database(channel)


#This function saves a new chennel in the list
def save_channel(channel):
    if not channel_is_saved(channel):
        save_channel_in_database(channel)
        return f'{channel.split('/')[3]} foi adicionado com sucesso!'
    else:
        return f'{channel.split('/')[3]} já consta na lista de canais!'


#This deleletes a channel in the channel_list
def delete_channel(channel):
    if channel_is_saved(channel):
        delete_channel_in_database(channel)
        return f'{channel.split('/')[3]} foi removido com sucesso!'
    else:
        return f'{channel.split('/')[3]} não está na lista!'


#This function makes de reload of the videos in channels
def update_videos_list(qtd):
    for canal in load_channels_list_in_database():
        lista_de_videos_e_imagens_no_canal = list_of_videos_and_images(canal,qtd)
        update_channel_videos_list(canal,lista_de_videos_e_imagens_no_canal['videos_list'])
        update_channel_tumb_list(canal,lista_de_videos_e_imagens_no_canal['tumb_list'])
        update_channel_tittle_list(canal,lista_de_videos_e_imagens_no_canal['tittle_list'])
    make_videos_list()


#This function is to send the videos to Frontend
def send_videos_list():
    return load_video_list()


def take_tumb(img:str):
    return img.split('"width')[0][1:-2]

def take_video_code(url):
    return url.split('/')[4]

def take_title(string):
    return string.split('"title"')[1].split('{')[2][8:-20]


def generate_token_session(username, sessionIP):
    return jwt.encode({'username': username, 'sessionIP': sessionIP}, os.environ['SECRET_KEY'],algorithm="HS256")

def decode_token_session(token):
    return jwt.decode(token,os.environ['SECRET_KEY'], algorithms="HS256")

def is_valid_token(token, sessionIP):
    try:
        decoded = decode_token_session(token)
    except:
        return False
    
    if decoded['sessionIP'] == sessionIP:
        for user in load_users():
            if token in user['session_tokens']:
                return True
            else:
                return False
    else:
        return False

