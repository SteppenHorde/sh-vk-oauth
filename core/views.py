from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse

from .oauth import *



class Main(View):
    template_name = 'core/main.html'
    template_js = 'core/js/vk_oauth.js'
    context = {}
    def get(self, request):
        # Хранение состояния авторизации с помощью сессий:
            # авторизация отсутствует или токен невалидный
        if not request.session.get('auth_info', False) or not is_vk_token_valid(request.session['auth_info'].get('access_token')):
            self.context['not_authed'] = True
            self.context['allow_user_n_friends_css'] = False
            code = request.GET.get('code', False)
            if code:
                request.session['auth_info'] = dict()
                request.session.set_expiry(2592000) # месяц храним сессию
                access_token = get_vk_access_token(code=code, redirect_uri=request.build_absolute_uri('/'))
                if is_vk_token_valid(access_token):
                    request.session['auth_info']['access_token'] = access_token
                else:
                    return HttpResponse('Не удалось авторизовать ваш аккаунт, вернитесь и попробуйте снова')

                self.context['allow_vk_oauth_script'] = True
                self.context['allow_user_n_friends_css'] = True
                return render(request, self.template_name, context=self.context)
            else: # не авторизован и не получен токен
                self.context['allow_vk_oauth_script'] = False
                self.context['oauth_url'] = get_vk_oauth_link(redirect_uri=request.build_absolute_uri('/'))
                return render(request, self.template_name, context=self.context)
        else: # уже авторизован
            self.context['allow_vk_oauth_script'] = False
            self.context['allow_user_n_friends_css'] = True
            self.context['not_authed'] = False
            friends = get_friends_info(request.session['auth_info']['access_token'])
            user = get_user_info(request.session['auth_info']['access_token'])
            self.context['friends'] = friends
            self.context['user'] = user
            return render(request, self.template_name, context=self.context)



class GetUsers(TemplateView): # только для JS запросов
    template_name = 'core/user_n_friends_list.html'
    context = {}
    def get(self, request):
        friends = get_friends_info(request.session['auth_info']['access_token'])
        user = get_user_info(request.session['auth_info']['access_token'])
        self.context['friends'] = friends
        self.context['user'] = user
        return render(request, self.template_name, context=self.context)
