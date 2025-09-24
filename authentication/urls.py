from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/v1/authentication/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authentication/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authentication/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

#Como estamos criando acessos via API, o ideal é isolar os acessos par obtenção dos tokens, desta maneira
#criamos um app authentication, e nele estamos criando as urls de autenticação, para que só quem estiver
#autenticado, é que poderá acessar as API's. Também é necessário em settings, configurar/incluir 
#estas urls, assim como fazemos com as app normalmente