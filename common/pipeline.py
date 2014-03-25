from django.shortcuts import redirect
from social.pipeline.partial import partial


@partial
def extra_details(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    extra_data = strategy.backend.extra_data(user, None, response, details)
    if user and user.email:
        return
    elif is_new:
        fields = ['first_name', 'last_name', 'email']
        if strategy.session_get('email'):
            for field in fields:
                details[field] = strategy.session_pop(field)
        else:
            strategy.session['email'] = extra_data.get('email')
            strategy.session['extra'] = extra_data
            return redirect('new_profile')