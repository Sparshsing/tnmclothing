from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    storeName = models.CharField(max_length=50, unique=True)
    storeCode = models.CharField(max_length=4, primary_key=True)
    user = models.ForeignKey(User, related_name='store', null=True, on_delete=models.SET_NULL)
    emailAddress = models.EmailField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipCode = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)])

    @property
    def userFullName(self):
        if self.user:
            return str(self.user.last_name + " " + self.user.first_name)
        else:
            return str('')

    def __str__(self):
        return self.storeName
