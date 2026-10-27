from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse
from http import HTTPStatus

from .services import (
    clear_user_data_from_session,
    delete_institution_for_login_session,
    get_institution_id_for_login_session,
    get_institution_memberships_of_logged_in_user,
    get_subgroup_id_for_login_session,
    get_user_id_for_login_session,
    parse_eduperson_entitlement,
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
    class DummyRequest:
        session: SessionStore

    def eduperson_entitlement_test_data(self) -> dict:
        return {
            'urn:mace:egi.eu:group:vo.abc.test.eu:members:role=member#aai.egi.eu',
            'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:institution-1:admins:role=member#aai.egi.eu',
            'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:institution-1:members:role=member#aai.egi.eu',
            'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:institution-2:members:role=member#aai.egi.eu',
            'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:incomplete-membership-declaration:role=member#aai.egi.eu',
            'urn:mace:egi.eu:group:vo.abc.test.eu:organizations:role=member#aai.egi.eu',
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

    def test_clear_user_data_from_session(self):
        """Clears all user data from the current session and preserves session
        data used for search by content functionalities.
        """
        test_session_data = {
            'OIDC_access_token': 'access_token',
            'user_institution_subgroups': 'user_institution_subgroups',
            'user_id': 'user_id',
            'user_given_name': 'user_given_name',
            'institution_for_login_session': 'institution_for_login_session',
            'subgroup_for_login_session': 'subgroup_for_login_session',
            'data_collection_search': 'data_collection_search',
            'static_dataset_search': 'static_dataset_search',
            'workflow_search': 'workflow_search',
            'simple_search': 'simple_search',
        }

        # SessionStore is created every time self.client.session is called,
        # so needs to be stored in a variable.
        session = self.client.session
        session.update(test_session_data)
        request = self.DummyRequest()
        request.session = session

        # Check session data was set
        self.assertEqual(
            request.session.get('OIDC_access_token'),
            test_session_data.get('OIDC_access_token')
        )
        self.assertEqual(
            get_institution_memberships_of_logged_in_user(request.session),
            test_session_data.get('user_institution_subgroups')
        )
        self.assertEqual(
            get_user_id_for_login_session(request.session),
            test_session_data.get('user_id')
        )
        self.assertEqual(
            request.session.get('user_given_name'),
            test_session_data.get('user_given_name')
        )
        self.assertEqual(
            get_institution_id_for_login_session(request.session),
            test_session_data.get('institution_for_login_session')
        )
        self.assertEqual(
            get_subgroup_id_for_login_session(request.session),
            test_session_data.get('subgroup_for_login_session')
        )
        self.assertEqual(
            request.session.get('data_collection_search'),
            test_session_data.get('data_collection_search')
        )
        self.assertEqual(
            request.session.get('static_dataset_search'),
            test_session_data.get('static_dataset_search')
        )
        self.assertEqual(
            request.session.get('workflow_search'),
            test_session_data.get('workflow_search')
        )
        self.assertEqual(
            request.session.get('simple_search'),
            test_session_data.get('simple_search')
        )

        clear_user_data_from_session(request)

        # Check that only user session was cleared
        self.assertEqual(request.session.get('OIDC_access_token'), None)
        self.assertEqual(get_institution_memberships_of_logged_in_user(request.session), None)
        self.assertEqual(get_user_id_for_login_session(request.session), None)
        self.assertEqual(request.session.get('user_given_name'), None)
        self.assertEqual(get_institution_id_for_login_session(request.session), None)
        self.assertEqual(get_subgroup_id_for_login_session(request.session), None)
        self.assertIn('data_collection_search', request.session)
        self.assertIn('static_dataset_search', request.session)
        self.assertIn('workflow_search', request.session)
        self.assertIn('simple_search', request.session)

    def test_parse_eduperson_entitlement(self):
        """Returns institutions with subgroups from an eduperson_entitlement dict.
        """
        unsorted_entitlement_data = parse_eduperson_entitlement(
            self.eduperson_entitlement_test_data()
        )
        # Sort to reliably check test results.
        entitlement_data = {
            key: unsorted_entitlement_data.get(key)
            for key in sorted(unsorted_entitlement_data.keys())
        }
        print('entitlement_data', entitlement_data)
        self.assertIn('institution-1', entitlement_data)
        self.assertEqual(entitlement_data.get('institution-1'), 'admins')
        self.assertIn('institution-2', entitlement_data)
        self.assertEqual(entitlement_data.get('institution-2'), 'members')
        self.assertNotIn('incomplete-membership-declaration', entitlement_data)
        self.assertDictEqual(entitlement_data, {
            'institution-1': 'admins',
            'institution-2': 'members',
        })