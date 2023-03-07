import requests
import json
start = False
def start():
    global start
    if start != True:
        start = True
    print('Версия библиотеки 1.0')

def error_yt_monster(error): #вы можете сами обработать ошибку с помощью этой функции
    if start != True:
        print('Вы забыли выполнить функцию start!')
        return '', 'Вы забыли выполнить функцию start!'
    error = int(error)
    if error == 900:
        err = 'Лимит, возникает при большом числе запросов.'
        return err
    elif error == 901:
        err = 'Лимит, возникает при большом числе ошибок связанных с токеном (1001-1004)'
        return err
    elif error == 902:
        err = 'Неверный тип токена. Например: вы используете Ключ доступа (для выполнения заданий) при добавлении задания'
        return err
    elif error == 1001:
        err = 'Отсутвует токен'
        return err
    elif error == 1002:
        err =  'Не найден токен'
        return err
    elif error == 1003:
        err = "Токен отключен Включите токен на сайте: https://ytmonster.ru/api/#key"
        return err
    elif error == 1004:
        err = 'Ошибка токена'
        return err
    elif error == 1101:
        err = 'Неправильный тип задания add-account'
        return err
    elif error == 1102 or error == 1103:
        err = 'Ошибка в ссылке аккаунта'
        return err
    elif error == 1301:
        err = 'Неправильный параметр get-accounts'
        return err
    elif error == 1401:
        err = 'Не найден аккаунт untie'
        return err
    elif error == 1501:
        err = 'Не найден аккаунт id_account'
        return err
    elif error == 1502:
        err = 'Не найден тип задания по get-task'
        return err
    elif error == 1503:
        err = 'Нет заданий данного типа'
        return err
    elif error == 1504:
        err = 'timeout - перерыв необходимый для получения нового задания выбранного типа'
        return err
    elif error == 1601:
        err = 'Не найден аккаунт id_account'
        return err
    elif error == 1602:
        err = 'Задание не выполнено'
        return err
    elif error == 1603:
        err = 'Задание было выполнено ранее'
        return err
    elif error == 1701:
        err = 'Не найден аккаунт id_account'
        return  err
    elif error == 1109 or error == 1509 or error == 1609 or error == 1809 or error == 1909 or error == 2009 or error == 3009:
        err = 'Ошибка, проверьте поле error_response'
        return err
    else:
        print('ok')
        err = 'ok'
        return err

def ytmonster_balance(token_work): #получение баланса
    if start != True:
        print('Вы забыли выполнить функцию start!')
        return '', 'Вы забыли выполнить функцию start!'
    try:
        req = requests.get('https://app.ytmonster.ru/api/?balance=get&token=' + token_work) #получение баланса
        json1 = json.loads(req.text)
        error = (json1["error"])
        err = error_yt_monster(error)
        if err == 'ok':
            return (json1["response"]["balance"]), ''
        else:
            return '', err
    except requests.exceptions.RequestException as e:
        print('ping err')
        err = 'Ошибка запроса к API ytmonster! Работает ли сайт?'
        return '', err
def get_client(token_work):
    if start != True:
        print('Вы забыли выполнить функцию start!')
        return '', 'Вы забыли выполнить функцию start!'
    req = requests.get('https://app.ytmonster.ru/api/?get-clients=get&token=' + token_work)
    json1 = json.loads(req.text)
    error = (json1["error"])
    err = error_yt_monster(error)
    if req.text == """{"error":0,"response":[]}""":
        return req.text, 'Нет рабочих клиентов'
    if err == 'ok':
        return req, err
    else:
        return '', err