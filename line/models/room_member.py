from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .room import Room
import random

ROLE_CHOICES = (
    ('wolf', '人狼'),
    ('villager', '村人'),
    ('teller', '占い師'),
)

class RoomMemberQuerySet(models.QuerySet):
    def random(self):
        object_list = list(self)
        random.shuffle(object_list)
        return object_list[0]

class RoomMemberManager(models.Manager):
    def get_queryset(self):
        return RoomMemberQuerySet(self.model, using=self._db)

    def front(self):
        return self.get_queryset()

class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=255)
    line_id = models.CharField(null=True, blank=True, max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    is_master = models.BooleanField(default=False)
    is_dead = models.BooleanField(default=False)

    objects = RoomMemberManager()

    def __str__(self):
        return self.name if self.name else str(self.room)+':'+str(self.id)

    class Meta:
        default_related_name = 'room_member_set'
        db_table = 'room_member'
        verbose_name = verbose_name_plural = _('models.room_member')
        ordering = ['-room', '-id']