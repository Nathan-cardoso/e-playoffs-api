from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):

    email = models.EmailField(
        unique=True,
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True, null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    instagram = models.URLField(
        blank=True,
        null=True,
        default=None
    )

    x = models.URLField(
        blank=True,
        null=True,
        default=None
    )

    youtube = models.URLField(
        blank=True,
        null=True,
        default=None
    )

    twitch = models.URLField(
        blank=True,
        null=True, 
        default=None
    )
