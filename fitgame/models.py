from django.db import models
from django.conf import settings

class UserFitbit(models.Model):
    """ A user's fitbit credentials, allowing API access """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fitbit_user = models.CharField(max_length=32, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.FloatField(help_text='Timestamp when the access token expires')

    def __str__(self):
        return str(self.user)

    def refresh_cb(self, token):
        """ Called when the OAuth token has been refreshed """
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        self.expires_at = token['expires_at']
        self.save()
