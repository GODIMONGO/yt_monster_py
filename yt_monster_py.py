import base64
import requests
from pytube import YouTube

url_clifl = "https://api.clifl.com/"


def version():
    return 4.0


def balance_coin(token):
    global url_clifl

    params = {
        "action": "user-balance",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return response['response']['coin'], 'NO'


def balance_many(token):
    global url_clifl

    params = {
        "action": "user-balance",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return int(response['response']['money']), 'NO'


def add_account(token, platform, url):
    global url_clifl

    params = {
        "action": "accounts-add",
        "platform": str(platform),
        "url": str(url),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':

        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    response = {'account': str(response['response']['account']), 'task': str(response['response']['task']),
                'url': str(response['response']['url']), 'type': str(response['response']['type'])}
    return response, 'NO'


def check_account(token, account, task):
    global url_clifl

    params = {
        "action": "accounts-check",
        "account": str(account),
        "task": str(task),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return str(response['status']), 'NO'


def get_task_list(token, platform, offset=0, limit=100):
    global url_clifl
    data = {
        "action": "mytasks-get",
        "platform": str(platform),
        "offset": str(offset),
        "limit": str(limit),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()
    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    elif not response['response']:
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', 'Нет заданий данного типа'
    else:
        task_list = response['response']
        processed_tasks = []

        for task in task_list:
            processed_task = {}
            processed_task['id'] = int(task['id'])
            processed_task['platform'] = str(task['platform'])
            if task['type'] == 'viewg':
                processed_task['guarantee'] = task['guarantee']
            processed_task['type'] = str(task['type'])
            processed_task['short_url'] = str(task['short_url'])
            processed_task['url'] = str(task['url'])
            if task['valh'] == '&infin;':
                processed_task['valh'] = 0
            else:
                processed_task['valh'] = int(task['valh'])
            processed_task['need'] = int(task['need'])
            processed_task['now'] = int(task['now'])
            processed_tasks.append(processed_task)

        return processed_tasks, 'NO'


def add_task(token, platform, href, count, coin, valh=0, sec=None, comments=None, sec_max=None, params=None, type=None,
             guarantee=False):
    global url_clifl
    from urllib.parse import urlparse, urlsplit, urlunsplit
    task = {"action": "mytasks-add", "token": str(token), "platform": str(platform), "count": str(count),
            "valh": str(valh)}
    if platform == 'tg' and type == 'view':
        task["coin"] = '100'
    if platform == 'tiktok' and type == 'view':
        task["coin"] = '1'
    else:
        task["coin"] = str(coin)
    if guarantee == True:
        task["guarantee"] = '1'
    if type != None:
        task["type"] = str(type)

    href = href_format(href, platform)
    href = base64.b64encode(href.encode('utf-8'))
    href = href.decode('utf-8')
    task["href"] = str(href)

    if platform == "ytview":
        task["sec"] = str(sec)
    if platform == "ytcomm":
        comments = base64.b64encode(comments.encode('utf-8'))
        comments = comments.decode('utf-8')
        task["comments"] = str(comments)
    if platform == 'ytview' and sec_max != None:
        task["sec_max"] = sec_max

    if params != None:
        task["params"] = str(params)

    response = requests.post(url_clifl, data=task).json()
    if response['status'] != 'success' and response['error'] != '':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
    return response['id'], 'NO'

def task_remove(token, platform,  id):
    global url_clifl

    params = {
        "action": "mytasks-remove",
        "platform": str(platform),
        "id": str(id),
        "token": str(token)
    }
    response = requests.post(url_clifl, data=params).json()

    if response['status'] != 'success':
        try:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error']
        except:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response['error_response']
    return str(response['status']), 'NO'


def task_addition(token, platform, id, count):
    global url_clifl
    data = {
        "action": "mytasks-addition",
        "id": str(id),
        "platform": str(platform),
        "count": str(count),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()

    if response['status'] != 'success':
        if response.get('error') != None:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
        else:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error_response')
    else:
        return str(response['status']), 'NO'


def streams_add(token, platform, nickname, tariff, currency, duration, viewers=0, ratio=0):
    global url_clifl
    data = {
        "action": "streams-add",
        "platform": str(platform),
        "nickname": str(nickname),
        "tariff": str(tariff),
        "currency": str(currency),
        "duration": str(duration),
        "token": str(token)
    }
    if viewers != 0:
        data[viewers] = str(viewers)
    if ratio != 0:
        data[ratio] = str(ratio)

    response = requests.post(url_clifl, data=data).json()

    if response['status'] != 'success':
        if response.get('error') != None:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
        else:
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error_response')
    else:
        return response['response'], 'NO'

def streams_get(token, id):
    data = {
        "action": "streams-get",
        "id": str(id),
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()

    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    else:
        return response['response'], 'NO'

def ytclients_get(token):
    global url_clifl
    data = {
        "action": "ytclients-get",
        "token": str(token)
    }

    response = requests.post(url_clifl, data=data).json()
    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    else:
        task_list = response['response']
        all_processed_tasks = []

        for client in task_list:
            processed_task = {
                'id': str(client['id']),
                'sec': int(client['info']['sec']),
                'http': client['info']['http'],
                'error': int(client['info']['error']),
                'ip': client['info']['ip'],
                'youtube_account': client['accounts']['youtube'],
                'coin': int(client['data']['coin']),
                'coin_task': int(client['data']['coin_task']),
                'count': int(client['data']['count']),
                'count_task': int(client['data']['count_task'])
            }
            all_processed_tasks.append(processed_task)

        return all_processed_tasks, 'NO'


def href_format(href, platform):
    from urllib.parse import urlsplit, urlunsplit
    if platform == "ytview" or platform == "ytlike" or platform == "ytcomm":
        href = f'https://www.youtube.com/watch?v={YouTube(str(href)).video_id}'

    if platform == "inst":
        from urllib.parse import urlparse, urlunparse
        parsed_url = urlparse(href.encode('utf-8'))
        netloc_parts = parsed_url.netloc.split(b'.')
        if len(netloc_parts) == 2 and netloc_parts[0] == b'instagram':
            netloc_parts.insert(0, b'www')
            new_netloc = b'.'.join(netloc_parts)
            new_parsed_url = parsed_url._replace(netloc=new_netloc)
            href = urlunparse(new_parsed_url).decode('utf-8')

    if platform == 'tiktok':
        try:
            response = requests.head(href, allow_redirects=True)
            href = response.url
            parsed_url = urlsplit(href)
            href = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', ''))
        except Exception as e:
            return 'Возникла ошибка во время обработки TikTok сылки', str(e)
    return href


def mytasks_task(token, platform, id):
    data = {
        "action": "mytasks-task",
        "token": str(token),
        "platform": str(platform),
        "id": str(id)
    }
    response = requests.post(url_clifl, data=data).json()
    if response['status'] != 'success':
        return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
    else:
        task = response['response']
        if response['response'] == 'error':
            return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', response.get('error')
        else:
            try:
                task = task[0]
                task = {
                    'id': str(task['id']),
                    "platform": str(task["platform"]),
                    "type": str(task["type"]),
                    "short_url": str(task["short_url"]),
                    "url": str(task["url"]),
                    "valh": str(task["valh"]),
                    "need": str(task["need"]),
                    "now": str(task["now"]),
                }
                return task, ''
            except:
                return 'Возникла ошибка. Пожалуйста, проверьте второе значение!', ''
