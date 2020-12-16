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

class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email']

    password = forms.CharField()
    repeat_password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['repeat_password'].widget = forms.PasswordInput()


    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        psw = cleaned_data.get('password')
        repeat_psw = cleaned_data.get('repeat_password')

        if repeat_psw != psw:
            msg = "Passwords do not match"
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)

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