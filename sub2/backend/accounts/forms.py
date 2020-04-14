from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')