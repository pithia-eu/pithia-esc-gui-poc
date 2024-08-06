import json
import logging
import os
import re
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from urllib.parse import unquote

from pithiaesc.settings import BASE_DIR

# Used in the main menu. Used as the base link for creating new institutions.
CREATION_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizationRequests'
# Used in institutions list page. Used as the base link for joining organisations.
# E.g., JOIN_URL_BASE + "<institution_name>"
JOIN_URL_BASE = 'https://perun.egi.eu/egi/registrar/?vo=vo.esc.pithia.eu&group=organizations:'


logger = logging.getLogger(__name__)


def get_user_info(access_token):
    """Contacts the EGI Check-in UserInfo API to retrieve
    the logged in user's details - e.g., which institution
    they are a part of, ID, etc.
    """
    response_text = None
    try:
        url = 'https://aai.egi.eu/auth/realms/egi/protocol/openid-connect/userinfo'
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer' + ' ' + access_token
        }
        response = requests.get(url, headers=headers)
        response_text = response.text
        return json.loads(response_text)
    except json.decoder.JSONDecodeError:
        logger.exception(f'Could not decode user info: "{response_text}"')
        return {'error': 'An error occurred whilst trying to decode the User Info API response.'}

def _get_institution_subgroup_pairs_from_eduperson_entitlement(eduperson_entitlement):
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

def _is_highest_inst_subgroup_pair_in_inst_subgroup_pair_dict(
        institution_name,
        subgroup_name,
        subgroups_by_institution_dict):
    if (subgroup_name == 'admins'):
        return False
    elif (institution_name not in subgroups_by_institution_dict):
        return False
    else:
        return True


def get_highest_subgroup_of_each_institution_for_logged_in_user(eduperson_entitlement):
    institution_subgroup_pairs = _get_institution_subgroup_pairs_from_eduperson_entitlement(eduperson_entitlement)
    subgroups_by_institution = {}
    for isgp in institution_subgroup_pairs:
        isgp_split = isgp.split(':')
        institution_name = isgp_split[0]
        subgroup_name = isgp_split[1]
        if (_is_highest_inst_subgroup_pair_in_inst_subgroup_pair_dict(
            institution_name,
            subgroup_name,
            subgroups_by_institution)):
            continue
        subgroups_by_institution[institution_name] = subgroup_name
        
    return subgroups_by_institution

# Login session management
def delete_institution_for_login_session(session):
    session.pop('institution_for_login_session', None)
    session.pop('subgroup_for_login_session', None)

def remove_login_session_variables(session):
    session.pop('OIDC_access_token', None)
    session.pop('is_logged_in', None)
    session.pop('user_institution_subgroups', None)
    session.pop('user_id', None)
    session.pop('user_given_name', None)
    delete_institution_for_login_session(session)

def get_user_id_for_login_session(session):
    return session.get('user_id')

def get_institution_id_for_login_session(session):
    return session.get('institution_for_login_session')

def get_subgroup_id_for_login_session(session):
    return session.get('subgroup_for_login_session')

def get_institution_memberships_of_logged_in_user(session):
    return session.get('user_institution_subgroups')

def set_institution_for_login_session(session, institution, subgroup):
    session['institution_for_login_session'] = institution
    session['subgroup_for_login_session'] = subgroup

def remove_login_session_variables_and_redirect_user_to_logout_page(request):
    remove_login_session_variables(request.session)
    absolute_home_page_uri = re.sub(r'^http\b', 'https', request.build_absolute_uri(reverse("home")))
    return HttpResponseRedirect(f'/authorised/?{urlencode({"logout": absolute_home_page_uri})}')

# Templates
def get_members_by_institution_id(institution_id):
    members = []
    perun_data = None
    try:
        with open(os.path.join(BASE_DIR, 'perun', 'ListOfOrganisations.json')) as organisation_list_file:
            perun_data = json.loads(organisation_list_file.read())
    except FileNotFoundError:
        return members
    
    try:
        institutions = perun_data.get('organizations')
        # Gets the first institution if there is one,
        # else, returns None
        institution = next(iter([i for i in institutions if i.get('name') == institution_id]), None)
        member_ids = institution.get('members')
        for u in perun_data.get('users'):
            uid = u.get('edu_person_unique_id')
            if uid in member_ids:
                members.append(u)
    except AttributeError:
        # Something is wrong here, as it means
        # that the institution cannot be found.
        pass

    return members
