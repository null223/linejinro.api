from .line_bot import line_bot_api
from .json import reply_token
from .rich_menu import remove_rich_menu

def SomeError(event):
    line_bot_api.reply_message(
        reply_token(event),
        TextSendMessage(text='エラーが発生しました。')
    )
    remove_rich_menu(event)

