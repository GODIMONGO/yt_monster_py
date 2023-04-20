import requests
import speedtest
import json
import time
from datetime import datetime
token_task = ''
token_work = ''
id_task = ''
# Версия библиотеки 1.8
def Versoin():
    return '1.8'


def replace_line_in_file(file_path, line_number, replacement):
    """
    Заменяет указанную строку в файле на указанное значение.

    Args:
    file_path (str): Путь к файлу, в котором нужно заменить строку.
    line_number (int): Номер строки в файле, которую нужно заменить.
    replacement (str): Значение, на которое нужно заменить строку.

    Raises:
    FileNotFoundError: Если указанный файл не найден.
    IndexError: Если указанный номер строки выходит за пределы файла.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return 'err', (f'Файл "{file_path}" не найден')
    try:
        lines[line_number - 1] = replacement + '\n'
    except IndexError:
        return 'err', (f'Номер строки {line_number} выходит за пределы файла "{file_path}"')
    with open(file_path, 'w') as f:
        f.writelines(lines)
        return 'ok', 'ok'


def read_file(file_path):
    """
    Читает содержимое файла и возвращает его в виде списка строк.

    Args:
    file_path (str): Путь к файлу, который нужно прочитать.

    Returns:
    list[str]: Список строк с содержимым файла.

    Raises:
    FileNotFoundError: Если указанный файл не найден.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            return 'ok', lines
    except FileNotFoundError:
        return 'err', (f'Файл "{file_path}" не найден')


def log(text): #Логирование в фаел лога
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '  ' + text)
        f.close()

def ytmonster_error(error):#обработка ошибок
    error = int(error)
    if error == 900:
        err = 'Лимит, возникает при большом числе запросов.'
        return '', err
    elif error == 901:
        err = 'Лимит, возникает при большом числе ошибок связанных с токеном (1001-1004)'
        return '', err
    elif error == 902:
        err = 'Неверный тип токена. Например: вы используете Ключ доступа (для выполнения заданий) при добавлении задания'
        return '', err
    elif error == 1001:
        err = 'Отсутвует токен'
        return '', err
    elif error == 1002:
        err = 'Не найден токен'
        return '', err
    elif error == 1003:
        err = "Токен отключен Включите токен на сайте: https://ytmonster.ru/api/#key"
        return '', err
    elif error == 1004:
        err = 'Ошибка токена'
        return '', err
    elif error == 1101:
        err = 'Неправильный тип задания add-account'
        return '', err
    elif error == 1102 or error == 1103:
        err = 'Ошибка в ссылке аккаунта'
        return '', err
    elif error == 1301:
        err = 'Неправильный параметр get-accounts'
        return '', err
    elif error == 1401:
        err = 'Не найден аккаунт untie'
        return '', err
    elif error == 1501:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1502:
        err = 'Не найден тип задания по get-task'
        return '', err
    elif error == 1503:
        err = 'Нет заданий данного типа'
        return '', err
    elif error == 1504:
        err = 'timeout - перерыв необходимый для получения нового задания выбранного типа'
        return '', err
    elif error == 1601:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1602:
        err = 'Задание не выполнено'
        return err
    elif error == 1603:
        err = 'Задание было выполнено ранее'
        return '', err
    elif error == 1701:
        err = 'Не найден аккаунт id_account'
        return '', err
    elif error == 1109 or error == 1509 or error == 1609 or error == 1809 or error == 1909 or error == 2009 or error == 3009:
        err = 'Ошибка, проверьте поле error_response'
        return '', err
    else:
        print('ok')
        err = 'ok'
        return '', err

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
        elif task == 'close_client':
            print('ok')
        elif task == 'get_client':
            req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
            print(req.text)
            json1 = json.loads(req.text)
            a, err = ytmonster_error(json1["error"])
            if err != 'ok':
                return a, err
            if req.text == """{"error":0,"response":[]}""":
                return '', 'Нет рабочих клиентов'
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
                       '\n💰 Заработал за выполнения заданий: ' + str(
                    json1["response"][b]["data"]["coin_task"]) + '\n--------------'
                b = b + 1
            return mess, err


        elif task == 'my_task':
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

def yt_monster_create_task_tg(task, task_href, token, reactions='', task_count=10, task_valh=0, task_coin=400):
    if task == 'like':
        if reactions == '':
            return '', 'err'
        import json
        import base64
        task_reactions = base64.b64encode(json.dumps({"reactions": reactions}).encode()).decode()
        print(task_reactions)
        print(str(base64.b64encode(task_href.encode()).decode()))
        url = 'https://app.ytmonster.ru/api/?add-task=tg&href=' + str(base64.b64encode(task_href.encode()).decode()) + '&count=' + str(task_count) + '&type=like&valh=' + str(task_valh) + '&coin=' + str(task_coin) + '&token=' + token + '&params=' + task_reactions
        req = requests.get(url)
        json1 = json.loads(req.text)
        a, err = ytmonster_error(json1["error"])
        if err != 'ok':
            return json1["error_response"], err
        req = 'Статус: ' + str(json1["response"]["status"]) + '\nID: ' + str(json1["response"]["id"])
        return req, 'ok'
    elif task == 'view':
        import json
        import base64
        print(str(base64.b64encode(task_href.encode()).decode()))
        url = 'https://app.ytmonster.ru/api/?add-task=tg&href=' + str(base64.b64encode(task_href.encode()).decode()) + '&count=' + str(task_count) + '&type=view&valh=' + str(task_valh) + '&coin=' + str(task_coin) + '&token=' + token
        req = requests.get(url)
        json1 = json.loads(req.text)
        a, err = ytmonster_error(json1["error"])
        if err != 'ok':
            return json1["error_response"], err
        req = 'Статус: ' + str(json1["response"]["status"]) + '\nID: ' + str(json1["response"]["id"])
        return req, 'ok'
