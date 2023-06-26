# Create your tasks here

from celery import shared_task

from apis.control_device import control_device


@shared_task
def control_led():
    return control_device()
