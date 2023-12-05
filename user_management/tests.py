from django.http import HttpResponse
from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse
from http import HTTPStatus

from .services import (
    _get_institution_subgroup_pairs_from_eduperson_entitlement,
    delete_institution_for_login_session,
    get_highest_subgroup_of_each_institution_for_logged_in_user,
    get_institution_id_for_login_session,
    get_institution_memberships_of_logged_in_user,
    get_subgroup_id_for_login_session,
    get_user_id_for_login_session,
    remove_login_session_variables,
    set_institution_for_login_session,
)

# Create your tests here.
class AuthViewDecoratorsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def test_login_session_institution_required(self):
        # The view being tested can be any that uses the
        # login_session_institution_required() decorator.
        response = self.client.get(reverse('resource_management:index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        
    def test_institution_ownership_required(self):
        # The views being tested can be any that use the
        # institution_ownership_required() decorator.
        
        # Check GET requests are redirected
        response = self.client.get(reverse('register:organisation'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        
        # Check POST requests are redirected before any processing occurs
        response = self.client.post(reverse('register:organisation'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

class LoginSessionRegressionTestCase(TestCase):
    test_eduperson_entitlement = {
        'urn:mace:egi.eu:group:vo.abc.test.eu:members:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:abc-test:admins:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:abc-test:members:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:abc-test:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:xyz:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:abc:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:abc:members:role=member#aai.egi.eu',
        'urn:mace:egi.eu:group:vo.abc.test.eu:role=member#aai.egi.eu'
    }

    def test_get_user_id_for_login_session(self):
        """
        Returns the user ID from the session.
        """
        test_value = 'user_id'
        session = self.client.session
        session['user_id'] = test_value
        session.save()

        user_id = get_user_id_for_login_session(session)
        self.assertEqual(user_id, test_value)

    def test_get_institution_id_for_login_session(self):
        """
        Returns the institution ID from the
        session.
        """
        test_value = 'institution_id'
        session = self.client.session
        session['institution_for_login_session'] = test_value
        session.save()

        institution_id = get_institution_id_for_login_session(session)
        self.assertEqual(institution_id, test_value)

    def test_get_subgroup_id_for_login_session(self):
        """
        Returns the institution subgroup
        ID from the session.
        """
        test_value = 'subgroup_id'
        session = self.client.session
        session['subgroup_for_login_session'] = test_value
        session.save()

        subgroup_id = get_subgroup_id_for_login_session(session)
        self.assertEqual(subgroup_id, test_value)

    def test_get_institution_memberships_of_logged_in_user(self):
        """
        Returns the institution memberships of the
        logged in user.
        """
        test_value = {
            'institution_123': 'members',
            'institution_456': 'admins',
        }
        session = self.client.session
        session['user_institution_subgroups'] = test_value
        session.save()

        memberships = get_institution_memberships_of_logged_in_user(session)
        self.assertEqual(memberships, test_value)

    def test_get_highest_subgroup_of_each_institution_for_logged_in_user(self):
        """
        Returns the highest authority subgroup
        of each institution that a user is a
        member of.
        """
        test_value = self.test_eduperson_entitlement
        subgroups = get_highest_subgroup_of_each_institution_for_logged_in_user(test_value)
        self.assertEqual(subgroups.get('abc-test'), 'admins')
        self.assertEqual(subgroups.get('abc'), 'members')

    
    def test_set_institution_for_login_session(self):
        """
        Sets the institution ID for the login session.
        """
        test_institution_id = 'institution_id'
        test_subgroup_id = 'subgroup_id'
        session = self.client.session
        set_institution_for_login_session(session, test_institution_id, test_subgroup_id)
        self.assertEqual(get_institution_id_for_login_session(session), test_institution_id)
        self.assertEqual(get_subgroup_id_for_login_session(session), test_subgroup_id)

    def test_delete_institution_for_login_session(self):
        """
        Deletes the institution for the login session.
        """
        test_institution_id = 'institution_id'
        test_subgroup_id = 'subgroup_id'
        session = self.client.session
        set_institution_for_login_session(
            session,
            test_institution_id,
            test_subgroup_id
        )
        self.assertEqual(get_institution_id_for_login_session(session), test_institution_id)
        self.assertEqual(get_subgroup_id_for_login_session(session), test_subgroup_id)
        delete_institution_for_login_session(session)
        self.assertEqual(get_institution_id_for_login_session(session), None)
        self.assertEqual(get_subgroup_id_for_login_session(session), None)

    def test_remove_login_session_variables(self):
        """
        Removes all login-related variables from the
        session.
        """
        test_access_token = 'access_token'
        test_is_logged_in = True
        test_user_institution_subgroups = 'user_institution_subgroups'
        test_user_id = 'user_id'
        test_user_given_name = 'user_given_name'
        test_institution_for_login_session = 'institution_for_login_session'
        test_subgroup_for_login_session = 'subgroup_for_login_session'
        
        session = self.client.session
        # Set the login-related session variables
        session['OIDC_access_token'] = test_access_token
        session['is_logged_in'] = test_is_logged_in
        session['user_institution_subgroups'] = test_user_institution_subgroups
        session['user_id'] = test_user_id
        session['user_given_name'] = test_user_given_name
        session['institution_for_login_session'] = test_institution_for_login_session
        session['subgroup_for_login_session'] = test_subgroup_for_login_session

        # Check that they were set
        self.assertEqual(session.get('OIDC_access_token'), test_access_token)
        self.assertEqual(session.get('is_logged_in'), test_is_logged_in)
        self.assertEqual(get_institution_memberships_of_logged_in_user(session), test_user_institution_subgroups)
        self.assertEqual(get_user_id_for_login_session(session), test_user_id)
        self.assertEqual(session.get('user_given_name'), test_user_given_name)
        self.assertEqual(get_institution_id_for_login_session(session), test_institution_for_login_session)
        self.assertEqual(get_subgroup_id_for_login_session(session), test_subgroup_for_login_session)

        # Check that they were removed
        remove_login_session_variables(session)

        self.assertEqual(session.get('OIDC_access_token'), None)
        self.assertEqual(session.get('is_logged_in'), None)
        self.assertEqual(get_institution_memberships_of_logged_in_user(session), None)
        self.assertEqual(get_user_id_for_login_session(session), None)
        self.assertEqual(session.get('user_given_name'), None)
        self.assertEqual(get_institution_id_for_login_session(session), None)
        self.assertEqual(get_subgroup_id_for_login_session(session), None)

    def test_get_institution_subgroup_pairs_from_eduperson_entitlement(self):
        """
        Returns institutions with subgroups from
        an eduperson_entitlement dict.
        """
        institution_subgroup_pairs = _get_institution_subgroup_pairs_from_eduperson_entitlement(self.test_eduperson_entitlement)
        print('institution_subgroup_pairs', institution_subgroup_pairs)
        self.assertTrue('abc-test:admins' in institution_subgroup_pairs)
        self.assertTrue('abc-test:members' in institution_subgroup_pairs)
        self.assertTrue('abc:members' in institution_subgroup_pairs)
        self.assertTrue('abc-test' not in institution_subgroup_pairs)
        self.assertTrue('abc' not in institution_subgroup_pairs)
        self.assertTrue('xyz' not in institution_subgroup_pairs)