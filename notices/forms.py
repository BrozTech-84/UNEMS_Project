from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    expiry_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Notice
        fields = ['title', 'content', 'category', 'attachment']
