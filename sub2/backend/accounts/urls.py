from . import views
from django.urls import path
from .serializers import CustomJWTSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('auth-login/',ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
]