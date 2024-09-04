from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class useradmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','is_active','date_join')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_join')
    ordering = ('-date_join',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(User,useradmin)