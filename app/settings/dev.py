from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i7bqh5eiw93f*$d6q_#$506gp%w8@xvo0nu77f_j&g&yt-zh38"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# CONSOLE email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# MAILHOG email backend.
# Testing email with mailhog, the mailhog container is running on port 1025
# UNCOMENT THE FOLLOWING LINES TO USE MAILHOG
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "mailhog"
# EMAIL_PORT = 1025

# Remove if not required
INSTALLED_APPS += ["wagtail.contrib.styleguide", "app.style_guide"]  # noqa F405


try:
    from .local import *  # noqa
except ImportError:
    pass
