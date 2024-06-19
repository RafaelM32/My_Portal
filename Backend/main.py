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
    resposta = {'ok': True}

    
    if not is_more_the_x_minutes(10) and not requisicao['refresh'] and not requisicao['change_videos_qtd']: #If did not pass 10 minutes and you dont use the refresh button 
        r = send_videos_list()
        resposta['videos_qtd']  = r['videos_qtd']
        resposta['videos_list'] = r['videos'][::-1]
        resposta['tumb_list']   = r['tumbs'][::-1]
        resposta['tittle_list'] = r['tittles'][::-1]
        return make_response(json.jsonify(resposta))
    
    else:
        #update_videos_qtd(requisicao['videos_quantity_peer_channel'])
        #update_videos_list()
        r = send_videos_list()
        resposta['videos_qtd']  = r['videos_qtd']
        resposta['videos_list'] = r['videos'][::-1]
        resposta['tumb_list']   = r['tumbs'][::-1]
        resposta['tittle_list'] = r['tittles'][::-1]
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
        resposta = {'ok': True, 'status': delete_channel(requisicao['channel'])}
        return make_response(json.jsonify(resposta))
    

    elif request.method == 'GET':
        resposta = {'ok': True, 'chanels_list': load_channels_list_in_database()}
        return make_response(json.jsonify(resposta))


if __name__ == '__main__':
    app.run(debug=True)
