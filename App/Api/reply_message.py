import json
import requests

def reply_message(CONFIG, reply_token, message="", messages=None):
    channel_access_token = CONFIG["channel_access_token"]
    LINE_API = CONFIG["LINE_API"] 

    headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer {%s}'%channel_access_token
    }
    if messages == None:
        messages = {
                    "type": "text",
                    "text": f"{message}"
                    }
    data = {
        "replyToken": f"{reply_token}",
        "messages":[ messages, 
            # for more than Sone message
            # {
            # "type": "text",
            # "text": "May I help you?"
            # }
        ]
    }
    data = json.dumps(data)
    requests.post(LINE_API, headers=headers, data=data)