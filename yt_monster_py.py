import requests
import speedtest
import json
import time
from datetime import datetime
token_task = ''
token_work = ''
id_task = ''
# Версия библиотеки 2.0
def Version():
    return '2.2'
def log(text): #Логирование в фаел лога
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '  ' + text)
        f.close()

def ytmonster_error(error):
    errors = {
        900: 'Лимит, возникает при большом числе запросов.',
        901: 'Лимит, возникает при большом числе ошибок связанных с токеном (1001-1004)',
        902: 'Неверный тип токена. Например: вы используете Ключ доступа (для выполнения заданий) при добавлении задания',
        1001: 'Отсутвует токен',
        1002: 'Не найден токен',
        1003: 'Токен отключен Включите токен на сайте: https://ytmonster.ru/api/#key',
        1004: 'Ошибка токена',
        1101: 'Неправильный тип задания add-account',
        1102: 'Ошибка в ссылке аккаунта',
        1103: 'Ошибка в ссылке аккаунта',
        1301: 'Неправильный параметр get-accounts',
        1401: 'Не найден аккаунт untie',
        1501: 'Не найден аккаунт id_account',
        1502: 'Не найден тип задания по get-task',
        1503: 'Нет заданий данного типа',
        1504: 'timeout - перерыв необходимый для получения нового задания выбранного типа',
        1601: 'Не найден аккаунт id_account',
        1602: 'Задание не выполнено',
        1603: 'Задание было выполнено ранее',
        1701: 'Не найден аккаунт id_account',
        1109: 'Ошибка, проверьте поле error_response',
        1509: 'Ошибка, проверьте поле error_response',
        1609: 'Ошибка, проверьте поле error_response',
        1809: 'Ошибка, проверьте поле error_response',
        1909: 'Ошибка, проверьте поле error_response',
        2009: 'Ошибка, проверьте поле error_response',
        3009: 'Ошибка, проверьте поле error_response'
    }

    error = int(error)
    if error in errors:
        return '', errors[error]
    else:
        return '', 'ok'


def ytmonster_req(token, task, id=''): #запрос к ytmonster и обработка некоторых ошибок
    token_work = token[0]
    token_task = token[1]
    print('ping: ytmonster.ru ...')
    try:
        if task == 'balance':
            req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return '', err
            else:
                return json1["response"]["balance"], 'ok'
        elif task == 'close_client': #закрытие клиента
            req = requests.get('https://app.ytmonster.ru/api/?close-client='+ id +'&token='+ token_work)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return '', err
            else:
                return 'клиент закрыт', 'ok'
            print('ok')
        elif task == 'get_client': #получение работающих клиентов
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
            ID_CLIENT = []
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return a, err
            if req.text == """{"error":0,"response":[]}""":
                return 'not_work', 'Нет рабочих клиентов', ID_CLIENT
            b = 0
            mess = '--------------\n'
            while len(json1['response']) > b:
                mess = mess + '\n👤 Номер клиента: ' + str(b) + '\n🆔 ID клиента: ' + str(json1["response"][b]["id"]) + \
                       '\n🌐 Тип браузера: ' + str(
                    json1["response"][b]["type_browse"]["name"]) + '\n⏳ Осталось просмотреть: ' + str(
                    json1["response"][b]["info"]["sec"]) + ' сек.' + \
                       '\n📺 Ссылка на просмотриваемое видео: https://www.youtube.com/watch?v=' + \
                       json1["response"][b]["info"]["http"] + \
                       '\n❌ Количество ошибок при просмотре: ' + str(json1["response"][b]["info"]["error"]) + \
                       '\n🌐 IP клиента: ' + str(json1["response"][b]["info"]["ip"]) + \
                       '\n🔴 Статус аккаунта ютуб:' + str(json1["response"][b]["accounts"]["youtube"]) + \
                       '\n👀 Просмотрел видео: ' + str(json1["response"][b]["data"]["count"]) + \
                       '\n💰 Заработал за просмотр видео: ' + str(json1["response"][b]["data"]["coin"]) + ' COIN' + \
                       '\n✅ Выполнил заданий: ' + str(json1["response"][b]["data"]["count_task"]) + \
                       '\n💰 Заработал за выполнения заданий: ' + str(json1["response"][b]["data"]["coin_task"]) + '\n--------------'
                ID_CLIENT.append(json1["response"][b]["id"])
                b = b + 1
            return mess, err, ID_CLIENT


        elif task == 'my_task': # получения списка заданий
            req = requests.get('https://app.ytmonster.ru/api/?my-tasks=' + id +'&offset=0&token=' + token_task)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if '''{"error":0,"response":[]}''' == req.text:
                return 'Нет заданий такого типа!', err
            if err != 'ok':
                return '', err
            i = len(json1['response'])
            b = 0
            mess = ''
            while i > b:
                time.sleep(1)
                mess = mess + '\n'+ 'Нужно выполнить: ' + json1["response"][b]["need"] + '/Выполнено: '+ json1["response"][b]["now"] +'\nКоличество выполнения в час: '+ json1["response"][b]["valh"] +'\nID: ' + json1["response"][b]["id"] + '\n' + 'Сылка: ' + json1["response"][b]["url"] + '\n' + 'Тип: ' + json1["response"][b]["soc"] + '\n-----------'
                b = b + 1
            return mess, err
        elif task == 'test':
            req = requests.get('https://app.ytmonster.ru/api/?get-task=[type]&id_account=[id_account]&token=' + token_task)
        else:
            log('Ошибка выполнения функции ytmonster! Нет указания что делать')
            return '', 'Ошибка выполнения функции ytmonster! Нет указания что делать'  
    except requests.exceptions.RequestException:
        time.sleep(10)
        print('ping err')
        err = 'Ошибка запроса к API ytmonster! Работает ли сайт?'
        return '', err
    return req, 'ok'

