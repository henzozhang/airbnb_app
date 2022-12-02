from django.contrib.auth.forms import UserCreationForm
from . import models

class UserCreationFormCustom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ['username', 'email']