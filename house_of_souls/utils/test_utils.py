from rest_framework.test import APITestCase

from users.factories import UserFactory, VolunteerFactory, AdminFactory, SuperUserFactory
from .factories_utils import USER_PASSWORD


class HOSAPITestCase(APITestCase):

    def create_superuser(self):
        self.super_user = SuperUserFactory()

    def login_user(self, user):
        return self.client.login(phone=user.phone, password=USER_PASSWORD)

    def create_volunteers(self, count):
        return [VolunteerFactory() for _ in range(count)]

    def create_admins(self, count):
        return [AdminFactory() for _ in range(count)]

    def create_users(self, count):
        return [UserFactory() for _ in range(count)]

    def assertStatusCode(self, response, status):
        self.assertIsNotNone(response)

        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            content = '<not printable {} bytes>'.format(len(response.content))

        self.assertEqual(
            response.status_code,
            status,
            msg='{} != {} with response data {}'.format(
                response.status_code,
                status,
                content
            )
        )

    def assertDictsEqual(self, request_dict, response_dict):   # TODO check biectively
        for k, v in request_dict.items():
            self.assertEqual(
                response_dict[k],
                v,
                msg='{} is from request. {} is from response. Key is {}'.format(
                    v, response_dict[k], k
                )
            )

    def assertListsOfDictsEqual(self, request_list, reponse_list, sort_by=''):
        sorted_request = sorted(request_list, key=lambda k: k[sort_by])
        sorted_response = sorted(reponse_list, key=lambda k: k[sort_by])

        for index, item in enumerate(sorted_request):
            self.assertDictsEqual(sorted_response[index], item)

    def assertDictsNotEqual(self, request_dict, response_dict):
        for k, v in request_dict.items():
            self.assertNotEqual(
                response_dict[k],
                v,
                msg='{} is from request. {} is from response. Key is {}'.format(
                    v, response_dict[k], k
                )
            )
