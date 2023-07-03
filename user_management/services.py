import json
import requests

# Used in the main menu. Used as the base link for creating new institutions.
PERUN_INSTITUTION_CREATION_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizations:'
# Used in institutions list page. Used as the base link for joining organisations.
# E.g., PERUN_INSTITUTION_JOIN_URL_BASE + "<institution_name>"
PERUN_INSTITUTION_JOIN_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizationRequests'

def list_groups(file):
    f = open(file)
    # The json.load() is used to read the JSON document from file
    groups = json.load(f)
    f.close()

    return groups

def get_user_info(url, access_token):
    """
    Contacts the EGI Check-in UserInfo API to retrieve
    the logged in user's details - e.g., which
    institution they are a part of, ID, etc.
    """
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer' + ' ' + access_token
    }

    return requests.get(url, headers=headers)
