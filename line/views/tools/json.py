import datetime


def line_id(event):
    return event['source']['userId']

def reply_token(event):
    return event['replyToken']

# message or postback
def message_type(event):
    return event['type']

def data_type(event):
    return event['message']['type']

def data_text(event):
    return event['message']['text']

def action_type(event):
    return event['postback']['data']
