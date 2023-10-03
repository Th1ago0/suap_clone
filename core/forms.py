from django import forms

class LoginForm(forms.Form):
    user_code = forms.CharField(widget=forms.TextInput(
            attrs={
                'name':'user_code',
                'id':'user_code',
    }), max_length=14)
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                'name':'password',
                'id':'password',
    }), max_length=64)