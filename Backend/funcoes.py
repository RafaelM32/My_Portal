import urllib.request
from datetime import datetime
from database import*


def html_from_url(url):
   return str(urllib.request.urlopen(url).read())


#This function extracts the url from the videos in the page
def list_of_videos_and_images(url):
    videos_list = []
    tumb_list = []
    tittle_list = []
    page = html_from_url(url)
    images = page.split('{"thumbnails":[{"url":')[1:-2]
    for image in images:
        tumb_link = take_tumb(image)
        if '://i.ytimg.com/vi' in tumb_link:
            tittle_list.append(take_title(image))
            videos_list.append(take_video_code(tumb_link))
            tumb_list.append(tumb_link)
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
def update_videos_list():
    print('A função update foi chamada')
    for canal in load_channels_list_in_database():
        lista_de_videos_e_imagens_no_canal = list_of_videos_and_images(canal)
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
    return youtube_text_decode(string.split('"title"')[1].split('{')[2][8:-20])

def youtube_text_decode(texto:str):
    codigos = [['\\\\"', '"'],['\\xc3\\x83','Ã'],['\\xc3\\x82','Â'],['\\xc3\\x87', 'Ç'],
               ['\\xf0\\x9f\\x8c\\x88','&#127752;'],['\\xc3\\x8a','Ê'],['\\xc3\\x8d', 'Í'],
               ['\\xf0\\x9f\\x9a\\xa8','&#128680;'],['\\xc3\\x81','Á'],['\\xc3\\x89','É'],
               ['\\xc3\\x93','Ó'],['\\xe2\\x80\\x99','’'],['\\xe2\\x80\\x98','‘'],['\\xc3\\xa1','á'],
               ['\\xc3\\xa9','é'],['\\xc3\\xa2','â'],['\\xf0\\x9f\\x92\\xa3','&#128163;'],
               ['\\xc3\\xa3','ã'],['\\xc3\\xaa','ê'],['\\xc3\\xb3','ó'],['\\xf0\\x9f\\xa4\\x94','&#129300;'],
               ['\\xf0\\x9f\\x90\\x8d','&#128013;'],['\\xf0\\x9f\\x98\\xa2','&#128546;'],
               ['\\xf0\\x9f\\xa4\\x9d','&#129309;'],['\\xf0\\x9f\\x92\\xa5','&#128165;'],['\\xf0\\x9f\\x93\\x96','&#128214;'],
               ['\\xf0\\x9f\\x98\\xb1','&#128561;'],['\\xc3\\xad','í'],['\\xc3\\x95','Õ'],['\\xc3\\xa7','ç'],
               ['\\xf0\\x9f\\x92\\x8a','&#128138;'],['\\xf0\\x9f\\x98\\xa1','&#128545;'],['\\xc3\\xb5','õ'],
               ['\\xe2\\x9a\\xa0\\xef\\xb8\\x8f','&#9888;'],['\\xf0\\x9f\\x91\\x80','&#128064;'],['\\xc3\\x9a','Ú'],
               ['\\xe2\\x80\\x9c','“'],['\\xe2\\x80\\x9d','”'],['\\xef\\xbf\\xbc','￼'],['\\xe2\\x80\\xa6','...'],['\\xc4\\x81','ã'],
               ['\\xc2\\xa0','&nbsp;'],['\\xc3\\x80','À'],['\\xc3\\x94','Ô'],['\\xc3\\xa0','à'],["\\'", "'"],
               ['\\xc2\\xba','º'],['\\xf0\\x9f\\xa4\\xa3','&#129315;'],['\\xf0\\x9f\\x98\\x82','&#128514;'],
               ['\\xf0\\x9f\\x98\\x8e','&#128526;'],['\\xf0\\x9f\\x91\\x8a\\xf0\\x9f\\x8f\\xbc','&#128074;&#127996;'],
               ['\\xf0\\x9f\\x8f\\x8d\\xef\\xb8\\x8','&#127949;&#65039;'],['\\xf0\\x9f\\x91\\xb6','&#128118;'],
               ['\\xf0\\x9f\\xa7\\x91','&#129489;'],['\\xe2\\x80\\x8d','&zwj;'],['\\xe2\\x9a\\x96\\xef\\xb8\\x8f','&#9878;&#65039;'],
               ['\\xe2\\x9c\\x88\\xef\\xb8\\x8f','&#9992;&#x2708;'],['\\xf0\\x9f\\xa4\\x96','&#129302;'],['\\xf0\\x9f\\x90\\xb6','&#128054;&#x1F436;'],
               ['\\xf0\\x9f\\x95\\xb9\\xef\\xb8\\x8','&#128377;'],['\\xf0\\x9f\\xa4\\xa2','&#129314;'],['\\xf0\\x9f\\x98\\xad','&#128557;'],
               ['\\xe2\\x80\\xbc\\xef\\xb8\\x8f','!!'],['\\xc3\\xba','ú']]
    for codigo in codigos:
        texto = texto.replace(codigo[0],codigo[1])
    return texto

def check_for_udate():
    while True:
        time.sleep(30)
        update_videos_list()