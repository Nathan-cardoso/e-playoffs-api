from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tournament, TournamentParticipant, Player
from .serializer import TournamentSerializer, PlayerSerializer
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny, IsAuthenticated

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path=('inscrever'))
    def inscrever(self, request, pk=None):
        tournament = self.get_object()
        player = request.user

        if TournamentParticipant.objects.filter(tournament=tournament, player=player).exists():
            return Response({'detail': 'Você já está participando deste torneio.'}, status=400)

        TournamentParticipant.objects.create(tournament=tournament, player=player)
        return Response({'detail': 'Participação confirmada com sucesso!'})


class TournamentParticipantViewSet(viewsets.ModelViewSet):
    queryset = TournamentParticipant.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(player=self.request.user)
    

class PLayerHomeViewSet(viewsets.ViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
