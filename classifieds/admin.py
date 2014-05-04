from django.contrib import admin
from classifieds.models import *


class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_owner', 'featured', 'published', 'published_date', 'remove_date']
    list_filter = ['featured', 'published']
    list_display_links = ['title', 'get_owner']

    def get_owner(self, obj):
        return '<a href="/admin/common/mokouser/{0}">{1}</a>'.format(obj.owner.id, obj.owner.get_full_name())

    get_owner.allow_tags = True
    get_owner.short_description = "Posted By"


admin.site.register(Job, JobAdmin)
admin.site.register(Company)
admin.site.register(General)
admin.site.register(ContactDetail)
admin.site.register(JobRequirement)
admin.site.register(Taxonomy)