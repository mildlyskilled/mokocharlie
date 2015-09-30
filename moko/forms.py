from uuid import uuid4
from django import forms
from django.forms import ModelForm, Textarea, TextInput, HiddenInput, DecimalField, Form
from common.models import Comment, Album, Classified, Contact
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Button, Field, Div
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from common.models import MokoUser, Photo
from haystack.forms import SearchForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
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
        self.fields['email'].error_messages['required'] = \
            "Please enter a username"
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7 login-fields'
        self.helper.add_input(Submit('submit', 'Save'))

    class Meta:
        model = MokoUser
        fields = ("email", "first_name", "last_name")


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
        fields = '__all__'


class MokoUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(MokoUserChangeForm, self).__init__(*args, **kargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-7'
        self.helper.add_input(
            Submit('submit', 'Save Changes', css_class="btn btn-success pull-right"))
        self.helper.add_input(
            Button("button", "Cancel", css_class="btn btn-danger"))
        self.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'last_name',
                'email',
            )
        )
        del self.fields['password']
        del self.fields['username']

    class Meta:
        model = MokoUser
        fields = ("email", "first_name", "last_name")
        help_texts = {
            'is_active': _('Should your account stay active?')
        }


class GeneralSearchForm(SearchForm):
    """ A form for performing search across Photos, Albums and Comments
    """

    def __init__(self, *args, **kwargs):
        super(GeneralSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7 login-fields'


class PhotoUploadForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['name', 'caption', 'owner', 'image_id', 'cloud_image', 'albums']
        widgets = {
            'name': TextInput(attrs={'class': 'col-lg-12'}),
            'caption': Textarea(attrs={'cols': 40, 'rows': 5}),
            'owner': HiddenInput(),
            'image_id': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'upload_photos'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7 login-fields'
        self.helper.add_input(Submit('submit', 'Submit', css_class='pull-right'))
        self.helper.layout = Layout(
            Fieldset(
                'Please describe your photo',
                # BEGIN HIDDEN FIELDS
                'published',
                'owner',
                'image_id',
                # END HIDDEN FIELDS
                'name',
                'caption',
                'cloud_image',
                'albums'
            )
        )
        self.fields['albums'].queryset = Album.objects.filter(label='People and Places')
        image_id = forms.CharField(initial=uuid4())


class ClassifiedForm(ModelForm):
    class Meta:
        model = Classified
        fields = ['type', 'title', 'description', 'contact', 'owner']

    def __init__(self, *args, **kwargs):
        super(ClassifiedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7 login-fields'
        self.helper.add_input(Submit('submit', 'Save Changes', css_class='pull-right'))
        self.helper.layout = Layout(
            Fieldset(
                'Create a classified',
                Field('type'),
                Field('title'),
                Field('description'),
                Field('contact'),
                'owner'
            ),
            Fieldset(
                'Describe the classified',
                Div(id='meta')
            )
        )


class DbContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class HospitalityContactForm(Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={"cols": 40, "rows": 5}))
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'post'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout(
        Fieldset(
            'Send a message',
            Field('name'),
            Field('email'),
            Field('message')
        )
    )
    helper.add_input(Submit('submit', 'Send Message', css_class='pull-right btn'))

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
