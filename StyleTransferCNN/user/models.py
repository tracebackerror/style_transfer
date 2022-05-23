from django.db import models
from django.contrib.auth.models import User

class SetupForgotPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    transformed1 = models.ImageField(upload_to='transformed_images/')
    transformed2 = models.ImageField(upload_to='transformed_images/')
    transformed3 = models.ImageField(upload_to='transformed_images/')

    def __str__(self):
        return f"{self.user.username}"