from django.forms import ModelForm
from .models import Post, UserProfile


class NewPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': "What's on your mind?"}
        self.fields['description'].label = ''

    class Meta:
        model = Post
        fields = ["description"]


class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio"]
        