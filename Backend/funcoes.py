import urllib.request
from datetime import datetime


#This 3 variables will goin to be replaced by a call to a BD
lista_de_canais = ["https://www.youtube.com/@Mamaefalei/videos","https://www.youtube.com/@NandoMouraOficial/videos",
                   "https://www.youtube.com/@rbiana/videos","https://www.youtube.com/@manodeyvin/videos",
                   "https://www.youtube.com/@CortesdoCasimitoOFICIAL/videos","https://www.youtube.com/@CortesdoPirullaOficial/videos",
                   "https://www.youtube.com/@izzynobre/videos","https://www.youtube.com/@leoeisa/videos",
                   "https://www.youtube.com/@LucasMontano/videos","https://www.youtube.com/@cortes-leonenilceoficial4101/videos",
                   "https://www.youtube.com/@CortesCienciaSemFim/videos","https://www.youtube.com/@republicacoisadenerd/videos",
                   "https://www.youtube.com/@tinocandotv/videos","https://www.youtube.com/@Pirulla25/videos",
                   "https://www.youtube.com/@BakaGaijinn/videos","https://www.youtube.com/@AllandosPanos/videos",
                   "https://www.youtube.com/@maromberu/videos","https://www.youtube.com/@MaiconKusterNews/videos",
                   "https://www.youtube.com/@MxRPlays/videos","https://www.youtube.com/@luideverso/videos"]
lista_de_videos_em_cada_canal =[]
last_time = [2024,6,5,7,3]


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

#This function save the actual time. It is to be used to mark the last time the server 
#Make the update from the videos
def save_time():
    now = datetime.now()
    last_time[0] = now.year
    last_time[1] = now.month
    last_time[2] = now.day
    last_time[3] = now.hour
    last_time[4] = now.minute


#This function cheks if has bem passed more than x minutes
def is_more_the_x_minutes(x):
    now = datetime.now()
    last_load = datetime(last_time[0],last_time[1],last_time[2],last_time[3],last_time[4])
    total_minutes = ((now - last_load).total_seconds())/60
    if total_minutes >= x:
        return True
    else:
        return False



#This function cheks is a chennel alrely is in the chennels list
def channel_is_saved(channel):
    for canal in lista_de_canais:
        if canal == channel:
            return True
    return False

#This function saves a new chennel in the list
def save_channel(channel):
    if not channel_is_saved(channel):
        lista_de_canais.append(channel)
        return f'{channel.split('/')[3]} foi adicionado com sucesso!'
    else:
        return f'{channel.split('/')[3]} já consta na lista de canais!'


#This deleletes a channel in the channel_list
def dele_channel(channel):
    if channel_is_saved(channel):
        lista_de_canais.remove(channel)
        return f'{channel.split('/')[3]} foi removido com sucesso!'
    else:
        return f'{channel.split('/')[3]} não está na lista!'


#This function makes de reload of the videos in channels
def upload_videos_list():
    lista_de_videos_em_cada_canal.clear()
    for canal in lista_de_canais:
        videos_no_canal = list_of_videos(canal)
        lista_de_videos_em_cada_canal.append(videos_no_canal)
    save_time()


#This function is to send the videos to Frontend
def send_videos_list(qtd=2):
    lista = []
    for videos in lista_de_videos_em_cada_canal:
        for i in range(qtd):
            lista.append(videos[i])
    return lista

