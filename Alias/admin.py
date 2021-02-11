from django.contrib import admin
from Alias.models import Alias


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ['alias', 'target', 'start', 'end']
