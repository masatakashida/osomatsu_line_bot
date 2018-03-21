# -*- encoding: utf-8 -*-
import json
import random
import requests
import base64
import hashlib
import hmac

channel_secret = "593f3ff1e6a03ca15b36d50d8d56af49" # Channel secret string

from django.shortcuts import render
from django.http import HttpResponse

from load_serif import osomatsu_serif  # 先ほどのおそ松のセリフ一覧をimport

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'ufPaV2RYTu8GHaNFJKGlWXL4fON5uKyhiulyOk7sT57wtVci1HjUQaPr0UUWjk8ktnpVlEP4qyheNcF3I6n7HIeQTTRiAzs2xTC84ir5rC+zdwknS9UjDXD5ARAWKHohRpbyaDkygicvmlRTWsAJhQdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")

def reply_text(reply_token, text):
    reply = random.choice(osomatsu_serif)
    payload = {
        "replyToken":reply_token,
        "messages":[
            {
                "type":"text",
                "text": reply
            }
        ]
    }
    body = request.body # Request body string
    hash = hmac.new(channel_secret.encode('utf-8'),
        body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    # Compare X-Line-Signature request header and the signature

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用