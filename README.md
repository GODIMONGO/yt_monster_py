# yt_monster_py
Библиотека для ytmonster.ru
Помните что по умолчанию если нет ошибок то возвращяется значение NO большими буквами на английском языке без пробелов.
На данный момент есть такие команды
version() #Нечего не принимает в ответ возвращяет версию библиотеки в строчном типе.
balance_coin(token) #Возвращяет баланс в COIN принимает в себя токен любого типа.
balance_many(token) #Возвращяет баланс денег принимает в себя токен любого типа.
Добавление аккаунта:
add_account(token, platform, url) #Возварщяет есть ли ошибки и словарь https://ytmonster.ru/api/v2/#accounts-add что бы получить значение нужно ввести ключ обозначающий значение то есть
"account" = айди аккаунта
"url" = сылка на выполнение 
принимает в себя токен, соц сеть в значения которые расписаны на https://ytmonster.ru/api/v2/#accounts-add и айди аккаунта так же раписан там.
check_account(token, account, task) #Возварщяет статус проверки аккаунта "success" и ошибку.
