from django import forms
from .models import *
 
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("firstname","lastname","email","password","contact")
        # fields = ("userimg","firstname","lastname","email","password","contact")
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Your Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Your Password'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Your Contact No.'}),
        }

class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","password")
        widgets = {

            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Your Email'}),

            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter Your Password'}),

        }
