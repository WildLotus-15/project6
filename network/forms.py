from django import forms
from .models import UserProfile

class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(EditProfileForm, self).__init__(*args, **kwargs)
            self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Name' }

            self.fields['bio'].widget.attrs = {'class': 'form-control', 'placeholder': 'Bio'}

            self.fields['picture'].widget.attrs = {'class': 'form-control'}
        
    class Meta:
        model = UserProfile
        fields = ["name", "bio", 'picture']