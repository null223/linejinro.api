from django.core.management.base import BaseCommand
from line.models import WordWolfItem

class Command(BaseCommand):

    def handle(self, *args, **options):
        WordWolfItem.objects.bulk_create([
            WordWolfItem(vil_img='東京', wolf_img='静岡'),
            WordWolfItem(vil_img='お茶漬け', wolf_img='ふりかけ'),
            WordWolfItem(vil_img='牛丼', wolf_img='カツ丼'),
            WordWolfItem(vil_img='ボールペン', wolf_img='シャープペン'),
            WordWolfItem(vil_img='スケート', wolf_img='スキー'),
            WordWolfItem(vil_img='ディズニーランド', wolf_img='ユニバ'),
            WordWolfItem(vil_img='水族館', wolf_img='動物園'),
            WordWolfItem(vil_img='カニ', wolf_img='カキ'),
            WordWolfItem(vil_img='クッキー', wolf_img='グミ'),
            WordWolfItem(vil_img='ガリガリ君', wolf_img='雪見だいふく'),
            WordWolfItem(vil_img='昼寝', wolf_img='夜更かし'),
            WordWolfItem(vil_img='パンツ', wolf_img='財布'),
            WordWolfItem(vil_img='ショッピングモール', wolf_img='商店街'),
            WordWolfItem(vil_img='加湿器', wolf_img='エアコン'),
            WordWolfItem(vil_img='健康診断', wolf_img='予防接種'),
            WordWolfItem(vil_img='ウェディングドレス', wolf_img='振袖')
        ])
