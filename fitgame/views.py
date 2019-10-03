from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render
from django.conf import settings
from fitbit import Fitbit


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
    if UserFitbit.objects.filter(fitbit_user=fitbit_user).exists():
        return redirect(reverse('fitgame:fitbit-error'))

    fbuser, _ = UserFitbit.objects.update_or_create(user=request.user, defaults={
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
    except UserFitbit.DoesNotExist:
        pass
    else:
        fbuser.delete()
    return redirect(reverse('fitgame:index'))
    

def get_steps(request):
    """An AJAX view that retrieves this user's step data from Fitbit.
    This view has been deprecated. Use `get_data` instead.
    URL name:
        `fitbit-steps`
    """

    return get_data(request, 'activities', 'steps')