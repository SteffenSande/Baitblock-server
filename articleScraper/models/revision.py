import os

from django import forms
from django.contrib import admin
from django.db import models

from helpers.base_models import RevisionBase


class Revision(RevisionBase):
    article = models.ForeignKey('articleScraper.Article', on_delete=models.CASCADE,)
    journalists = models.ManyToManyField('articleScraper.Journalist')
    images = models.ManyToManyField('articleScraper.ArticleImage')

    words = models.IntegerField()
    subscription = models.BooleanField(default=False)

    def file_path(self, folder: str, file_type='html') -> str:
        return os.path.join(folder, os.path.join(self.article.news_site.file_folder(), self.filename(file_type)))


class RevisionModelAdminForm(forms.ModelForm):
    journalists = forms.MultipleChoiceField()
    images = forms.MultipleChoiceField()
    url = forms.URLField(disabled=True)

    def __init__(self, *args, **kwargs):
        from articleScraper.models import ArticleImage
        from articleScraper.models import Journalist

        super(RevisionModelAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['images'].choices = [(None, f) for f in ArticleImage.objects.filter(revision=kwargs['instance'])]
            self.fields['journalists'].choices = [(None, f) for f in
                                              Journalist.objects.filter(revision=kwargs['instance'])]
            try:
                self.fields['url'].initial = kwargs['instance'].article.headline.url
            except:
                pass

    class Meta:
        model = Revision
        fields = '__all__'


class RevisionAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'timestamp', 'subscription', 'version', 'file')
    search_fields = ('title', 'version',)
    list_display = ['title', 'timestamp', 'version', 'subscription']

    list_filter = [
        'version',
    ]

    form = RevisionModelAdminForm

    exclude = ('images', 'journalists',)


admin.site.register(Revision, RevisionAdmin)
