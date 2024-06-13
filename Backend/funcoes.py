import urllib.request
from datetime import datetime
from database import*


def html_from_url(url):
   return str(urllib.request.urlopen(url).read())


#This function extracts the url from the videos in the page
def list_of_videos(url):
    lista = []
    page = html_from_url(url)
    page = page.split("watch?v=")[1:]
    for video in page:
        if len(video) > 6000:
            lista.append(video[:11])
    return lista


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
def update_videos_list(qtd=2):
    for canal in load_channels_list_in_database():
        lista_de_videos_no_canal = list_of_videos(canal)
        update_channel_videos_list(canal,lista_de_videos_no_canal)
    make_videos_list(qtd)


#This function is to send the videos to Frontend
def send_videos_list():
    return load_video_list()['videos']
