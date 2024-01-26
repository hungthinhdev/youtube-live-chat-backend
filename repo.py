import pyrebase
from pprint import pprint
from collections import OrderedDict
import time
import logging
from datetime import datetime
YOUTUBE_LIVE_CHAT_COMMENTS: str = 'youtube_live_chat_comments'
COMMENTS_SENT: str = 'comments_sent'
firebaseConfig = {
  "apiKey": "AIzaSyCDExtQfUEqEzEaxzPTrr9fbUrc8sH5Pqs",
  "authDomain": "live-chat-500be.firebaseapp.com",
  "databaseURL": "https://live-chat-500be-default-rtdb.firebaseio.com",
  "projectId": "live-chat-500be",
  "storageBucket": "live-chat-500be.appspot.com",
  "messagingSenderId": "677369051796",
  "appId": "1:677369051796:web:4ed46600b87ec8cc03d281",
  "measurementId": "G-GGPR2N6S6Y"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
def insertOneYoutubeLiveChat(live_chat_comment: dict = None) -> None:
    response = db.child(YOUTUBE_LIVE_CHAT_COMMENTS).push(live_chat_comment)
    logging.info(f"Youtube live chat's Inserted key: {response['name']}")
def findYoutubeLiveChatNotSent():
    response = db.child(YOUTUBE_LIVE_CHAT_COMMENTS).get()
    liveChatComments = response.val()
    response = db.child(COMMENTS_SENT).get()
    if response.val() is None:
        if liveChatComments is None or not isinstance(liveChatComments, OrderedDict):
            return []
        else:
            result: list = []
            for live_chat_comment_id in liveChatComments.keys():
                live_chat_comment = liveChatComments.get(live_chat_comment_id)
                live_chat_comment['_id'] = live_chat_comment_id
                result.append(live_chat_comment)
            return result
    else:
        if liveChatComments is None or not isinstance(response.val() , OrderedDict):
            return []
        else:
            sentCommentIds = response.val().values()
            result: list = []
            for live_chat_comment_id in liveChatComments.keys():
                if live_chat_comment_id not in sentCommentIds:
                    live_chat_comment = liveChatComments.get(live_chat_comment_id)
                    live_chat_comment['_id'] = live_chat_comment_id
                    result.append(live_chat_comment)
            return result
def markLiveChatAsSent(id: str = ''):
    response = db.child(COMMENTS_SENT).push(id)
    pprint(f"Already mark comment with id: {response['name']} as read")
def findOneById(id: str = ''):
    response = db.child(YOUTUBE_LIVE_CHAT_COMMENTS).child(id).get()
    pprint(response.val())
    return response.val()
def findAllYoutubeLiveChat():
    response = db.child(YOUTUBE_LIVE_CHAT_COMMENTS).get()
    pprint(response.val())
    return response.val()
if __name__ == '__main__':
    for comment in findYoutubeLiveChatNotSent():
        pprint(comment)

