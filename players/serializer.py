from rest_framework import serializers
from .models import Tournament, TournamentParticipant, Player
from django.urls import reverse

class PlayerShortSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = ['id', 'username', 'profile_image_url']
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

class TournamentParticipantSerializer(serializers.ModelSerializer):
    user = PlayerShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), 
        source='user',
        write_only=True
    )
    
    class Meta:
        model = TournamentParticipant
        fields = ['id', 'user', 'user_id', 'joined_at', 'tournament']
        read_only_fields = ['joined_at', 'tournament']

class TournamentListSerializer(serializers.ModelSerializer):
    owner = PlayerShortSerializer(read_only=True)
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)
    detail_url = serializers.SerializerMethodField()
    game_display = serializers.CharField(source='get_game_display', read_only=True)
    
    class Meta:
        model = Tournament
        fields = [
            'id', 'name', 'game', 'game_display', 'date_start', 
            'owner', 'participants_count', 'public', 'value', 'detail_url'
        ]

    def get_detail_url(self, obj):
        return reverse('tournament-detail', kwargs={'pk': obj.pk})

class TournamentDetailSerializer(serializers.ModelSerializer):
    owner = PlayerShortSerializer(read_only=True)
    participants_info = TournamentParticipantSerializer(many=True, read_only=True)  # ✅ Correto agora
    is_owner = serializers.SerializerMethodField()
    is_participant = serializers.SerializerMethodField()
    game_display = serializers.CharField(source='get_game_display', read_only=True)
    
    class Meta:
        model = Tournament
        fields = '__all__'
        read_only_fields = ['created_at', 'owner', 'participants_info']
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.owner
    
    def get_is_participant(self, obj):
        request = self.context.get('request')
        return request and obj.participants.filter(id=request.user.id).exists()


class PlayerSerializer(serializers.ModelSerializer):
    owned_tournaments_count = serializers.IntegerField(source='owned_tournaments.count', read_only=True)
    participating_tournaments_count = serializers.IntegerField(source='participating_tournaments.count', read_only=True)
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'username', 'email', 'profile_image', 'profile_image_url',
            'first_name', 'last_name', 'date_joined', 
            'owned_tournaments_count', 'participating_tournaments_count'
        ]
        extra_kwargs = {
            'profile_image': {'write_only': True}
        }
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

class PlayerDetailSerializer(serializers.ModelSerializer):
    owned_tournaments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='tournament-detail',
        source='owned_tournaments'
    )
    participating_tournaments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='tournament-detail',
        source='participating_tournaments'
    )
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'profile_image', 'profile_image_url', 'bio',
            'instagram', 'x', 'youtube', 'twitch',
            'date_joined', 'owned_tournaments', 'participating_tournaments'
        ]
        extra_kwargs = {
            'profile_image': {'write_only': True}
        }
    
    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None