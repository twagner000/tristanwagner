from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='x48gm=xyt7cgz_3zl6r4bxh2^^-_s8++x0sh4j_*px-e$u&kp4')

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WEBPACK_LOADER = {
    'TIMETRACKER': {
            'BUNDLE_DIR_NAME': 'timetracker_bundles/',
            'STATS_FILE': str(APPS_DIR.path('timetracker','webpack-stats.dev.json')),
        },
    'BG_REC': {
            'BUNDLE_DIR_NAME': 'bg_rec_bundles/',
            'STATS_FILE': str(APPS_DIR.path('bg_rec','webpack-stats.dev.json')),
        },
}