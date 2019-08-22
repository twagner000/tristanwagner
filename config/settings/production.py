from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [".tristanwagner.com"]
# END SITE CONFIGURATION

SECURE_SSL_REDIRECT = True

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "tristanwagner.noreply@gmail.com"
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

WEBPACK_LOADER = {
    'TIMETRACKER': {
            'BUNDLE_DIR_NAME': 'timetracker_bundles/',
            'STATS_FILE': str(APPS_DIR.path('timetracker','webpack-stats.prod.json')),
        },
    'BG_REC': {
            'BUNDLE_DIR_NAME': 'bg_rec_bundles/',
            'STATS_FILE': str(APPS_DIR.path('bg_rec_frontend','webpack-stats.prod.json')),
        },
}