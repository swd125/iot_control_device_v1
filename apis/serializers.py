import datetime
import json
from django.conf import settings
from django.forms import model_to_dict
from rest_framework import serializers
from django_celery_beat.models import ClockedSchedule, PeriodicTask, CrontabSchedule


class IotControlDevicePeriodSerializer(serializers.Serializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs.get('start_datetime') > attrs.get('end_datetime'):
            raise serializers.ValidationError
        
        task_name = 'apis.tasks.control_led_with_msg'
        get_start_clocked, get_start_clocked_created = ClockedSchedule.objects.get_or_create(clocked_time=attrs.get('start_datetime'))
        get_end_clocked, get_endclocked_created = ClockedSchedule.objects.get_or_create(clocked_time=attrs.get('end_datetime'))
        
        if PeriodicTask.objects.filter(clocked__clocked_time=attrs.get('start_datetime'), task=task_name).exists():
            raise serializers.ValidationError('invalid range time')
        if PeriodicTask.objects.filter(clocked__clocked_time=attrs.get('end_datetime'), task=task_name).exists():
            raise serializers.ValidationError('invalid range time')
        
        topic = "control/807D3AC722E8"
        start_periodic_task_object = {
            "name": f"{task_name}-{datetime.datetime.now()}",
            "task": task_name,
            "clocked": get_start_clocked,
            "one_off": True,
            "start_time": datetime.datetime.now(),
            "args": [topic, {'control_led': 1}],
        }

        end_periodic_task_object = {
            "name": f"{task_name}-{datetime.datetime.now()}",
            "task": task_name,
            "clocked": get_end_clocked,
            "one_off": True,
            "start_time": datetime.datetime.now(),
            "args": [topic, {'control_led': 0}],
        }

        attrs['periodic_tasks'] = [start_periodic_task_object, end_periodic_task_object]

        return attrs
    
    def create(self, validated_data):
        periodic_tasks = validated_data.get('periodic_tasks') 
        result = []
        if periodic_tasks:
            for data in periodic_tasks:
                periodic_task, created = PeriodicTask.objects.get_or_create(
                    name= data.get('name'),
                    task= data.get('task'),
                    clocked= data.get('clocked'),
                    one_off= data.get('one_off'),
                    start_time= data.get('start_time'),
                    args= json.dumps(data.get('args')),
                )
                periodic_task_object = model_to_dict(periodic_task)
                result.append(periodic_task_object)
            else:
                return result
        else:   
            return serializers.ValidationError
        
    def to_representation(self, instance):
        result = {
            "periodic_tasks": instance
        }
        print("to_representation >>>> ", instance)
        return result
    

class IotControlDeviceDailySerializer(serializers.Serializer):
    topic = serializers.CharField(default='control/807D3AC722E8')
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        if start_time > end_time:
            raise serializers.ValidationError
        
        print('start_time >>>>>>>>>> ', start_time)
        print('end_time >>>>>>>>>> ', end_time)
        task_name = 'apis.tasks.control_led_with_msg'
        get_start_time, get_start_time_created = CrontabSchedule.objects.get_or_create(minute=start_time.minute, hour=start_time.hour, timezone=settings.TIME_ZONE)
        get_end_time, get_end_time_created = CrontabSchedule.objects.get_or_create(minute=end_time.minute, hour=end_time.hour, timezone=settings.TIME_ZONE)
        
        if PeriodicTask.objects.filter(crontab__minute=start_time.minute, crontab__hour=start_time.hour, task=task_name).exists():
            raise serializers.ValidationError('invalid range time')
        if PeriodicTask.objects.filter(crontab__minute=end_time.minute, crontab__hour=end_time.hour, task=task_name).exists():
            raise serializers.ValidationError('invalid range time')
        
        topic = attrs.get('topic')
        start_periodic_task_object = {
            "name": f"{task_name}-{start_time}",
            "task": task_name,
            "crontab": get_start_time,
            "start_time": None,                                     # datetime.datetime.now(),
            "args": json.dumps([topic, {'control_led': 1}]),
        }

        end_periodic_task_object = {
            "name": f"{task_name}-{end_time}",
            "task": task_name,
            "crontab": get_end_time,
            "start_time": None,                                    # datetime.datetime.now(),
            "args": json.dumps([topic, {'control_led': 0}]),
        }

        attrs['periodic_tasks'] = [start_periodic_task_object, end_periodic_task_object]

        return attrs
    
    def create(self, validated_data):
        periodic_tasks = validated_data.get('periodic_tasks') 
        result = []
        if periodic_tasks:
            for data in periodic_tasks:
                periodic_task, created = PeriodicTask.objects.get_or_create(**data)
                periodic_task_object = model_to_dict(periodic_task)
                result.append(periodic_task_object)
            else:
                return result
        else:   
            return serializers.ValidationError
        
    def to_representation(self, instance):
        result = {
            "periodic_tasks": instance
        }
        print("to_representation >>>> ", instance)
        return result