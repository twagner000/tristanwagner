from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render
from django.conf import settings
from fitbit import Fitbit
from fitbit.exceptions import (HTTPUnauthorized, HTTPForbidden, HTTPConflict, HTTPServerError)
from . import models

from django.http import HttpResponse
import json


@login_required
def login(request):
    """
    Begin OAuth authentication process. Obtain a request token and redirect to the Fitbit site for user authorization.
    """
    callback_uri = request.build_absolute_uri(reverse('fitgame:fitbit-complete'))
    fb = Fitbit(settings.FITAPP_CONSUMER_KEY, settings.FITAPP_CONSUMER_SECRET, callback_uri=callback_uri)
    token_url, code = fb.client.authorize_token_url(redirect_uri=callback_uri)

    return redirect(token_url)
    
@login_required
def complete(request):
    """
    Store credentials. Fitbit sends a callback to this URL after user authorization.
    """
    try:
        code = request.GET['code']
    except KeyError:
        return redirect(reverse('fitgame:fitbit-error'))

    callback_uri = request.build_absolute_uri(reverse('fitgame:fitbit-complete'))
    fb = Fitbit(settings.FITAPP_CONSUMER_KEY, settings.FITAPP_CONSUMER_SECRET, callback_uri=callback_uri)
    try:
        token = fb.client.fetch_access_token(code, callback_uri)
        access_token = token['access_token']
        fitbit_user = token['user_id']
    except KeyError:
        return redirect(reverse('fitgame:fitbit-error'))

    #check if fitbit_user already exists
    if models.UserFitbit.objects.filter(fitbit_user=fitbit_user).exists():
        return redirect(reverse('fitgame:fitbit-error'))

    fbuser, _ = models.UserFitbit.objects.update_or_create(user=request.user, defaults={
        'fitbit_user': fitbit_user,
        'access_token': access_token,
        'refresh_token': token['refresh_token'],
        'expires_at': token['expires_at'],
    })

    return redirect(reverse('fitgame:index'))


@login_required
def logout(request):
    """Forget this user's Fitbit credentials.
    """
    try:
        fbuser = request.user.userfitbit
    except models.UserFitbit.DoesNotExist:
        pass
    else:
        fbuser.delete()
    return redirect(reverse('fitgame:index'))
    
    
def make_response(code=None, objects=[]):
    """AJAX helper method to generate a response"""

    data = {
        'meta': {'total_count': len(objects), 'status_code': code},
        'objects': objects,
    }
    return HttpResponse(json.dumps(data))
    

def get_steps(request):
    """
    <https://python-fitbit.readthedocs.io/en/latest/#fitbit.Fitbit.time_series>
    <https://dev.fitbit.com/build/reference/web-api/activity/#activity-time-series>
    """
    
    #check that user is logged in and integrated with Fitbit.
    user = request.user
    if not user.is_authenticated or not user.is_active:
        return make_response(101)
    elif not models.UserFitbit.objects.filter(user=user).exists():
        return make_response(102)
    fbuser = models.UserFitbit.objects.get(user=user)
        
    #check that resource path is valid ('tracker' in path excludes manual log entries), else status 104
    resource_path = '/activities/tracker/steps'

    #check dates
    """base_date = request.GET.get('base_date', 'today')
    period = request.GET.get('period', None)
    end_date = request.GET.get('end_date', None)
    if period:
        #need period or end_date (not both)
        if end_date:
            make_response(104)
        #TODO: check period is valid
            #return make_response(104)
    elif not end_date:
        #need period or end_date
        return make_response(104)
    """
    base_date = 'today'
    period = '30d'
    end_date = None

    # Request data through the API and handle related errors.
    try:
        fb = Fitbit(settings.FITAPP_CONSUMER_KEY, settings.FITAPP_CONSUMER_SECRET, **fbuser.get_user_data())
        data = fb.time_series(resource_path, base_date=base_date, period=period, end_date=end_date)
        data = data['activities-tracker-steps']
    except (HTTPUnauthorized, HTTPForbidden):
        # Delete invalid credentials.
        fbuser.delete()
        return make_response(103)
    except HTTPConflict:
        return make_response(105)
    except HTTPServerError:
        return make_response(106)
    #except:
    #    raise

    return render(request, 'fitgame/steps.html', {'steps':data})
    
    
def get_activities(request):
    #check that user is logged in and integrated with Fitbit.
    user = request.user
    if not user.is_authenticated or not user.is_active:
        return make_response(101)
    elif not models.UserFitbit.objects.filter(user=user).exists():
        return make_response(102)
    fbuser = models.UserFitbit.objects.get(user=user)
        
    fb = Fitbit(settings.FITAPP_CONSUMER_KEY, settings.FITAPP_CONSUMER_SECRET, **fbuser.get_user_data())
    data = fb.activities()

    return render(request, 'fitgame/activities.html', {'activities':data})