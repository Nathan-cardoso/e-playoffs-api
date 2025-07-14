from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tournament, TournamentParticipant
from .serializer import TournamentSerializer
from django.conf import settings
from django.http import HttpResponseRedirect

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        tournament = self.get_object()
        player = request.user

        if TournamentParticipant.objects.filter(tournament=tournament, player=player).exists():
            return Response({'detail': 'Você já está participando deste torneio.'}, status=400)

        TournamentParticipant.objects.create(tournament=tournament, player=player)
        return Response({'detail': 'Participação confirmada com sucesso!'})
