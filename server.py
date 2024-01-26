import asyncio
import socketio
import logging
import json
import time
import uvicorn
from pprint import pprint
import multiprocessing
from repo import (
  findYoutubeLiveChatNotSent,
  markLiveChatAsSent,
)
loop = asyncio.get_event_loop()
sio = socketio.AsyncServer(
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True,
    async_mode='asgi'
)
app = socketio.ASGIApp(sio)
async def consume_live_chat_coroutine() -> None:
    try:
        comment_list: list = findYoutubeLiveChatNotSent()
        if len(comment_list) > 0:
            for comment in comment_list:
                logging.info(f'Youtube Comment {comment}')
                markLiveChatAsSent(comment.get('_id'))
                await sio.emit('livechat::receive', json.dumps(comment, default=str))
                await asyncio.sleep(5)
        else:
            logging.info(f'There are not any Youtube Comment')
            await sio.emit('livechat::receive', json.dumps('', default=str))
    except asyncio.CancelledError:
        logging.info('Stop sending livechat')
@sio.event 
async def connect(sid, environ):
    logging.info(f'Client connected: {sid}')
task = None
@sio.on('livechat::consume')
async def consume_livechat(sid, data=None):
    loop = asyncio.get_event_loop()
    coroutine = consume_live_chat_coroutine()
    global task
    task = loop.create_task(coroutine)
@sio.event 
async def disconnect(sid):
    logging.info(f'Client disconnected: {sid}')
    loop = asyncio.get_event_loop()
    global task
    task.cancel()
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # uvicorn.run(app, host='localhost', port=8000)
    uvicorn.run(app, port=8000)
