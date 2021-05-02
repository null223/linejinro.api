from django.core.management.base import BaseCommand
from line.models import WordWolfItem

class Command(BaseCommand):

    def handle(self, *args, **options):
        WordWolfItem.objects.bulk_create([
            WordWolfItem(vil_img='東京', wolf_img='静岡'),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img=''),
            WordWolfItem(vil_img='', wolf_img='')
        ])