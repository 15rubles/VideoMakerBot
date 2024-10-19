from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from django.apps import apps
from db_manager.models import *


"""
USAGE EXAMPLE: 
user_controller = ModelController('db_manager', 'Users')
user = user_controller.add(args**)
"""

class ModelController:
    def __init__(self, model_name):
        self.model = apps.get_model('db_manager', model_name)

    def add(self, **kwargs):
        try:
            obj = self.model.object.create(**kwargs)
            return obj
        except (IntegrityError, ValidationError, ValueError) as e:
            # TODO: add logging
            print(e)

    def update(self, object_id, **kwargs):
        try:
            obj = self.model.objects.get(id=object_id)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        except ObjectDoesNotExist:
            # TODO: add logging
            raise ValidationError('Object does not exist')

    def remove(self, object_id):
        try:
            obj = self.model.objects.get(id=object_id)
            obj.delete()
        except ObjectDoesNotExist:
            # TODO: add logging
            raise ValidationError('Object does not exist')