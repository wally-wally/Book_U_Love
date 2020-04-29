from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .serializers import CustomJWTSerializer
from rest_framework_jwt.views import ObtainJSONWebToken

router = DefaultRouter(trailing_slash=True)
router.register(r"allusers",views.UserViewSet,basename="allusers")

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('auth-login/',ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
    path('user/', views.user),
    path('user/recommend/',views.recommend),
    path('find_password/', views.find_password),
    path('password_update/<int:id>/', views.password_update),
    path('createuser/',views.createuser)
] + router.urls