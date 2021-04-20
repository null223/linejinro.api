import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction
from . import tools
from .tools.line_bot import line_bot_api
from line.models import Room, RoomMember


def StartWordWolf(event):

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(
            text='プレイ人数を教えてください。',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label='5人', data='wordWolf__n-5')),
                QuickReplyButton(action=PostbackAction(label='6人', data='wordWolf__n-6')),
                QuickReplyButton(action=PostbackAction(label='7人', data='wordWolf__n-7')),
                QuickReplyButton(action=PostbackAction(label='8人', data='wordWolf__n-8')),
                QuickReplyButton(action=PostbackAction(label='9人', data='wordWolf__n-9')),
                QuickReplyButton(action=PostbackAction(label='10人', data='wordWolf__n-10'))
            ])
        )
    )

def SetWordWolf(event):
    member = int(tools.action_type(event).split('-')[-1])

    room = Room.objects.create()
    RoomMember.objects.create(room=room, role='wolf')
    for i in range(member -1):
        RoomMember.objects.create(room=room, role='villager')

    member_master = room.room_member_set.all().random()
    member_master.line_id = tools.line_id(event)
    member_master.save()


    app_link = 'https://line.me/R/oaMessage/{account_id}/?{token}'.format(account_id=settings.LINE_ACCOUNT_ID, token=room.token)
    line_bot_api.reply_message(
        tools.reply_token(event),
        [
            TextSendMessage(
                text=str(member)+'人ですね。\n\n参加メンバーにこちらのURLを共有してください。\n'+app_link
            ),
            TextSendMessage(text='続いて、お名前を教えてください。')
        ]
    )

def GetName(event):
    name = tools.data_text(event)
    member = RoomMember.objects.all().filter(line_id=tools.line_id(event))
    member.name = name
    member.save()

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(
            text='「{name}」さんありがとうございます。'.format(name=member.name)
        )
    )


