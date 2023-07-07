import json
import requests
from urllib.parse import unquote

# Used in the main menu. Used as the base link for creating new institutions.
CREATION_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizations:'
# Used in institutions list page. Used as the base link for joining organisations.
# E.g., JOIN_URL_BASE + "<institution_name>"
JOIN_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizationRequests:'


def get_user_info(access_token):
    """
    Contacts the EGI Check-in UserInfo API to retrieve
    the logged in user's details - e.g., which
    institution they are a part of, ID, etc.
    """
    url = 'https://aai-demo.egi.eu/auth/realms/egi/protocol/openid-connect/userinfo'
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer' + ' ' + access_token
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def get_institution_subgroups_of_logged_in_user(request):
    eduperson_entitlement = request.session.get('eduperson_entitlement')

    # Find all groups that are a part of
    # the 'organizations' parent group.
    organisations = []
    for s in eduperson_entitlement:
        index = s.rfind('organizations', 0, -1)
        if index == -1:
            # The 'organizations' group is not mentioned.
            continue

        index1 = s.rfind('role', 0, -1)
        new_string = s[index: index1 - 1]
        if len(new_string) <= len('organizations'):
            # No subgroup of 'organizations' found, just
            # the string for the 'organizations' group
            # itself.
            continue

        index2 = new_string.find(':', 0, -1)
        organisations.append(new_string[index2 + 1:])
    
    # Find the subgroups
    subgroups = []
    for o in organisations:
        index = o.find(':')
        if index == -1:
            continue
        subgroups.append(unquote(o[:]))
    return subgroups

# Login session management
def remove_login_session_variables(request):
    if 'is_logged_in' in request.session:
        del request.session['is_logged_in']
    if 'eduperson_entitlement' in request.session:
        del request.session['eduperson_entitlement']
    if 'email' in request.session:
        del request.session['email']
    if 'institution_for_login_session' in request.session:
        del request.session['institution_for_login_session']
    if 'subgroup_for_login_session' in request.session:
        del request.session['subgroup_for_login_session']

def get_institution_id_of_logged_in_user(request):
    return request.session.get('institution_for_login_session')

def get_subgroup_of_logged_in_user(request):
    return request.session.get('subgroup_for_login_session')

def get_logged_in_user_id(request):
    return request.session.get('email')