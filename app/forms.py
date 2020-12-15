from django import forms
from app.models import Question, UserProfile, Answer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class EditProfileForm(forms.ModelForm):
	avatar = forms.ImageField()

	class Meta:
		model = UserProfile
		fields = ['username', 'email', 'avatar']

	def save(self, *args, **kwargs):
		user = super().save(*args, **kwargs)
		user.avatar = self.cleaned_data['avatar']
		user.save()
		return user

class CreateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget = forms.PasswordInput()

		
class CreateProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['avatar']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput())

class AskForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text']