def test_speed(times): #сколько раз замерить скорость интернета
    st = speedtest.Speedtest()
    download_speeds = []
    upload_speeds = []
    for i in range(times):
        download_speed = st.download() / 1000000  # скорость загрузки в Мбит/с
        upload_speed = st.upload() / 1000000  # скорость отгрузки в Мбит/с
        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        print(f"Скорость загрузки {i + 1}: {download_speed:.2f} Мбит/с")
        print(f"Скорость отгрузки {i + 1}: {upload_speed:.2f} Мбит/с")
    avg_download_speed = sum(download_speeds) / len(download_speeds)
    avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
    return f"Средняя скорость загрузки: {avg_download_speed:.2f} Мбит/с" + '\n' + f"Средняя скорость отгрузки: {avg_upload_speed:.2f} Мбит/с"

# Beta функция на данный момент не доработана

def yt_monster_create_task_tg(task, task_href, token, reactions='', task_count=10, task_valh=0, task_coin= 0):
    token_work = token[0]
    token_task = token[1]
    if task == 'like_tg':
        if reactions == '':
            return '', 'err'
        import json
        import base64
        task_reactions = base64.b64encode(json.dumps({"reactions": reactions}).encode()).decode()
        print(task_reactions)
        print(str(base64.b64encode(task_href.encode()).decode()))
        url = 'https://app.ytmonster.ru/api/?add-task=tg&href=' + str(base64.b64encode(task_href.encode()).decode()) + '&count=' + str(task_count) + '&type=like&valh=' + str(task_valh) + '&token=' + token_task + '&params=' + task_reactions
        req = requests.get(url)
        json1 = json.loads(req.text)
        a, err = ytmonster_error(json1["error"])
        if err != 'ok':
            return json1["error_response"], err
        req = 'Статус: ' + str(json1["response"]["status"]) + '\nID: ' + str(json1["response"]["id"])
        return req, 'ok'
    elif task == 'view_tg':
        import json
        import base64
        print(str(base64.b64encode(task_href.encode()).decode()))
        url = 'https://app.ytmonster.ru/api/?add-task=tg&href=' + str(base64.b64encode(task_href.encode()).decode()) + '&count=' + str(task_count) + '&type=view&valh=' + str(task_valh) + '&coin=' + str(task_coin) + '&token=' + token_task
        req = requests.get(url)
        json1 = json.loads(req.text)
        a, err = ytmonster_error(json1["error"])
        if err != 'ok':
            return json1["error_response"], err
        req = 'Статус: ' + str(json1["response"]["status"]) + '\nID: ' + str(json1["response"]["id"])
        return req, 'ok'