from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
