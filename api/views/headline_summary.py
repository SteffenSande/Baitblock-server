import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from submission.forms.headline_summary import HeadlineSummaryForm
from helpers.utilities import get_user_ip


@csrf_exempt
def headline_summary(request):
    data = {
        'message': 'No access',
        'error': True
    }

    if request.method != 'POST':
        return JsonResponse(data)

    form = HeadlineSummaryForm(request.POST)

    if not form.is_valid():
        data['message'] = 'Could not submit summary for headline. Some data was missing'
        return JsonResponse(data)

    try:
        summary = form.save(commit=False)
        summary.ip = get_user_ip(request)
        summary.created = datetime.datetime.now()
        summary.save()

        if summary.headline.summary is None:
            summary.headline.summary = summary
            summary.headline.save()

        data['error'] = False
        data['message'] = 'Success. A moderator is reviewing the submission.'
    except:
        data['message'] = 'There has occurred an error. Please try again later.'

    return JsonResponse(data)
