from django import forms
from .models import User
from .models import TodoTask

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


from django import forms


class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['title', 'completed']
