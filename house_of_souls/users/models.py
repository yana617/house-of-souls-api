from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from typing import List


VOLUNTEER_ROLE = 'Volunteer'
HOS_ADMIN_ROLE = 'HOS_admin'
GENERAL_USER_ROLE = 'User'
DEV_ADMIN_ROLE = 'Dev_admin'


class UserManager(BaseUserManager):

    def _create_user(self, phone_number, password, **extra_fields):

        if 'email' in extra_fields:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(phone=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)

    def create_hos_administrator(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(_('name'), max_length=30, blank=False)
    surname = models.CharField(_('surname'), max_length=30, blank=False)
    phone = PhoneNumberField(blank=False, null=False, max_length=13, unique=True)
    birthday = models.DateField(blank=False, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email = models.EmailField(_('email address'), blank=True, unique=True, null=True)

    objects = UserManager()

    is_volunteer = models.BooleanField(
        _('is_volunteer'),
        default=False,
        help_text=_('Designates whether the user can claim on schedule.'),
    )
    is_admin = models.BooleanField(
        _('is_admin'),
        default=False,
        help_text=_('Designates whether the user can manage volunteers.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'

    @property
    def role_str(self) -> List[str]:
        roles = {
            VOLUNTEER_ROLE: self.is_volunteer,
            HOS_ADMIN_ROLE: self.is_admin,
            DEV_ADMIN_ROLE: self.is_staff,
        }
        role = list(filter(lambda x: roles[x], roles))
        if not role:
            role = [GENERAL_USER_ROLE]
        return ', '.join(role)

    def __str__(self):
        return f'{self.role_str}: {self.name} {self.surname} {self.phone}'

    def __repr__(self):
        return self.self()
