from django.db import models
from django.conf import settings
from .room import Room
from .mixins import *

class DaysQuerySet(models.QuerySet):
    pass

class DaysManager(models.Manager):
    def get_queryset(self):
        return DaysQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class Days(TimestampMixin):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day = models.IntegerField(default=0)
    is_night = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)

    objects = DaysManager()

    def __str__(self):
        daytime = "night" if self.is_night else "noon"
        return "[{room}:{daytime}]".format(room=self.room, daytime=daytime)

    class Meta:
        default_related_name = 'days_set'
        db_table = 'days'
        verbose_name = verbose_name_plural = 'models.days'
        ordering = ['-room', '-id']
