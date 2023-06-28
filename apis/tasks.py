# Create your tasks here

from celery import shared_task

from apis.control_device import control_device, control_device_with_params


@shared_task
def control_led():
    return control_device()


@shared_task
def task_console():
    print("task_console")
    return 1


@shared_task
def control_led_with_msg(topic, msg):
    return control_device_with_params(topic, msg)