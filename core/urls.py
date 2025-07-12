from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework import routers
from players.views import TournamentViewSet

router = routers.DefaultRouter()

router.register(r'torneios', TournamentViewSet, basename='tournament')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="rest_register"),
    path("api/auth/login/", LoginView.as_view(), name="rest_login"),
    path("api/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
