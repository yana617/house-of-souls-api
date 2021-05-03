from django.test import TestCase
from rest_framework import status
from utils.test_utils import HOSAPITestCase
from utils.factories_utils import USER_PASSWORD
from .factories import SuperUserFactory, AdminFactory, UserFactory, VolunteerFactory


class UsersModelTestcase(TestCase):

    def _check_fields(self, user):
        self.assertTrue(user.name)
        self.assertTrue(user.surname)
        self.assertTrue(user.phone)
        self.assertTrue(user.birthday)
        self.assertTrue(user.date_joined)
        self.assertEqual(user.email, None)
        self.assertEqual(user.last_login, None)

    def test_user_factories(self):
        superuser = SuperUserFactory()
        volunteer = VolunteerFactory()
        admin = AdminFactory()
        general_user = UserFactory()

        for user in [superuser, volunteer, admin, general_user]:
            self._check_fields(user)

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertFalse(superuser.is_volunteer)
        self.assertFalse(superuser.is_admin)

        self.assertTrue(volunteer.is_volunteer)
        self.assertFalse(volunteer.is_staff)
        self.assertFalse(volunteer.is_superuser)
        self.assertFalse(volunteer.is_admin)

        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_staff)
        self.assertFalse(admin.is_superuser)
        self.assertFalse(admin.is_volunteer)

        self.assertFalse(user.is_volunteer)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class BaseUsersAPITestCase(HOSAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = SuperUserFactory()
        cls.volunteer = VolunteerFactory()
        cls.admin = AdminFactory()
        cls.general_user = UserFactory()


class UsersAuthAPITestCase(BaseUsersAPITestCase):
    LOGIN_USER_URL = '/api/users/login'
    LOGOUT_USER_URL = '/api/users/logout'

    @staticmethod
    def _get_credentials_data(user):
        return {
            'phone': user.phone,
            'password': USER_PASSWORD
        }

    def test_login_volunteer(self):
        response = self.client.post(self.LOGIN_USER_URL, data=self._get_credentials_data(self.volunteer))
        self.assertStatusCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], self.volunteer.id)
        self.assertTrue(response.data['data']['is_volunteer'])
        self.assertFalse(response.data['data']['is_admin'])
        self.assertIn('last_login', response.data['data'])
        self.assertIn('date_joined', response.data['data'])

    def test_login_admin(self):
        response = self.client.post(self.LOGIN_USER_URL, data=self._get_credentials_data(self.admin))
        self.assertStatusCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], self.admin.id)
        self.assertTrue(response.data['data']['is_admin'])
        self.assertFalse(response.data['data']['is_volunteer'])
        self.assertIn('last_login', response.data['data'])
        self.assertIn('date_joined', response.data['data'])

    def test_login_user(self):
        response = self.client.post(self.LOGIN_USER_URL, data=self._get_credentials_data(self.general_user))
        self.assertStatusCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], self.general_user.id)
        self.assertFalse(response.data['data']['is_admin'])
        self.assertFalse(response.data['data']['is_volunteer'])
        self.assertIn('last_login', response.data['data'])
        self.assertIn('date_joined', response.data['data'])

    def test_logout(self):

        self.login_user(self.general_user)
        response = self.client.post(self.LOGOUT_USER_URL)
        self.assertStatusCode(response, status.HTTP_200_OK)

        self.login_user(self.volunteer)
        response = self.client.post(self.LOGOUT_USER_URL)
        self.assertStatusCode(response, status.HTTP_200_OK)

        self.login_user(self.admin)
        response = self.client.post(self.LOGOUT_USER_URL)
        self.assertStatusCode(response, status.HTTP_200_OK)


class UsersAPITestCase(BaseUsersAPITestCase):
    USERS_URL = '/api/users'

    def _test_list_users(self, user):
        self.login_user(user)
        response = self.client.get(self.USERS_URL)
        self.assertStatusCode(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), len([self.volunteer, self.admin, self.general_user]))
        self.client.logout()

    def test_list_users(self):
        response = self.client.get(self.USERS_URL)
        self.assertStatusCode(response, status.HTTP_403_FORBIDDEN)

        for user in [self.volunteer, self.admin]:
            self._test_list_users(user)

        self.login_user(self.general_user)
        response = self.client.get(self.USERS_URL)
        self.assertStatusCode(response, status.HTTP_403_FORBIDDEN)


class UsersRegisterAPITestCase(BaseUsersAPITestCase):
    REGISTER_USER_URL = '/api/users/register'


class UsersMeAPITestCase(BaseUsersAPITestCase):
    ME_USER_URL = '/api/users/me'

    def _test_get_me(self, user):
        self.login_user(user)
        response = self.client.get(self.ME_USER_URL)
        self.assertStatusCode(response, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], user.id)
        self.assertEqual(response.data['data']['phone'], user.phone)
        self.assertEqual(response.data['data']['birthday'], user.birthday)
        self.assertEqual(response.data['data']['name'], user.name)
        self.assertEqual(response.data['data']['surname'], user.surname)
        self.assertEqual(response.data['data']['is_volunteer'], user.is_volunteer)
        self.assertEqual(response.data['data']['is_admin'], user.is_admin)
        self.assertIn('last_login', response.data['data'])
        self.assertIn('date_joined', response.data['data'])
        self.client.logout()

    def test_get_me(self):
        for user in [self.general_user, self.volunteer, self.admin]:
            self._test_get_me(user)
