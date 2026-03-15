from django.db import models


class Todo(models.Model):
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
