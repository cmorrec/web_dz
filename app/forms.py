from django import forms
from app.models import Question, UserProfile, Answer
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['username', 'email', 'avatar']

class CreateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget = forms.PasswordInput()

	def is_valid(self):
		return True
		
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