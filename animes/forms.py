from django.forms import ModelForm
from django import forms
from .models import Anime, Review


class AnimeForm(ModelForm):
    class Meta:
        model = Anime
        fields = ['title', 'featured_image', 'description', 'source_link', 'tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AnimeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body']

        labels = {
            'body':'Leave your review'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class VoteForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value']

        labels = {
            'value':'Vote'
        }

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})