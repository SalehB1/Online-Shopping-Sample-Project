from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^09\d{9}$',
                                 message="شماره تلفن باید در قالب '09010944090' وارد شود.")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    username_regex = RegexValidator(regex=r'^[\w.+-]*[a-zA-Z][\w.+-]*\Z',
                                    message="نام کاربری باید حداقل یک حرف داشته باشد و @ پذیرفته نمی شود")
    username = models.CharField(max_length=15, unique=True,
                                help_text=_(
                                    'هشدار نام کاربری باید بین 1 تا 15 حرف باشد و (فقط از حروف، اعداد و . / + / - / _ استفاده شود)'),
                                validators=[username_regex],
                                error_messages={'unique': _("کاربری با آن نام کاربری از قبل وجود دارد."), },
                                )
    image = models.ImageField(upload_to="profileImage/", null=True, blank=True)
    is_client = models.BooleanField(default=False, help_text='gdgdfgd')
    is_seller = models.BooleanField(default=False, help_text='gdgdgfg')
    is_verified = models.BooleanField(default=False, help_text='gdgdgfg')
    if phone:

        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = ['username', 'email']
    elif email:
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username', 'phone']
    else:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['phone', 'email']
    objects = CustomUser()

    def __str__(self):
        return f'{self.username}'
