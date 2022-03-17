from django.forms import ModelForm
from .models import UserProfile

class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "picture"]
