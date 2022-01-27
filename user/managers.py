from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(BaseUserManager):

    def create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('email must not empty!')
        if not phone:
            raise ValueError('phone must not empty!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff'):
            raise ValueError(_('staff need to be Enabled'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('superuser need to be Enabled'))
        return self.create_user(email, phone, password, **extra_fields)
