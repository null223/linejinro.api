from django.conf import settings
from line.models import RichMenu as ModelRichMenu
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, PostbackAction
from .line_bot import line_bot_api
from .json import line_id

def set_rich_menu(event):
    line_bot_api.link_rich_menu_to_user(line_id(event), ModelRichMenu.objects.all().first().menu_id)

def remove_rich_menu(event):
    line_bot_api.unlink_rich_menu_from_user(line_id(event))

def get_rich_menu():
    result = False

    width = 2500
    height = 1686
    try:
        # define a new richmenu
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=width, height=height),
            selected = True,
            name = 'richmenu',
            chat_bar_text = 'メニュー',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=height, height=height),
                    action=PostbackAction(label='ストーリーをすすめる', data='next_step')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=height, y=0, width=width - height, height=height/2),
                    action=PostbackAction(label='中止', data='stop')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=height, y=height/2, width=width - height, height=height/2),
                    action=PostbackAction(label='投票', data='vote')
                )
            ]
        )
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

        # upload an image for rich menu
        path = settings.STATIC_ROOT + 'images/richmenu.jpeg'
        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

        result = True

    except Exception:
        result = False

    print(richMenuId, 'richmenu-id result: '+str(result))
