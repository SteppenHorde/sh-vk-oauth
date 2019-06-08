import requests
from django.urls import reverse_lazy
from .secrets import * #gitignore



API_VERSION = '5.95'
METHOD_URL = 'https://api.vk.com/method/'
AUTH_URL = 'https://oauth.vk.com/authorize'
ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'


def get_vk_oauth_link(
            url=AUTH_URL,
            client_id=SECRET_CLIENT_ID,
            display='page',
            scope='friends,offline',
            response_type='code',
            redirect_uri=reverse_lazy('main'), # reverse('main') циклит вьюху
            v=API_VERSION,
    ):
    vk_oauth_link = url + '?' + '&'.join([
                                        f'client_id={client_id}',
                                        f'display={display}',
                                        f'scope={scope}',
                                        f'response_type={response_type}',
                                        f'redirect_uri={redirect_uri}',
                                        f'v={v}',
                                        ])
    return vk_oauth_link


def get_vk_access_token(
            code,
            redirect_uri=reverse_lazy('main'), # reverse('main') циклит вьюху
            url=ACCESS_TOKEN_URL,
            client_id=SECRET_CLIENT_ID,
            client_secret=SECRET_CLIENT_SECRET,
    ):
    vk_access_token_link = url + '?' + '&'.join([
                                        f'client_id={client_id}',
                                        f'client_secret={client_secret}',
                                        f'redirect_uri={redirect_uri}',
                                        f'code={code}',
                                        ])
    response = requests.get(vk_access_token_link)
    json_response = response.json()
    access_token = json_response.get('access_token')
    return access_token


def is_vk_token_valid(
        access_token,
        url=METHOD_URL,
        client_secret=SECRET_CLIENT_SECRET,
        v=API_VERSION,
    ):
    method_name='users.get'
    check_vk_token_valid_link = url + method_name + '?' + '&'.join([
                                                            f'access_token={access_token}',
                                                            f'v={v}',
                                                            ])
    response = requests.get(check_vk_token_valid_link)
    json_response = response.json()
    if json_response.get('error', False):
        return False
    else:
        return True


def get_friends_info(
        access_token,
        count=5,
        url=METHOD_URL,
        order='random',
        v=API_VERSION,
    ):
    method_name = 'friends.get'
    fields = 'first_name,last_name,photo_50'
    get_friends_info_link = url + method_name + '?' + '&'.join([
                                                    f'access_token={access_token}',
                                                    f'count={count}',
                                                    f'order={order}',
                                                    f'fields={fields}',
                                                    f'v={v}',
                                                    ])
    response = requests.get(get_friends_info_link)
    json_response = response.json()
    return json_response.get('response').get('items')


def get_user_info(
        access_token,
        url=METHOD_URL,
        v=API_VERSION,
    ):
    method_name = 'users.get'
    fields = 'first_name,last_name,photo_200'
    get_user_info_link = url + method_name + '?' + '&'.join([
                                                    f'access_token={access_token}',
                                                    f'fields={fields}',
                                                    f'v={v}',
                                                    ])
    response = requests.get(get_user_info_link)
    json_response = response.json()
    return json_response.get('response')[0]
