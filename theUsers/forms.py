from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'department', 'phone']
        widgets = {
            'role': forms.Select(attrs={'class':'form-control'}),
            'department': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Department'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
        }