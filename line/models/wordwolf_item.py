from django.db import models
from django.conf import settings
from .mixins import *
import random


class WordWolfItemQuerySet(models.QuerySet):
    def random(self):
        object_list = list(self)
        random.shuffle(object_list)
        return object_list[0]

class WordWolfItemManager(models.Manager):
    def get_queryset(self):
        return WordWolfItemQuerySet(self.model, using=self._db)

    def line(self):
        return self.get_queryset()

class WordWolfItem(TimestampMixin):
    # vil_name = models.CharField(max_length=255)
    vil_img = models.CharField(max_length=255)
    # wolf_name = models.CharField(max_length=255)
    wolf_img = models.CharField(max_length=255)

    objects = WordWolfItemManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        default_related_name = 'word_wolf_item_set'
        db_table = 'word_wolf_item'
        verbose_name = verbose_name_plural = 'models.word_wolf_item'
        ordering = ['-id']