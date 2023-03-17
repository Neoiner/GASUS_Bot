from django.contrib import admin

# Register your models here.

from .models import ScheduleGroupTypeDay, Users


class UsersAdmin(admin.ModelAdmin):
    search_fields = ['first_name']


admin.site.register(Users, UsersAdmin)


class ScheduleGroupTypeDayAdmin(admin.ModelAdmin):
    search_fields = ['group_name_with_type_and_day']


admin.site.register(ScheduleGroupTypeDay, ScheduleGroupTypeDayAdmin)
