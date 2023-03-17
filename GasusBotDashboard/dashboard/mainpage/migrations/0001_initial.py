# Generated by Django 3.1.7 on 2021-04-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleGroupTypeDay',
            fields=[
                ('group_name_with_type_and_day', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('academic_degree', models.CharField(blank=True, max_length=30, null=True)),
                ('faculty', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=25, null=True)),
                ('week_type', models.CharField(blank=True, max_length=15, null=True)),
                ('day_of_week', models.CharField(blank=True, max_length=15, null=True)),
                ('first_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('first_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('second_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('second_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('third_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('third_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('fourth_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('fourth_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('fifth_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('fifth_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('sixth_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('sixth_lecture', models.CharField(blank=True, max_length=255, null=True)),
                ('seventh_lecture_time', models.CharField(blank=True, max_length=15, null=True)),
                ('seventh_lecture', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'schedule_group_type_day',
                #'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('group', models.CharField(blank=True, max_length=15, null=True)),
                ('daily_subscription_on', models.BooleanField(blank=True, null=True)),
                ('weekly_subscription_on', models.BooleanField(blank=True, null=True)),
                ('created_time', models.DateTimeField(blank=True, null=True)),
                ('last_active_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                #'managed': False,
            },
        ),
    ]