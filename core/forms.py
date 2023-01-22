from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=255, required=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2',]
		help_texts = {
			'username': '',
			'email': '',
			'password1': '',
			'password2': '',
		}

class UpdateProfile(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'pfp']

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['image','caption']