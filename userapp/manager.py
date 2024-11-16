from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

class CustomerManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)

        from .models import Country
        cname = extra_fields.pop('cname', None)
        if cname:
            try:
                extra_fields['cname'] = Country.objects.get(cname=cname)
            except ObjectDoesNotExist:
                raise ValueError(f'Country with cname "{cname}" does not exist.')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)
