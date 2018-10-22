from django.forms import ModelForm

from submission.models import HeadlineSummary


class HeadlineSummaryForm(ModelForm):
    class Meta:
        model = HeadlineSummary
        exclude = ('created', 'ip')
