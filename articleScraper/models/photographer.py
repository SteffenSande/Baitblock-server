from django import forms
from django.contrib import admin
from django.db import models


class Photographer(models.Model):
    firstName = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

    @property
    def images(self):
        from articleScraper.models import ArticleImage
        return ArticleImage.objects.filter(photographers__articleimage__photographers=self)


class PhotographerModelAdminForm(forms.ModelForm):
    images = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super(PhotographerModelAdminForm, self).__init__(*args, **kwargs)
        self.fields['images'].choices = [(None, f) for f in kwargs['instance'].images]

    class Meta:
        model = Photographer
        fields = '__all__'


class PhotographerAdmin(admin.ModelAdmin):
    form = PhotographerModelAdminForm


