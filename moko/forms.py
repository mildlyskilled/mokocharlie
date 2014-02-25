from django.forms import ModelForm, Textarea, TextInput
from moko.models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django.utils.translation import gettext as _


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('image_comment', 'comment_author')
        labels = {
            'image_comment': _('Your Comment'),
            'comment_author': _('Your Name'),
        }

        widgets = {
            'image_comment': Textarea(attrs={'cols': 40, 'rows': 5}),
            'comment_author': TextInput(attrs={'class': 'col-lg-12'})
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-5'
        self.helper.field_class = 'col-lg-7'
        self.helper.layout = Layout(
            Fieldset(
                'Your Comment',
                'image_comment',
                'comment_author',
            )
        )
        self.helper.add_input(Submit('submit', 'Post Comment', css_class="btn btn-success pull-right"))
