import urllib.request
from datetime import datetime


#This list will be in the main file. It is here now just to test.
lista_de_urls = ["https://www.youtube.com/@rbiana/videos","https://www.youtube.com/@Mamaefalei/videos"]


#This function just save the html data from the new videos page from the channels
#So in order to it work the url HAS TO BE FROM THE VIDEO PAGE of the channel
def save_page(url):
    urllib.request.urlretrieve(url, "html_page.html")


#This function extracts the url from the videos in the page
def list_of_videos(file):
    lista = []
    with open(file, encoding= "utf-8") as page:
        for line in page:
            if "watch?v=" in line:
                lista = line.split("watch?v=")
                lista = lista[1:]
        for i in range(len(lista)):
            lista[i] = "https://www.youtube.com/embed/" + lista[i][:11]
    return lista


#This function save a certain number (video_quantity) of videos in the page (max= 30)
def make_the_video_list_file(video_quantity = 2):
    lista_de_urls = load_channels_list()
    if video_quantity <= 30 and video_quantity > 0:
        open("videos_list.txt","w").close() #Just to clean the file
        for url in lista_de_urls:
            save_page(url)
            with open("videos_list.txt","a") as document:
                for i in range(video_quantity):
                    document.write(list_of_videos("html_page.html")[i]+"\n")
    save_time()



#This function save the actual time. It is to be used to mark the last time the server 
#Make the update from the videos
def save_time():
    now = datetime.now()
    with open("time.txt","w") as time_document:
        time_document.write(str(now.year)+ "\n")
        time_document.write(str(now.month)+ "\n")
        time_document.write(str(now.day)+ "\n")
        time_document.write(str(now.hour)+ "\n")
        time_document.write(str(now.minute))

#This function load the last time saved on the time.txt file and converts it to a list(Y,M,D,H,m)
def load_last_timelist():
    lista = []
    with open("time.txt") as time_document:
        for line in time_document:
            lista.append(int(line))
    return lista

#This function cheks if has bem passed more than x minutes
def is_more_the_x_minutes(x):
    now = datetime.now()
    last_time = load_last_timelist()
    last_time = datetime(last_time[0],last_time[1],last_time[2],last_time[3],last_time[4])
    total_minutes = ((now - last_time).total_seconds())/60
    if total_minutes >= x:
        return True
    else:
        return False


#This function is to load the link of videos saved on videos_list.txt file
def load_videos_list():
    videos_list = []
    with open("videos_list.txt", "r") as videos_document:
        for video in videos_document:
            if video != "": #To dont load the last empit line
                videos_list.append(video.strip())
    return videos_list



#This function cheks is a chennel alrely is in the chennels list
def channel_is_saved(channel):
    with open('channels_list.txt', 'r') as channels_list_doc:
        for ch in channels_list_doc:
            if channel == ch.strip():
                return True
        return False

#This function saves a new chennel in the list
def save_channel(channel):
    if not channel_is_saved(channel):
        with open('channels_list.txt', "a") as channels_list_doc:
            channels_list_doc.write(channel + '\n')
        return f'{channel} foi adicionado com sucesso!'
    else:
        return f'{channel} já consta na lista de canais!'


#This function returns those channels in the channel_list.txt
def load_channels_list():
    channel_list = []
    with open('channels_list.txt', 'r') as channels_list_doc:
        for channel in channels_list_doc:
            if channel != '':
                channel_list.append(channel.strip())
    return channel_list

#This deleletes a channel in the channel_list
def dele_channel(channel):
    if channel_is_saved(channel):
        channel_list = load_channels_list()
        with open('channels_list.txt', 'w') as channel_list_doc:
            for ch in channel_list:
                if ch != channel:
                    channel_list_doc.write(ch + '\n')
        return f'{channel} foi removido com sucesso!'
    else:
        return f'{channel} não está na lista!'