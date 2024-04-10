import json
import os


def get_server_config():
    with open('/Users/apple/Documents/Work/GitRepoLocal/algotradefastapi/trade-apis/config/server.json', 'r') as server:
        jsonServerData = json.load(server)
        return jsonServerData


def get_system_config():
    with open('/Users/apple/Documents/Work/GitRepoLocal/algotradefastapi/trade-apis/config/system.json', 'r') as system:
        jsonSystemData = json.load(system)
        return jsonSystemData


def get_user_config():
    with open('/Users/apple/Documents/Work/GitRepoLocal/algotradefastapi/trade-apis/config/user.json', 'r') as fp:
        json_user_data = json.load(fp)
        return json_user_data
