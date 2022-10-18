import json
import datetime

def read_json(path):
    f = open(path, encoding="utf8")
    data = json.load(f)
    f.close()
    return data

def write_log(input, predict, index, answer):
    x = datetime.datetime.now()
    with open('Src\Log\log1.csv', mode='r', encoding='utf-8') as f:
        last_line = [i.strip() for i in f.readlines()][-1]
        f.close()
    number = last_line.split(',')[0]
    if number == '': number = 0
    else: number = int(number)

    with open('Src\Log\log1.csv', mode='a', encoding='utf-8') as f:
        f.write(f'{number + 1},{x.strftime("%d/%m/%Y:%H:%M:%S")},{input},{predict},{index * 100 // 1}%,{answer}\n')
        f.close()

def read_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        read_word = [i.strip() for i in f.readlines()]
        f.close()
    return read_word