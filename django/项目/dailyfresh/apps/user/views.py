from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.views.generic import View
from django.conf import settings
from user.models import User
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re
from django.http import HttpResponse


# Create your views here.

# /user/register
def register(request):
    '''注册'''
    if request.method == 'GET':
        #显示注册页面
        return render(request, 'register.html')
    else:
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        if not all([username, password, email]):
            # 判断传递的数据不完整（false），all：可对列表内参数进行迭代
            return render(request, 'register.html', {'errmsg': '数据不完整！'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确！'})

        # 校验协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议！'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            '''用户名不存在'''
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在！'})

        # 业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        # 修改字段值保存
        user.is_active = 0
        user.save()

        # 视图重定向
        return redirect(reverse('goods:index'))

def register_handle(request):
    '''进行注册处理'''
    #接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    #数据校验
    if not all([username,password,email]):
        #判断传递的数据不完整（false），all：可对列表内参数进行迭代
        return render(request, 'register.html', {'errmsg':'数据不完整！'})

    #校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg':'邮箱格式不正确！'})

    #校验协议
    if allow != 'on':
        return render(request, 'register.html', {'errmsg':'请同意协议！'})

    # 校验用户名是否重复
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        '''用户名不存在'''
        user = None

    if user:
        #用户名已存在
        return render(request, 'register.html', {'errmsg':'用户名已存在！'})

    #业务处理：进行用户注册
    user = User.objects.create_user(username, email,password)
    #修改字段值保存
    user.is_active = 0
    user.save()

    #视图重定向
    return redirect(reverse('goods:index'))

class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request, 'register.html')
    def post(self,request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        if not all([username, password, email]):
            # 判断传递的数据不完整（false），all：可对列表内参数进行迭代
            return render(request, 'register.html', {'errmsg': '数据不完整！'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确！'})

        # 校验协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议！'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            '''用户名不存在'''
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在！'})

        # 业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        # 修改字段值保存
        user.is_active = 0
        user.save()

        #发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/3
        #激活链接中包含用户的身份信息，并且要把身份信息进行加密

        #加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)  #bytes
        token = token.decode()

        #发邮件
        # subject = '天天生鲜欢迎信息'
        # message = ''
        # sender = settings.EMAIL_FORM    #收件人看到的发件人
        # receiver = [email]              #收件人
        # html_message = '<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户:<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
        #
        # send_mail(subject, message,sender, receiver,html_message=html_message)

        # 调用celery定义的函数，添加任务；
        # 执行任务：需先启动redis，并在cmd窗口该项目路径下执行celery_tasks.tasks文件： celery -A celery_tasks.tasks worker -l info
        send_register_active_email.delay(email, username, token)

        # 视图重定向
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            #获取待激活用户的id
            user_id = info['confirm']

            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            #跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期')

class LoginView(View):
    '''登录'''
    def get(self,request):
        '''显示登录页面'''
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self,request):
        '''登录校验'''

        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        #校验数据
        if not all([username,password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        #业务处理：登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            #用户名、密码正确
            if user.is_active:
                #用户已激活
                #记录用户登录状态
                login(request,user)

                # 跳转首页
                resonse = redirect(reverse('goods:index'))

                #判断是否需要记住
                remember = request.POST.get('remember')

                if remember == 'on':
                    #记住用户名
                    resonse.set_cookie('username', username, max_age=7*24*3600)
                else:
                    resonse.delete_cookie('username')

                #返回resonse
                return resonse
            else:
                #用户未激活
                return render(request, 'login.html', {'errmsg':'账户未激活！'})
        else:
            #用户名或密码错误
            return render(request, 'login.html', {'errmsg':'用户名或密码错误！'})
