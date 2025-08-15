from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i7bqh5eiw93f*$d6q_#$506gp%w8@xvo0nu77f_j&g&yt-zh38"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Remove if not required
INSTALLED_APPS += [  # noqa F405
    "app.style_guide",
    "wagtail.contrib.styleguide",
    "django_browser_reload",
]

MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]  # noqa F405


try:
    from .local import *  # noqa
except ImportError:
    pass
