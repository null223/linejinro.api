from django.db import models
from django.conf import settings
from .mixins import *


class RichMenuQuerySet(models.QuerySet):
    pass

class RichMenuManager(models.Manager):
    def get_queryset(self):
        return RichMenuQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class RichMenu(TimestampMixin):
    menu_id = models.CharField(max_length=255)

    objects = RichMenuManager()

    def __str__(self):
        return str(self.menu_id)

    class Meta:
        default_related_name = 'rich_menu_set'
        db_table = 'rich_menu'
        verbose_name = verbose_name_plural = 'models.rich_menu'
        ordering = ['-id']
        get_latest_by = 'created_at'