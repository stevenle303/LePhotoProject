from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder':'Confrim Password'})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)