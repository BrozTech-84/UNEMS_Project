from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email',]
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
    
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[-1]

        STUDENT_DOMAIN = 'student.university.ke'
        STAFF_ADMIN_DOMAIN = 'staf.university.ke'   
        
        role = None

        if domain == STUDENT_DOMAIN:
            role = 'student'
        elif domain == STAFF_ADMIN_DOMAIN:
            role = 'staff' 
        else:
            raise ValidationError("Please use a valid university email address.")

        self.cleaned_data['role'] = role
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'phone']
        widgets = {
            'department': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Department'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
        }