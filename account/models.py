import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=150)
    mobile = models.CharField(_('mobile'), max_length=20, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _("Accounts")
        verbose_name_plural = _("Accounts")

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Address
    """
    # uuid create a random id string, it's hardest to guess and change de url do edit
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), on_delete=models.CASCADE)
    full_name = models.CharField(_('full name'), max_length=150)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    postcode = models.CharField(_('postcode'), max_length=12, blank=True)
    address_line_1 = models.CharField(_('address line one'), max_length=150, blank=True)
    address_line_2 = models.CharField(_('address line two'), max_length=150, blank=True)
    town_city = models.CharField(_('town/city/state'), max_length=150, blank=True)
    country = CountryField()
    delivery_instructions = models.CharField(_("delivery instructions"), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    default = models.BooleanField(_('default'), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return "Address"
