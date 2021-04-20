from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid


class RoomQuerySet(models.QuerySet):
    pass

class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class Room(models.Model):
    token = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    result = models.BooleanField(default=False)

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
        verbose_name = verbose_name_plural = _('models.room')
        ordering = ['-id']