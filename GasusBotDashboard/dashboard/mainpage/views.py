import datetime
import calendar

import pytz
from django.conf.global_settings import TIME_ZONE
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import Users, ScheduleGroupTypeDay


TIMEZONE = pytz.timezone(TIME_ZONE)

def index(request):
    now = datetime.datetime.now(tz=TIMEZONE)

    total_users = Users.objects.all().count()

    total_daily_subscribed_users = Users.objects.filter(daily_subscription_on=True).count()
    total_weekly_subscribed_users = Users.objects.filter(weekly_subscription_on=True).count()

    total_subscribed_users = total_daily_subscribed_users + total_weekly_subscribed_users

    current_year = now.year
    current_month = now.month
    current_day = now.day
    start_of_the_day = datetime.datetime(year=current_year, month=current_month,
                                         day=current_day, hour=0, minute=0, second=0, tzinfo=TIMEZONE)

    active_users = Users.objects.filter(last_active_time__gte=str(start_of_the_day)).count()

    total_schedules = ScheduleGroupTypeDay.objects.all().count()

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', {
        'total_users': total_users,
        'total_subscribed_users': total_subscribed_users,
        'total_daily_subscribed_users': total_daily_subscribed_users,
        'total_weekly_subscribed_users': total_weekly_subscribed_users,
        'active_users': active_users,
        'total_schedules': total_schedules
    })




class TotalUsersChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        users_count = []

        now = datetime.datetime.now(tz=TIMEZONE)
        current_year = now.year
        current_month = now.month
        current_month_text = now.strftime("%B")
        current_day = now.day

        for day in range(1, current_day + 1):
            date = datetime.datetime(year=current_year, month=current_month, day=day,
                                     hour=23, minute=59, second=59, tzinfo=TIMEZONE)
            label = current_month_text + ' ' + str(day)
            labels.append(label)
            registered_by_the_day = Users.objects.filter(created_time__lte=str(date)).count()
            users_count.append(registered_by_the_day)

        data = {
            'labels': labels,
            'users_count': users_count,
        }
        return Response(data)

    class DailyActiveUsersChartData(APIView):
        authentication_classes = []
        permission_classes = []

        def get(self, request, format=None):
            labels = []
            users_count = []

            now = datetime.datetime.now(tz=TIMEZONE)
            current_year = now.year
            current_month = now.month
            current_day = now.day
            start_of_the_day = datetime.datetime(year=current_year, month=current_month,
                                                 day=current_day, hour=0, minute=0, second=0, tzinfo=TIMEZONE)

            for day in range(1, current_day + 1):
                date = datetime.datetime(year=current_year, month=current_month, day=day,
                                         hour=23, minute=59, second=59, tzinfo=TIMEZONE)
                label = current_month_text + ' ' + str(day)
                labels.append(label)
                registered_by_the_day = Users.objects.filter(created_time__lte=str(date)).count()
                users_count.append(registered_by_the_day)

            data = {
                'labels': labels,
                'users_count': users_count,
            }
            return Response(data)
