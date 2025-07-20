from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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

class Tournament(models.Model):

    GAME_CHOICES = (
        ('League of Legends', 'League of Legends'),
        ('CS:GO', 'CS:GO'),
        ('Valorant', 'Valorant'),
        ('FIFA', 'FIFA'),
        ('Dragon Ball FighterZ', 'Dragon Ball FighterZ')
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    game = models.CharField(
        choices=GAME_CHOICES,
        max_length=100
    )

    date_start = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='torneios_owned'
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TournamentParticipant',
        related_name='tournaments_participated'
    )

    server_discord = models.URLField(
        blank=True,
        null=True,
        default=None,
    )

    public = models.BooleanField(
        default=True,
        help_text='Torneio visível para todos os usuários.'
    )

    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )


    def __str__(self):
        return self.name

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE
    )

    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('tournament', 'player')
