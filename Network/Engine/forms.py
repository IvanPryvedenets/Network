from django import forms
from .models import Post


# Create form for post creating
class PostForm(forms.ModelForm):
    class Meta:
            model = Post
            fields = ['title', 'text', 'read']

    title = forms.CharField(max_length=100, required=True)
    text = forms.CharField(widget=forms.Textarea, max_length=500, required=True)

    title.widget.attrs.update({'class': 'form-control', 'placeholder': 'Title'})
    text.widget.attrs.update({'class': 'form-control', 'rows': 4})
