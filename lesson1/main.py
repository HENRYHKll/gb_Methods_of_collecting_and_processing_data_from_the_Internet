import requests

import json


# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.

def get_githab_rep_user(user):
    lnk = f'https://api.github.com/users/{user}/repos'
    headers = {'User-Agent': user,
               'Accept': 'application/vnd.github.v3+json'}
    params = {'sort': 'full_name'}
    response = requests.get(lnk, headers=headers, params=params)
    j_data = response.json()
    with open('1.json', 'w') as f:
        json.dump(j_data, f)
    with open('1.json') as f:
        data = json.load(f)
        for rep in data:
            print(rep['name'])


username = input('enter user name GitHub: ')

get_githab_rep_user(username)

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.


def vk_get_app():
    app_id = 7929798
    vk_version = '5.132'
    lnk = f'https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html' \
          f'&scope=friends&response_type=token&v={vk_version}';
    print(f'Go to link:\n{lnk}\n  and copy token.')
    token = input('\nEnter tocen: ')

    response = requests.get(f'https://api.vk.com/method/groups.get?extended=1&access_token={token}&v={vk_version}')
    response_json = response.json()
    with open('2.json', 'w') as file:
        json.dump(response_json, file)

    print('\nList Groups')
    for group in response_json['response']['items']:
        print(f"{group['name']}")


vk_get_app()

