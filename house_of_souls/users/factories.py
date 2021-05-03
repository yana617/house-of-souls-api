from functools import partial

import factory

from django.contrib.auth import get_user_model
from utils import factories_utils


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    phone = factory.Sequence(lambda n: '+37529296%04d' % n)
    birthday = factory.Faker('date')
    password = factory.Faker('password')


class UserFactory(BaseUserFactory):
    password = factory.PostGenerationMethodCall('set_password', factories_utils.USER_PASSWORD)


class VolunteerFactory(UserFactory):
    is_volunteer = True


class AdminFactory(UserFactory):
    is_admin = True


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


BaseUserDictFactory = partial(factories_utils.dict_factory, BaseUserFactory)
