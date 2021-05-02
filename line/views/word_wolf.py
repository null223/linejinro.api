import json, collections
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction
from . import tools
from .tools.line_bot import line_bot_api
from line.models import Room, RoomMember, WordWolfItem, MemberAction


def StartWordWolf(event):

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(
            text='プレイ人数を教えてください。',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label='2人(開発用)', data='wordWolf__n-2')),

                QuickReplyButton(action=PostbackAction(label='4人', data='wordWolf__n-4')),
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

    room = Room.objects.create(word=WordWolfItem.objects.all().random())
    RoomMember.objects.create(room=room, role='wolf')
    for i in range(member -1):
        RoomMember.objects.create(room=room, role='villager')

    member_master = room.room_member_set.all().random()
    member_master.line_id = tools.line_id(event)
    member_master.save()


    app_link = 'https://line.me/R/oaMessage/{account_id}/?token_at{token}'.format(account_id=settings.LINE_ACCOUNT_ID, token=room.token)
    line_bot_api.reply_message(
        tools.reply_token(event),
        [
            TextSendMessage(
                text=str(member)+'人ですね。\n\n参加メンバーにこちらのURLを共有してください。'
            ),
            TextSendMessage(text=app_link),
            TextSendMessage(text='続いて、お名前を教えてください。')
        ]
    )

def JoinRoom(event):
    member = Room.objects.all().get(token=tools.data_text(event).split('token_at')[-1]).room_member_set.all().random()
    member.line_id = tools.line_id(event)
    member.save()

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(text='ありがとうございます。\n続いて、お名前を教えてください。')
    )

def GetName(event):
    name = tools.data_text(event)
    member = RoomMember.objects.line().get(line_id=tools.line_id(event))
    member.name = name
    member.status = 'playing'
    member.save()

    tools.set_rich_menu(event)

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(
            text='{name}さんありがとうございます。\n全員の入力が完了しましたら「ストーリーをすすめる」を押してください。'.format(name=member.name)
        )
    )

def VoteResult(event, room):
    selects = []
    for mem in room.room_member_set.line():
        action = mem.member.latest()
        selects.append(action.select)

    selected_list = collections.Counter(selects).most_common()
    most_count = selected_list[0][1]
    most_list = []
    for sel in selected_list:
        if sel[1] == most_count:
            most_list.append(sel[0])

    wolf_member = room.room_member_set.line().filter(role='wolf').first()

    if len(most_list) == 1:
        find_success = '見事少数派を見つけられました。\nこのまま行くと多数派の勝利となりますが、少数派の方は多数派のお題はなんだったでしょうか？\n当てられたら大逆転勝利です！\n（ゲームの進行はここまでになります。お疲れ様でした！）'
        find_failed = '少数派の方の勝利です。\nお疲れ様でした！'
        text = find_success if most_list[0] == wolf_member else find_failed
        line_bot_api.reply_message(
            tools.reply_token(event),
            [
                TextSendMessage(text='投票の結果選ばれたのは「{member}さん」でした。'.format(member=most_list[0].name)),
                TextSendMessage(text='そして今回の少数派は「{member}さん」でした。'.format(member=wolf_member.name)),
                TextSendMessage(text=text)
            ]
        )
        member = RoomMember.objects.line().get(line_id=tools.line_id(event))
        member.is_dead = True
        member.save()

        if not member.room.room_member_set.all().exclude(is_dead=True).exists():
            for mem in room.room_member_set.line():
                mem.status = "ended"
                mem.save()

            member.room.active = False
            member.room.save()
        tools.remove_rich_menu(event)
    else:
        most_member_text = ''
        for mem in most_list:
            most_member_text += ' ・{member}さん\n'.format(member=mem.name)

        line_bot_api.reply_message(
            tools.reply_token(event),
            [
                TextSendMessage(text='投票の結果選ばれたのは\n{members}でした。'.format(members=most_member_text)),
                TextSendMessage(text='票が分かれてしまったので、もう一度議論をして「投票」を始めてください。')
            ]
        )

def NextStep(event):
    member = RoomMember.objects.line().filter(line_id=tools.line_id(event))
    if not member.exists():
        tools.SomeError(event)

    member = member.first()

    is_wolf = member.role == 'wolf'

    # vote
    _action = MemberAction.objects.all().filter(member=member)
    action = _action.latest() if _action.exists() else None

    room = member.room

    noname_member = room.room_member_set.line().filter(name__isnull=True)
    # notvoted_member = room.room_member_set.line().filter(member_action_set__isnull=True)
    notvoted_member_list = []
    for mem in room.room_member_set.line():
        mem_action = MemberAction.objects.filter(member=mem)
        if not mem_action.exists():
            notvoted_member_list.append(mem)

    if noname_member.exists() or (action and notvoted_member_list):
        line_bot_api.reply_message(
            tools.reply_token(event),
            TextSendMessage(text='ほかのプレイヤーの選択をお待ちください。')
        )

    if not noname_member.exists():
        if not action:
            line_bot_api.reply_message(
                tools.reply_token(event),
                [
                    TextSendMessage(text='今回のあなたのお題は「{theme}」です。\n少数派は誰か。自分が少数派と気づいた時に多数派のお題は何か。\n慎重に議論してみましょう！'.format(theme=room.word.wolf_img if is_wolf else room.word.vil_img)),
                    TextSendMessage(text='議論時間は各自で調整お願いします。\n議論が終わったら「投票」を押して投票を始めてください。')
                ]
            )

        else:
            VoteResult(event, room)

def StopToMenu(event):
    member = RoomMember.objects.line().filter(line_id=tools.line_id(event))
    if member.exists():
        member = member.first()
        member.status = 'ended'
        member.save()
        if not member.room.room_member_set.all().exclude(status='ended').exists():
            member.room.active = False
            member.room.save()

    tools.remove_rich_menu(event)

    line_bot_api.reply_message(
        tools.reply_token(event),
        TextSendMessage(text='ルームから退出しました。')
    )


def Vote(event):
    member = RoomMember.objects.line().filter(line_id=tools.line_id(event))
    if not member.exists():
        tools.SomeError(event)

    member = member.first()

    room = member.room

    noname_member = room.room_member_set.line().filter(name__isnull=True)

    if noname_member.exists():
        line_bot_api.reply_message(
            tools.reply_token(event),
            TextSendMessage(text='ほかのプレイヤーの選択をお待ちください。')
        )
    else:
        quick_list = []
        for mem in room.room_member_set.line():
            quick_list.append(
                QuickReplyButton(
                    action=PostbackAction(
                        label='{name}さん'.format(name=mem.name),
                        data='vote-{id}'.format(id=str(mem.id))
                    )
                )
            )

        line_bot_api.reply_message(
            tools.reply_token(event),
            TextSendMessage(
                text='投票はこちらから',
                quick_reply=QuickReply(items=quick_list)
            )
        )

def VoteSelect(event):
    member = RoomMember.objects.line().filter(line_id=tools.line_id(event))
    if not member.exists():
        tools.SomeError(event)

    member = member.first()

    select_member_id = int(tools.action_type(event).split('-')[-1])
    select_member = member.room.room_member_set.line().get(id=select_member_id)
    MemberAction.objects.create(member=member, select=select_member)

    line_bot_api.reply_message(
        tools.reply_token(event),
        [
            TextSendMessage(text='投票先：「{name}さん」'.format(name=select_member.name)),
            TextSendMessage(text='全員の投票が完了しましたら、「ストーリーをすすめる」を押してください。')
        ]
    )



