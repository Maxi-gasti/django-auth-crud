from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'My task'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write the description'}),
        }
