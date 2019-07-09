from django import forms
from django.contrib import admin
from django.db import models


class ArticleImage(models.Model):
    url = models.URLField(max_length=2500)
    text = models.TextField()

    photographers = models.ManyToManyField('articleScraper.Photographer')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class ArticleImageModelAdminForm(forms.ModelForm):
    photographers = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super(ArticleImageModelAdminForm, self).__init__(*args, **kwargs)
        self.fields['photographers'].choices = [(None, f) for f in kwargs['instance'].photographers.all()]

    class Meta:
        model = ArticleImage
        exclude = ('photographers',)


class ArticleImageAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    search_fields = ('text',)
    list_display = ['text']

    form = ArticleImageModelAdminForm

