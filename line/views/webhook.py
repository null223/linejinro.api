import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.models import TextSendMessage
# from line.models import Room
from . import tools
from .tools.line_bot import line_bot_api


class WebHookView(APIView):

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        # リクエスト取得
        request_json = json.loads(request.body.decode('utf-8'))

        if request_json != None:
            for event in request_json['events']:
                
                # ブロック時処理スルー
                if tools.message_type(event) == 'unfollow': return Response(status=200)
                # 接続確認用
                if tools.reply_token(event) == '00000000000000000000000000000000': return Response(status=200)

                # text message
                if tools.message_type(event) == 'message':
                    line_bot_api.reply_message(tools.reply_token(event), TextSendMessage(text='Hello World!'+settings.LINE_ACCOUNT_ID))

                elif tools.message_type(event) == 'postback':
                    # word wolf
                    if tools.action_type(event) == 'start__wordWolf':
                        views.StartWordWolf(event)



        # ステータスコード 200 を返却
        return Response({'result': 'true'}, status=200)