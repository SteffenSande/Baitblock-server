from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from helpers.utilities import get_user_ip
from submission.forms.report import UserReportForm

from submission.models import Report, UserReport


@csrf_exempt
def report_headline(request):
    data = {
        'message': 'No access',
        'error': True
    }

    if request.method != 'POST':
        return JsonResponse(data)

    form = UserReportForm(request.POST, ip=get_user_ip(request))

    if not form.is_valid():
        data['message'] = 'Could not report. Some data was missing! ({}) '.format(form.errors.as_text())
        return JsonResponse(data)

    try:
        report = Report.objects.get(headline=form.cleaned_data.get('id', None), category=form.cleaned_data.get('category', None))
    except Report.DoesNotExist:
        report = Report(headline=form.cleaned_data.get('id', None), category=form.cleaned_data.get('category', None))
        report.save()
        form.save(report=report)
        data['message'] = 'Link reported!'
        data['error'] = False
        return JsonResponse(data)

    try:
        UserReport.objects.get(report__id=report.id, ip=get_user_ip(request))
        data['message'] = 'IP has already reported this link'
    except UserReport.DoesNotExist:
        form.save(report=report)
        report.save()

        data['message'] = 'Link reported!'
        data['error'] = False

    return JsonResponse(data)
