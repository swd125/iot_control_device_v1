from celery import shared_task
from django_celery_beat.models import PeriodicTask, PeriodicTasks, ClockedSchedule
from rest_framework import generics
from apis.control_device import control_device_with_params
from apis.serializers import IotControlDevicePeriodSerializer, IotControlDeviceDailySerializer


class IotControlDevicePeriodApi(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = IotControlDevicePeriodSerializer


class IotControlDeviceDailyApi(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = IotControlDeviceDailySerializer