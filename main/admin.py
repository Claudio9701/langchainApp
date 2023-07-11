from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    min_num = 1
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
