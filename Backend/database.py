from pymongo import MongoClient
from xml.dom import minidom
from bson import ObjectId
from datetime import datetime
import os

cluster = MongoClient(os.environ['MONGODB_URI'])
database = cluster.favyt
channels_collection = database.channels
videos_list = database.videos_list

def save_channel_in_database(channel):
    new_channel = {'channel_url': channel}
    channels_collection.insert_one(new_channel)


def load_channels_list_in_database():
    channel_list = []
    channels = channels_collection.find()   
    for channel in channels:
        channel_list.append(channel['channel_url'])
    return channel_list


def clear_channels_list_in_database():
    channels_collection.delete_many({})


def delete_channel_in_database(channel):
    channels_collection.delete_one({'channel_url': channel})


def channel_is_saved_in_database(channel):
    result = channels_collection.find_one({'channel_url': channel})
    if result == None:
        return False
    return True


def update_channel_videos_list(channel, lista):
    channel_to_update = {'channel_url': channel}
    video_list = {'$set': {'video_list': lista}}
    channels_collection.update_one(channel_to_update, video_list)


def load_channels():
    result = channels_collection.find({})
    for canal in result:
        yield canal

def make_videos_list():
    delete_video_list()
    lista_v = []
    lista_t = []
    qtd = load_video_list()['videos_qtd']
    for canal in load_channels():
        l =  canal['video_list']
        t = canal['tumb_list']
        for i in range(qtd):
            lista_v.append(l[i])
            lista_t.append(t[i])
    update_v = {'$set': {'videos': lista_v}}
    update_t = {'$set': {'tumbs': lista_t}}
    videos_list.update_one({'_id': ObjectId('666a42d5bae506d59146744f')}, update_v)
    videos_list.update_one({'_id': ObjectId('666a42d5bae506d59146744f')}, update_t)
    save_time_in_data_base()

def load_video_list():
    result = videos_list.find_one({'_id': ObjectId('666a42d5bae506d59146744f')})
    return result

def delete_video_list():
    update = {'$set': {'videos': []}}
    videos_list.update_one({'_id': ObjectId('666a42d5bae506d59146744f')}, update)

def save_time_in_data_base():
    update = {'$set': {'time': datetime.now()}}
    videos_list.update_one({'_id': ObjectId('666a42d5bae506d59146744f')}, update)

def update_videos_qtd(qtd:int):
    if qtd < 31 and qtd > -1:
        update = {'$set': {'videos_qtd' : qtd}}
        videos_list.update_one({'_id': ObjectId('666a42d5bae506d59146744f')}, update)
    else: 
        return "qtd has to be a int number between 0 and 30"

def update_channel_tumb_list(channel, tumblist):
    update = {'$set': {'tumb_list': tumblist}}
    channel_to_update = {'channel_url': channel}
    channels_collection.update_one(channel_to_update,update)




    