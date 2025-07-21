from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from players.views import TournamentViewSet, PlayerViewSet
from dj_rest_auth.registration.views import RegisterView


router = routers.DefaultRouter()
router.register(r'torneios', TournamentViewSet, basename='tournament')
router.register(r'players', PlayerViewSet, basename='player')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    
    # Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/cadastro/", RegisterView.as_view(), name="rest_register"),
    # Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]