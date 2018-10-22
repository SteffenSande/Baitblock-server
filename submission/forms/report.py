from django import forms

from headlineScraper.models import Headline
from submission.models import Report, UserReport, ReportCategory

from django.forms import ValidationError


class ReportForm(forms.ModelForm):
    explanation = forms.CharField()

    class Meta:
        model = Report

        fields = ['headline', 'category']

    def clean_explanation(self):
        explanation = self.cleaned_data.get('explanation', '')

        if not explanation:
            raise ValidationError('Explanation cannot be empty')


class UserReportForm(forms.ModelForm):
    id = forms.IntegerField()
    category = forms.CharField()

    class Meta:
        model = UserReport

        fields = ['explanation']

    def __init__(self, *args, **kwargs):
        self.ip = kwargs.pop('ip')
        super(UserReportForm, self).__init__(*args, **kwargs)

    def clean_ip(self):
        return self.ip

    def clean_explanation(self):
        explanation = self.cleaned_data.get('explanation', '')

        if not explanation:
            raise ValidationError('Explanation cannot be empty')

        return explanation

    def clean_category(self):
        category = self.cleaned_data.get('category', '')

        if not category:
            raise ValidationError('Category cannot be empty')

        try:
            return ReportCategory.objects.get(pk=category)
        except ReportCategory.DoesNotExist:
            raise ValidationError('{} is not a legal category...'.format(category))

    def clean_id(self):
        try:
            headline_id = int(self.cleaned_data.get('id', '-1'))
        except ValueError:
            raise ValidationError('Id needs to be a integer')

        try:
            return Headline.objects.get(id=headline_id)
        except Headline.DoesNotExist:
            raise ValidationError('Id must be a valid headline')

    def save(self, commit=True, **kwargs):
        report = super(UserReportForm, self).save(commit=False)
        report.ip = self.ip

        if 'report' in kwargs:
            report.report = kwargs.get('report', None)

        if commit:
            report.save()

        return report
