from django import forms
from .models import MoviePetition
from django.core.exceptions import ValidationError

class MoviePetitionForm(forms.ModelForm):
    class Meta:
        model = MoviePetition
        fields = ['title', 'release_year', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the movie title...',
                'required': True
            }),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2023',
                'min': '1900',
                'max': '2030'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us why this movie should be added to our catalog...'
            }),
        }
        labels = {
            'title': 'Movie Title',
            'release_year': 'Release Year',
            'description': 'Description'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 2:
                raise ValidationError('Movie title must be at least 2 characters long.')
            if len(title) > 255:
                raise ValidationError('Movie title must be less than 255 characters.')
        return title

    def clean_release_year(self):
        release_year = self.cleaned_data.get('release_year')
        if release_year:
            if release_year < 1900 or release_year > 2030:
                raise ValidationError('Release year must be between 1900 and 2030.')
        return release_year

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            description = description.strip()
            if len(description) > 1000:
                raise ValidationError('Description must be less than 1000 characters.')
        return description