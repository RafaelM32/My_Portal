from flask import Flask, json, make_response, request
from funcoes import*
from flask_cors import CORS



app = Flask(__name__)
CORS(app,origins=['https://favytlogin.netlify.app'],expose_headers=['Access-Control-Allow-Origin'],supports_credentials=True)

@app.route("/")
def aplication_status():
    return "Api online"


#This is the core route. Hele i control the functions made in the funcoes.py file
#Here i receve the request from the Frontend and check if the last upload was lass then 10 minutes before
#If so i just send the videos on the videos_list.txt file
#Else, i reload the video_list.txt file befor send a new one.
#test
@app.route("/iframes", methods= ['GET', 'POST'])
def iframes():

    requisicao = request.json
    resposta = {'ok': True}
    
    if requisicao['refresh']:
        update_videos_qtd(requisicao['videos_quantity_peer_channel'])
        update_videos_list(requisicao['videos_quantity_peer_channel'])
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
        cookie = request.cookies.get('session_token')
        ip_requisicao = request.remote_addr
        if cookie != None:
            if is_valid_token(cookie, ip_requisicao):
                resposta = {'ok': True, 'chanels_list': load_channels_list_in_database(), 'qtd': load_video_list()['videos_qtd'], 'cookie': cookie}
            else:
                resposta = {'ok': False}
        else:
            resposta = {'ok': False}
        return make_response(json.jsonify(resposta))

@app.route('/videos', methods=['POST'])
def videos():
    requisicao = request.json
    resposta = list_of_videos_and_images(requisicao['channel'])
    return resposta

@app.route('/qtd', methods=['POST'])
def update_qtd():
    requisicao = request.json
    update_videos_qtd(requisicao['new_qtd'])
    return make_response(json.jsonify({'ok': True}))

@app.route('/login', methods=['POST'])
def login():
    requisicao = request.json
    ip_requisicao = request.remote_addr
    is_saved, userID = is_user_saved(requisicao['username'],requisicao['password'])
    if is_saved:
        token_session = generate_token_session(requisicao['username'],ip_requisicao)
        if not is_valid_token(token_session, ip_requisicao, requisicao['username']):
            save_token_session(token_session, userID)
        resposta = make_response(json.jsonify({'valid_login': True}))
        resposta.set_cookie('session_token', value = token_session, samesite='None',httponly=True,secure=True)
        return resposta

    resposta = make_response(json.jsonify({'valid_login': False, 'status': 'Invalid Credentials'}))
    return resposta

if __name__ == '__main__':
    app.run()
