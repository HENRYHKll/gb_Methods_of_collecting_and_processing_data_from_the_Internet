import scrapy
import json
from scrapy.http import HtmlResponse
import re
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'on.space'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1636014781:AYJQALTugLAz57xPBwN6dkVRgH/Hwa9gFmR1a6FPR3DT+59hx74aI4Mm6jvs3XhSpZAc9X5a0FoH1aNeVqu/POgn51OKekJsSMlWwo+XfTir1zTIGhYzw+G/Lboscb+BkVTlPwB+cA69ymbewA=='
    user_parser_acc_list = ['newbor_official', 'kvartaldepo']
    insta_api_url = 'https://i.instagram.com/api/v1/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_url,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user_parser_acc in self.user_parser_acc_list:
                yield response.follow(f'/{user_parser_acc}',
                                      callback=self.parse_user,
                                      cb_kwargs={'username': user_parser_acc})


    def parse_user(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {"count": 12}
        user_status = 'followers'
        for user_status in ('following', 'followers'):
            get_follow_user_url = f'{self.insta_api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'
            yield response.follow(get_follow_user_url,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  callback=self.parse_user_follow,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def parse_user_follow(self, response: HtmlResponse, username, user_id, variables, user_status):
        json_data = response.json()
        if json_data.get('next_max_id'):
            variables['max_id'] = json_data.get('next_max_id')
            get_following_users_url = f'{self.insta_api_url}friendships/{user_id}/{user_status}/?{urlencode(variables)}'

            yield response.follow(get_following_users_url,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables),
                                             'user_status': user_status},
                                  callback=self.parse_user_follow,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        for user in json_data.get('users'):
            item = InstaparserItem(
                username=user.get('username'),
                user_status=user_status,
                user_id=user.get('pk'),
                photo=user.get('profile_pic_url'),
                from_username=username
            )

            yield item


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
