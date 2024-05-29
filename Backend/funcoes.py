import urllib.request

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
def make_the_video_list_file(lista_de_urls, video_quantity = 0):
    if video_quantity <= 30 and video_quantity > 0:
        open("videos_list.txt","w").close() #Just to clean the file
        for url in lista_de_urls:
            save_page(url)
            with open("videos_list.txt","a") as document:
                for i in range(video_quantity):
                    document.write(list_of_videos("html_page.html")[i]+"\n")


make_the_video_list_file(lista_de_urls,video_quantity=2)