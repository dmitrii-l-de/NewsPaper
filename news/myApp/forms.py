from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Author, User


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = [
            'title',
            'article',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("article")

        if title == text:
            raise ValidationError(
                "Заголовок не должно быть идентичен тексту статьи."
            )
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
           'email',
           'username',
           'first_name',
           'last_name',
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
