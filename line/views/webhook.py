import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.models import TextSendMessage
# from line.models import Room
from . import tools, word_wolf
from .tools.line_bot import line_bot_api
from line.models import RoomMember


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

                member = RoomMember.objects.line().filter(line_id=tools.line_id(event))

                # status None
                if not member.exists():
                    if tools.message_type(event) == 'message':
                        if tools.data_text(event).startswith('token_at'):
                            word_wolf.JoinRoom(event)
                        else:
                            word_wolf.StartWordWolf(event)

                    elif tools.message_type(event) == 'postback':
                        if tools.action_type(event).startswith('wordWolf__n-'):
                            word_wolf.SetWordWolf(event)
                        else:
                            tools.SomeError(event)

                # status Init
                elif member.latest('created_at').status == 'init':
                    if tools.message_type(event) == 'message':
                        word_wolf.GetName(event)

                    elif tools.message_type(event) == 'postback':
                        tools.SomeError(event)

                # status Playing
                elif member.first().status == 'playing':
                    if tools.message_type(event) == 'message':
                        pass

                    elif tools.message_type(event) == 'postback':

                        if tools.action_type(event) == 'next_step':
                            word_wolf.NextStep(event)
                        elif tools.action_type(event) == 'stop':
                            word_wolf.StopToMenu(event)
                        elif tools.action_type(event) == 'vote':
                            word_wolf.Vote(event)
                        elif tools.action_type(event).startswith('vote-'):
                            word_wolf.VoteSelect(event)



        # ステータスコード 200 を返却
        return Response({'result': 'true'}, status=200)