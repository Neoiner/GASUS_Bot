# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ScheduleGroupTypeDay(models.Model):
    group_name_with_type_and_day = models.CharField(primary_key=True, max_length=40)
    academic_degree = models.CharField(max_length=30, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=25, blank=True, null=True)
    week_type = models.CharField(max_length=15, blank=True, null=True)
    day_of_week = models.CharField(max_length=15, blank=True, null=True)
    first_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    first_lecture = models.CharField(max_length=255, blank=True, null=True)
    second_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    second_lecture = models.CharField(max_length=255, blank=True, null=True)
    third_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    third_lecture = models.CharField(max_length=255, blank=True, null=True)
    fourth_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    fourth_lecture = models.CharField(max_length=255, blank=True, null=True)
    fifth_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    fifth_lecture = models.CharField(max_length=255, blank=True, null=True)
    sixth_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    sixth_lecture = models.CharField(max_length=255, blank=True, null=True)
    seventh_lecture_time = models.CharField(max_length=15, blank=True, null=True)
    seventh_lecture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule_group_type_day'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    group = models.CharField(max_length=15, blank=True, null=True)
    daily_subscription_on = models.BooleanField(blank=True, null=True)
    weekly_subscription_on = models.BooleanField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    last_active_time = models.DateTimeField(blank=True, null=True)
    is_moderator = models.BooleanField(blank=True, null=True, default=False)
    class Meta:
        managed = False
        db_table = 'users'
