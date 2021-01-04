
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(_('name'), max_length=30, blank=False)
    surname = models.CharField(_('surname'), max_length=30, blank=False)
    phone = models.CharField(blank=False, null=True, max_length=13, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email = models.EmailField(_('email address'), blank=True, unique=True)

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
