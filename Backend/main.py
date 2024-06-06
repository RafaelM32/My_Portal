from flask import Flask, json, make_response, request
from funcoes import*
from flask_cors import CORS



app = Flask(__name__)
CORS(app, origins=['https://favyt.netlify.app'])

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

    
    if not is_more_the_x_minutes(10) and not requisicao['refresh']: #If did not pass 10 minutes and you dont use the refresh button 
        resposta['videos_list'] = send_videos_list(requisicao['videos_quantity_peer_channel'])                #the api will onli retunr the videos list. Instead of reload the list
        return make_response(json.jsonify(resposta))
    
    else:
        upload_videos_list()
        resposta['videos_list'] = send_videos_list(requisicao['videos_quantity_peer_channel'])
        return make_response(json.jsonify(resposta))



#In this route i can modify the list of channels that i want to load
#I can get the list or add a new channel or even delete some one
@app.route('/channel_list', methods= ['GET', 'POST','DELETE'])
def channel_list():

    if request.method == 'POST':
        requisicao = request.json
        resposta = {'ok': True, 'status': save_channel(requisicao['channel'])}
        return make_response(json.jsonify(resposta))
    

    elif request.method =='DELETE':
        requisicao = request.json
        resposta = {'ok': True, 'status': dele_channel(requisicao['channel'])}
        return make_response(json.jsonify(resposta))
    

    elif request.method == 'GET':
        resposta = {'ok': True, 'chanels_list': load_channels_list()}
        return make_response(json.jsonify(resposta))


if __name__ == '__main__':
    app.run(debug=True)
