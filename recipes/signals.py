from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages


def handle_login(sender, request, user, **kwargs):
    messages.success(request, "Logged in successfully.")


def handle_logout(sender, request, user, **kwargs):
    messages.info(request, "You have been logged out.")


user_logged_in.connect(handle_login)
user_logged_out.connect(handle_logout)
