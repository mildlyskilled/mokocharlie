from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from moko.forms import CustomUserChangeForm, CustomUserCreationForm
from photos.models import Photo, Album, Comment, Hotel, PhotoStory, Promotion, UserPhoto, MokoUser
from django.utils.translation import ugettext_lazy as _


class AlbumForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = Photo.objects.filter(album=self.instance.pk)


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm


class MokoUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(MokoUser, MokoUserAdmin)
admin.site.register(Photo)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Comment)
admin.site.register(Hotel)
admin.site.register(PhotoStory)
admin.site.register(Promotion)
admin.site.register(UserPhoto)