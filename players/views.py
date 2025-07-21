from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Tournament, TournamentParticipant, Player
from .serializer import (
    TournamentListSerializer,
    TournamentDetailSerializer,
    TournamentParticipantSerializer,
    PlayerSerializer,
    PlayerDetailSerializer
)

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all().order_by('-date_start')
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TournamentListSerializer
        return TournamentDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro para torneios públicos ou do usuário
        if not self.request.user.is_staff:
            queryset = queryset.filter(public=True) | queryset.filter(owner=self.request.user)
        
        # Filtro por jogo
        game = self.request.query_params.get('game')
        if game:
            queryset = queryset.filter(game=game)
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='join')
    def join_tournament(self, request, pk=None):
        tournament = self.get_object()
        player = request.user
        
        if tournament.owner == player:
            return Response(
                {'detail': 'Você é o dono deste torneio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if TournamentParticipant.objects.filter(tournament=tournament, user=player).exists():
            return Response(
                {'detail': 'Você já está participando deste torneio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        TournamentParticipant.objects.create(tournament=tournament, user=player)
        return Response(
            {'detail': 'Participação confirmada com sucesso!'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='leave')
    def leave_tournament(self, request, pk=None):
        tournament = self.get_object()
        participant = get_object_or_404(
            TournamentParticipant,
            tournament=tournament,
            player=request.user
        )
        participant.delete()
        return Response(
            {'detail': 'Você saiu do torneio com sucesso.'},
            status=status.HTTP_200_OK
        )
    
    

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(pk=self.request.user.pk)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)