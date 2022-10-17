import datetime

def write_log(input, predict, index, answer):
    x = datetime.datetime.now()
    with open('log.csv', mode='a', encoding='utf-8') as f:
        f.write(f'{x.strftime("%d/%m/%Y:%H:%M:%S")},{input},{predict},{index * 100 // 1}%,{answer}\n')
        f.close()
