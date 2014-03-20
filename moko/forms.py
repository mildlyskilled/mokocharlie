from django import forms
from django.forms import ModelForm, Textarea, TextInput, HiddenInput
from photos.models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from photos.models import MokoUser


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('image_comment', 'comment_author', 'image')
        labels = {
            'image_comment': _('Your Comment'),
            'comment_author': _('Your Name'),
        }

        widgets = {
            'image_comment': Textarea(attrs={'cols': 40, 'rows': 5}),
            'comment_author': TextInput(attrs={'class': 'col-lg-12'}),
            'image': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'post-comment-form'
        self.helper.form_action = "javascript:postComment('post-comment-form')"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-5'
        self.helper.field_class = 'col-lg-7'
        self.helper.add_input(
            Submit('submit', 'Post Comment', css_class="btn btn-success pull-right"))
        self.helper.layout = Layout(
            Fieldset(
                'Your Comment',
                'image',
                'image_comment',
                'comment_author',
            )
        )


class LoginForm(forms.Form):
    """ Basic username/password based login form. """
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['required'] = \
            "Please enter a username"
        self.fields['password'].error_messages['required'] = \
            "Please enter a password"
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7 login-fields'
        self.helper.add_input(Submit('submit', 'Login'))


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = MokoUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = MokoUser