from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from django.shortcuts import redirect
from django.contrib import messages


class MokoSocialMiddleWare(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            messages.add_message(request, messages.WARNING,
                                 "There was an error logging you in have you already\
                                  registered using this email address?")
            return redirect("login")
        else:
            raise exception