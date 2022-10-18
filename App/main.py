from flask import Flask, request, send_from_directory, render_template
import numpy as np

from .Services.file_handle import *
from .Services.load_model import *
from .Core.text_processing import *
from .Api.reply_message import reply_message

MODEL = load_model("Model\my_model_1")
WORD2VEC_MODEL = load_word2vec_model()
CONFIG = read_json('Src\config.json')
DATA = read_json('Src\data.json')

REPLY = {}

app = Flask(__name__)

def get_predict(text, label, used_model):
    # Pre-process with message
    vec_text = text_transform(used_model, WORD2VEC_MODEL, text, read_text('Src\stop_words.txt'))

    # Prediction
    logit = used_model.predict(vec_text, batch_size=32, verbose=0)
    index = [ logit[0][pred] for pred in np.argmax(logit, axis=1) ][0]
    if index <= CONFIG["model"]["conf"]:
        return [False, index]
    else:
        predict = [ label[pred] for pred in np.argmax(logit, axis=1) ][0].lower()
        return [predict, index]

@app.route('/')
def Home():
   return render_template("App\Views\index.html")

@app.route('/webhook', methods=['POST'])
def webhook(): 
    # Data from webhook 
    payload = request.json
    events = payload['events'][0]
    userId = events['source']['userId']
    msg = events['message']['text'].strip().lower()
    reply_token = events['replyToken']

    # label from data
    label = sorted([i.lower() for i in list(DATA["label"])])
    special_class = [i.lower() for i in list(DATA['special_class'])]
    mapImage = [i.lower() for i in list(DATA['mapImage'])]
    
    is_match_mapImage = richMenu(msg, mapImage)
    if (is_match_mapImage):
        content = DATA['mapImage'][msg]
        try:
            answer = content['answer']
            path = content['path']
            data = read_json(path)
            reply_message(CONFIG["api"], reply_token, messages=data)
        except:
            answer = content
            reply_message(CONFIG['api'], reply_token, answer)
        return '', 200

    predict, index = get_predict(msg, label, MODEL)
    out_spacial = specialClass(predict, special_class)

    if (predict and userId not in REPLY): # สถานะรอรับคำถาม
        if out_spacial: # ถ้าทำนายได้และไม่อยู่ในคลาสพิเศษ
            answer = predict
        elif not out_spacial:   # ถ้าทายได้แต่อยู่ในคลาสพิเศษ
            answer = "ขั้นตอนที่เท่าไรคะ"
            REPLY[userId] = msg
    elif (userId in REPLY):  # สถานะรอรับว่าขั้นที่เท่าไหร่
        msg = (REPLY[userId] + "ขั้น" + msg).replace("ขั้นขั้น", "ขั้น")
        predict, index = get_predict(msg) # ทำนายใหม่อีกรอบ
        if predict: # ทำนายได้
            answer = predict
        else:   # ทำนายไม่เจอ
            answer = "ไม่พบขั้นตอนที่ถามค่ะ"
        del REPLY[userId]
    else:
        answer = "ไม่เข้าใจคำถามค่ะ กรุณาถามใหม่หรือติดต่อเจ้าหน้าที่ 02-4376631-5 ต่อ 3477 ในวันและเวลาราชการ"

    try:
        ANSWER = dict((k.lower(), v.lower()) for k, v in DATA['answer'].items())
        answer = ANSWER[answer.lower()]
    except:
        pass
    # print(f"user in reply {REPLY}")
    write_log(msg, predict, index, answer)
    reply_message(CONFIG['api'], reply_token, answer)
    return '', 200

@app.route('/images/<path:dirname>/<path:size>', methods=['GET'])
def getImage(dirname, size):
    return send_from_directory(f'C:\Source\Src\images\{dirname}', path=f'{size}')