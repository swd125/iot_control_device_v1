from django.urls import path

from apis.views.v1.api_control_device import IotControlDevicePeriodApi, IotControlDeviceDailyApi

urlpatterns = [
    path('api/v1/iot-control-device-period-task', IotControlDevicePeriodApi.as_view()),
    path('api/v1/iot-control-device-daily-task', IotControlDeviceDailyApi.as_view())
]
