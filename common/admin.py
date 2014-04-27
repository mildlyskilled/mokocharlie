from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from moko.forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import ugettext_lazy as _
from common.models import *


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_albums', 'get_owner', 'published', 'times_viewed', 'created_at']
    search_fields = ['name', 'description']
    list_display_links = ('name', 'get_owner')
    list_select_related = ('get_owner', 'albums')

    def get_owner(self, obj):
        return '<a href="/admin/common/mokouser/{0}">{1}</a>'.format(obj.owner.id, obj.owner.get_full_name())


    def unpublish_photo(self, request, queryset):
        queryset.update(published=0)


    def publish_photo(self, request, queryset):
        queryset.update(published=1)

    get_owner.allow_tags = True
    get_owner.short_description = "Uploaded By"
    unpublish_photo.short_description = "Unpublish Selected Photos"
    publish_photo.short_description = "Publish Selected Photos"

    actions = [unpublish_photo, publish_photo]


class AlbumForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = Photo.objects.filter(album=self.instance.pk)


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ['label', 'created_at', 'album_images', 'featured', 'published']
    list_filter = ['published', 'featured']

    def feature_album(self, request, queryset):
        queryset.update(featured=1)

    def unfeature_album(self, request, queryset):
        queryset.update(featured=0)

    def unpublish_album(self, request, queryset):
        queryset.update(published=0)


    def publish_album(self, request, queryset):
        queryset.update(published=1)

    publish_album.short_description = "Publish Selected Photos"
    unpublish_album.short_description = "Unpublish Selected Photos"
    feature_album.short_description = "Feature Selected Albums"
    unfeature_album.short_description = "Remove Selected Albums from Featured List"

    actions = [feature_album, unfeature_album, unpublish_album, publish_album]


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['image', 'comment_author', 'comment_date', 'comment_approved', 'comment_reported']
    list_filter = ['comment_reported', 'comment_approved']

    def approve_comment(self, request, queryset):
        queryset.update(comment_approved=1)

    def disapprove_comment(self, request, queryset):
        queryset.update(comment_approved=0)

    approve_comment.short_description = "Mark selected comments as approved"
    disapprove_comment.short_description = "Mark selected comments as disapproved"

    actions = [approve_comment, disapprove_comment]


class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospitality_type', 'get_albums', 'featured', 'published']
    list_display_links = ('name', 'get_albums')
    select_related = True
    list_filter = ['published', 'featured']


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


class CollectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['cover_album'].queryset = Album.objects.filter(collections=self.instance.pk)


class CollectionAdmin(admin.ModelAdmin):
    form = CollectionForm
    list_display = ['name', 'get_albums', 'cover_album', 'featured', 'published']
    list_filter = ['featured', 'published']

    def publish_collection(self, request, queryset):
        queryset.update(published=1)

    def unpublish_collection(self, request, queryset):
        queryset.update(published=0)

    def feature_collection(self, request, queryset):
        queryset.update(featured=1)

    def unfeature_collection(self, request, queryset):
        queryset.update(featured=0)

    publish_collection.short_description = "publish Selected Collections"
    unpublish_collection.short_description = "Unpublish Selected Collections"
    feature_collection.short_description = "Feature Selected Collections"
    unfeature_collection.short_description = "Unfeature Selected Collections"

    actions = [publish_collection, unpublish_collection, feature_collection, unfeature_collection]


class ClassifiedAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassifiedAdminForm, self).__init__(*args, **kwargs)

        advertisers = Group.objects.get(name="Advertisers")
        self.fields['owner'].queryset = advertisers.user_set.all()


class ClassifiedAdmin(admin.ModelAdmin):
    #form =  ClassifiedAdminForm
    list_display = ['title', 'get_owner', 'featured', 'published', 'published_date', 'unpublish_date']
    list_filter = ['featured', 'published']
    list_display_links = ['title', 'get_owner']

    def get_owner(self, obj):
        return '<a href="/admin/common/mokouser/{0}">{1}</a>'.format(obj.owner.id, obj.owner.get_full_name())

    get_owner.allow_tags = True
    get_owner.short_description = "Posted By"


admin.site.register(MokoUser, MokoUserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(PhotoStory)
admin.site.register(Promotion)
admin.site.register(Collections, CollectionAdmin)
admin.site.register(Classified, ClassifiedAdmin)
admin.site.register(ClassifiedType)