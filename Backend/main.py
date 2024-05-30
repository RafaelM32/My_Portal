from flask import Flask, json, make_response, request
from funcoes import*
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

@app.route("/")
def aplication_status():
    return "Api online"


#This is the core route. Hele i control the functions made in the funcoes.py file
#Here i receve the request from the Frontend and check if the last upload was lass then 10 minutes before
#If so i just send the videos on the videos_list.txt file
#Else, i reload the video_list.txt file befor send a new one.
@app.route("/iframes", methods= ['GET', 'POST'])
def iframes():

    requisicao = request.json
    resposta = {'ok': True, 'iframes_list': []}

    if not is_more_the_x_minutes(10):
        resposta['ok'] = False
        resposta['iframes_list'] = list_of_iframe_videos()
        return make_response(json.jsonify(resposta))
    
    else:
        make_the_video_list_file(requisicao['channels'],requisicao['videos_quantity_peer_channel'])
        resposta['iframes_list'] = list_of_iframe_videos()
        save_time()
        return make_response(json.jsonify(resposta))
