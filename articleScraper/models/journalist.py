from django import forms
from django.contrib import admin
from django.db import models


class Journalist(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    news_site = models.ForeignKey('scraper.NewsSite', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

    @property
    def articles(self):

        from articleScraper.models import Article
        return Article.objects.filter(revision__journalists=self)


class JournalistModelAdminForm(forms.ModelForm):
    articles = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):

        super(JournalistModelAdminForm, self).__init__(*args, **kwargs)
        self.fields['articles'].choices = [(None, f) for f in kwargs['instance'].articles]

    class Meta:
        model = Journalist
        fields = '__all__'


class JournalistAdmin(admin.ModelAdmin):
    readonly_fields = ('firstName', 'lastName', 'news_site',)
    search_fields = ('firstName', 'lastName',)
    list_display = ['firstName', 'lastName', 'news_site']

    list_filter = [
        'news_site',
    ]

    form = JournalistModelAdminForm


admin.site.register(Journalist, JournalistAdmin)
