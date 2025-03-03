from django.contrib import admin
from accounts import models
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','role','is_active')
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(models.User,CustomUserAdmin)
admin.site.register(models.UserProfile)