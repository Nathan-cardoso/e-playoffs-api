from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from players.views import TournamentViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from dj_rest_auth.registration.views import (
    RegisterView, VerifyEmailView, ResendEmailVerificationView
)
# from dj_rest_auth.views import (
#     LoginView, LogoutView, UserDetailsView,
#     PasswordResetView, PasswordResetConfirmView
# )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()

router.register(r'torneios', TournamentViewSet, basename='tournament')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Rotas da API
    path('api/v1/', include(router.urls)),
    #Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cadastro/', RegisterView.as_view(), name='rest_register'),
    # Docs 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
