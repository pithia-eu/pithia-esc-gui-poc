import json
import requests

BASE_URL = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizations:'
organization_creation_url = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizationRequests'

def list_groups(file):
    f = open(file)
    # The json. load() is used to read the JSON document from file
    groups = json.load(f)
    f.close()

    return groups

def get_user_info(url, access_token):
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer' + ' ' + access_token
    }

    return requests.get(url, headers=headers)
