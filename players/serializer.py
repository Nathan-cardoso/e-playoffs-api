from rest_framework import serializers
from .models import Tournament, TournamentParticipant, Player

class TournamentParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipant
        fields = ['player', 'joined_at']

class TournamentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'description', 'game','value', 'date_start', 'owner', 'participants']


class TournamentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    participants = TournamentParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'email', 'profile_image']
