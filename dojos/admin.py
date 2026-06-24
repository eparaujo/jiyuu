from django.contrib import admin
from . import models


class DojoAdmin(admin.ModelAdmin):
    list_display = (
        'razaosocial',
        'tradename',
        'site',
        'email',
        'whatsapp',
        'phone',
        'street',
        'number',
        'zipcode',
        'district',
        'city',
        'state',
        'country',
    )

    search_fields = ('tradename',)


class DojoMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'dojo',
        'role',
        'is_active',
    )

    list_filter = (
        'role',
        'is_active',
        'dojo',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'dojo__tradename',
        'dojo__razaosocial',
    )


admin.site.register(models.Dojo, DojoAdmin)
admin.site.register(models.DojoMembership, DojoMembershipAdmin)