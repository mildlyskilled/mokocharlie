from django.contrib import admin
from django.forms import ModelForm
from moko.models import Photo, Album, Comment, Hotel, PhotoStory, Promotion, UserPhoto


# class AlbumModelAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'cover':
#             print request
#             kwargs["queryset"] = Photo.objects.filter(album=self.id)
#
#         return super(AlbumModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AlbumForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['cover'].queryset = Photo.objects.filter(album=self.instance.pk)

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm

admin.site.register(Photo)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Comment)
admin.site.register(Hotel)
admin.site.register(PhotoStory)
admin.site.register(Promotion)
admin.site.register(UserPhoto)