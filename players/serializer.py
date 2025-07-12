from rest_framework import serializers
from .models import Tournament, TournamentParticipant

class TournamentParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipant
        fields = ['player', 'joined_at']

class TournamentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'description', 'game', 'date', 'owner', 'participants']
