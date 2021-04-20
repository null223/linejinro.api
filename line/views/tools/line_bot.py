from django.conf import settings
from linebot import LineBotApi


line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)
