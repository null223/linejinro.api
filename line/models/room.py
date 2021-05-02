from django.db import models
from django.conf import settings
import uuid
from .wordwolf_item import WordWolfItem
from .mixins import *


class RoomQuerySet(models.QuerySet):
    pass

class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class Room(TimestampMixin):
    token = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    result = models.BooleanField(default=False)
    word = models.ForeignKey(WordWolfItem, null=True, on_delete=models.PROTECT)

    objects = RoomManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        default_related_name = 'room_set'
        db_table = 'room'
        verbose_name = verbose_name_plural = 'models.room'
        ordering = ['-id']
        get_latest_by = 'created_at'