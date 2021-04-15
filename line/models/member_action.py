from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .room_member import RoomMember
from .days import Days

class MemberActionQuerySet(models.QuerySet):
    pass

class MemberActionManager(models.Manager):
    def get_queryset(self):
        return MemberActionQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class MemberAction(models.Model):
    member = models.ForeignKey(RoomMember, related_name='member', on_delete=models.CASCADE)
    days = models.ForeignKey(Days, on_delete=models.CASCADE)
    select = models.ForeignKey(RoomMember, related_name='select_member', on_delete=models.CASCADE)

    objects = MemberActionManager()

    def __str__(self):
        return self.id

    class Meta:
        default_related_name = 'member_action_set'
        db_table = 'member_action'
        verbose_name = verbose_name_plural = _('models.member_action')
        ordering = ['-member', '-id']