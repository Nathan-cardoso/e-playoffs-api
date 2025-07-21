from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class Player(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True, 
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    twitch = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'pk': self.pk})

class Tournament(models.Model):
    GAME_CHOICES = (
        ('League of Legends', 'League of Legends'),
        ('CS:GO', 'CS:GO'),
        ('Valorant', 'Valorant'),
        ('FIFA', 'FIFA'),
        ('Dragon Ball FighterZ', 'Dragon Ball FighterZ')
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    game = models.CharField(choices=GAME_CHOICES, max_length=100)
    date_start = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_tournaments'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TournamentParticipant',
        related_name='participating_tournaments'
    )
    server_discord = models.URLField(blank=True, null=True)
    public = models.BooleanField(
        default=True,
        help_text='Torneio visível para todos os usuários.'
    )
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )
    
    class Meta:
        ordering = ['-date_start']
        permissions = [
            ('can_manage_tournament', 'Can manage tournament'),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tournament-detail', kwargs={'pk': self.pk})
    
    def is_participant(self, user):
        return self.participants.filter(pk=user.pk).exists()

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='participants_info'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tournament_participations'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('tournament', 'user')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.tournament.name}"