import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.models import TextSendMessage
from . import tools
from .tools.line_bot import line_bot_api


def StartWordWolf(event):

    line_bot_api.reply_message(tools.reply_token(event), TextSendMessage(text='プレイ人数を教えてね'))