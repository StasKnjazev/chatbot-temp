from flask import Flask, request, abort, send_file
import numpy as np

from .Services.file_handle import read_json
from .Services.load_word2vec_model import load_word2vec_model
from .Services.load_model import load_model
from .Services.log_handle import write_log

from .Core.text_transform import text_transform

from .Api.reply_message import reply_message

MODEL = load_model()
WORD2VEC_MODEL = load_word2vec_model()
API_CONFIG = read_json('Src\config.json')
LABEL = read_json('Src\label.json')
ANSWER = read_json('Src\\answer.json')
LABEL_LIST = sorted(list(LABEL))
MAX_LENG = 29
INTENT = "ready"
old_q = ""
index = 0
REPLY = {}

app = Flask(__name__)

def specialClass(clas):
    labels = ["ปลดล็อก", "รอผู้บริหารรับรอง", "ดำเนินโครงการไม่ได้", "ส่งผู้บริหารรับรองไม่ได้", "วิธีส่งผู้บริหารรับรองแผนพัฒนา", "การบันทึก", "บันทึกไม่ได้", "คัดลอก", "ไม่มีข้อมูล"]
    if clas in labels:
        return False
    else:
        return clas

def get_predict(text):
    global index
    # Pre-process with message
    vec_text = text_transform(WORD2VEC_MODEL, MAX_LENG, text)

    # Prediction
    logit = MODEL.predict(vec_text, batch_size=32)
    index = [ logit[0][pred] for pred in np.argmax(logit, axis=1) ][0]
    if index <= 0.70:
        return False
    else:
        predict = [ LABEL_LIST[pred] for pred in np.argmax(logit, axis=1) ][0]
        return predict

@app.route('/')
def Home():
   return "Hello"

@app.route('/webhook', methods=['POST'])
def webhook(): 
    global index
    # Data from webhook
    payload = request.json
    events = payload['events'][0]
    userId = events['source']['userId']
    msg = events['message']['text'].strip()
    reply_token = events['replyToken']

    if (msg == "ระบบประกันคุณภาพการศึกษา"):
        data = read_json("MapImage\menu.json")
        reply_message(API_CONFIG, reply_token, messages=data)
        return '', 200

    predict = get_predict(msg)
    out_spacial = specialClass(predict)

    if (predict and userId not in REPLY): # สถานะรอรับคำถาม
        if out_spacial: # ถ้าทำนายได้และไม่อยู่ในคลาสพิเศษ
            answer = predict
        elif not out_spacial:   # ถ้าทายได้แต่อยู่ในคลาสพิเศษ
            answer = "ขั้นตอนที่เท่าไรคะ"
            REPLY[userId] = msg
    elif (userId in REPLY):  # สถานะรอรับว่าขั้นที่เท่าไหร่
        msg = (REPLY[userId] + "ขั้น" + msg).replace("ขั้นขั้น", "ขั้น")
        predict = get_predict(msg) # ทำนายใหม่อีกรอบ
        if predict: # ทำนายได้
            answer = predict
        else:   # ทำนายไม่เจอ
            answer = "ไม่พบขั้นตอนที่ถามค่ะ"
        del REPLY[userId]
    else:
        answer = "ไม่เข้าใจคำถามค่ะ กรุณาถามใหม่หรือติดต่อเจ้าหน้าที่ 02-4376631-5 ต่อ 3477 ในวันและเวลาราชการ"

    try:
        answer = ANSWER[answer]
    except:
        pass
    # print(f"user in reply {REPLY}")
    write_log(msg, predict, index, answer)
    reply_message(API_CONFIG, reply_token, answer)
    return '', 200

@app.route('/image', methods=['GET'])
def testImage():
    return send_file('C:\Source\Src\images\step1_7w1040_V2_0.jpg', mimetype='image/jpg')