from django.db import models
from hashlib import md5
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MtlPyUser(AbstractUser):
    @property
    def email_hash(self):
        return md5(self.email).hexdigest()
    

    @property
    def full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)
