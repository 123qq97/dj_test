'''
--------------------------------------------------视图------------------------------------------------------------------
概述：
    作用：
        视图接受web请求，并响应web请求
    
    本质：
        视图就是一个python中的函数
    
    响应：
        网页：
            重定向
            错误视图：
                404
                500
                400
        json数据：
    
    过程：
        ①用户在浏览器中输入网址
        ②django获取网址信息，去除ip与端口
        ③url管理器，逐个匹配urlconf，记录视图函数名
        ④视图管理器找到相应的视图去执行，返回结果给浏览器
        
    url配置：
        配置流程：
            指定根级url配置文件：
                settings.py文件中的ROOT_URLCONF
                代码：ROOT_URLCONF='project.urls'
                默认实现了
        
            urlpatterns:
                一个url实例的列表
                url对象：
                    正则表达式
                    视图名称
                    名称
        
            url匹配正则的注意事项：
                如果想要从url中获取一个值，需要对正则加小括号
                匹配正则前方不需要加反斜杠
                正则前需要加r表示字符串不转义
        
        引入其他url配置：
            在应用中创建urls.py文件，定义本应用的url配置，在工程urls.py文件中使用include()方法
            代码：
                from django.contrib import admin
                from django.urls import path,include
                
                urlpatterns = [
                    path('admin/', admin.site.urls),
                    path('',include('myapp.urls')),
                ]
                ---------------不同文件中代码-----------
                from django.urls import path,re_path
                from . import views
                
                
                urlpatterns = [
                    path('',views.index),
                    re_path(r'^(\d+)/(\d+)$',views.content),
                    path('grades/',views.grades),
                    path('student/',views.students),
                    re_path(r'^grades/(\d+)$',views.grade_student),
                    path('addstudent/',views.addstudent),
                    path('addstudent2/',views.addstudent2),
                    path('student3/',views.student3),
                    re_path(r'^stu/(\d+)/$',views.stupage),
                    path('studentsearch/', views.studentsearch),
                    path('girl_class/', views.girl_class),
                ]
            匹配过程：
        
        url的反向解析：
            概述：如果在视图、模板中使用了硬编码链接，在url配置发生改变时，动态生成对应的链接的地址
            解决：在使用链接时，通过url配置的名称，动态生成对应的url地址
            作用：使用url模板
        
        视图函数：
            定义视图:
                本质：一个函数
                视图参数：
                    一个HttpRequest的实例
                    通过正则表达式获取的参数
                位置：一般在view.py文件下定义
            错误视图：
                404视图：
                    找不到网页（url匹配不成功）时返回
                    在templates目录下定义404.html：
                        request_path：导致错误的网址
                        代码：
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>Title</title>
                            </head>
                            <body>
                                <h1>页面丢失</h1>
                                <h2>{{request_path}}</h2>
                            
                            </body>
                            </html>
                    配置settings.py：
                        DEBUG:如果为True永远不会调用404.html页面
                        ALLOWED_HOSTS=['*']
                500视图：
                    在视图代码中出现错误（服务器代码）
                400视图：
                    错误出现在客户出现的操作
            
            HttpRequest对象：
                概述：
                    服务器接收http请求后，会根据保温创建HttpRequest对象
                    对象的第一参数就是HttpRequest对象
                    django创建的，之后调用视图时传递给视图
                属性：
                    path：请求的完整路径（不包括域名和端口）
                    method：表示请求的方式，常用的有GET、POST
                    encoding：表示浏览器提交的数据的编码方式
                    GET：类似字典的对象，包含了get请求的所有参数
                    POST：类似字典的对象，包含了post请求的所有参数
                    FILES：类似字典的对象，包含了所有上传的文件
                    cookies：字典，包含所有的cookie
                    session：类似字典的对象，表示当前会话
                方法：
                    is_ajax():如果是通过XMLHttpRequest发起的，返回true
                    QueryDict对象：request对象中的Get、POST都属于QueryDict对象
                    方法：
                        get():
                            作用：根据键获取值
                            只能获取一个值
                            www.sunck.wang/abc?a=1&b=2&c=3
                        getlist():
                            将键的值以列表的形式返回
                            可以获取多个值
                            www.sunck.wang/abc?a=1&a=2&c=3
                            
                QueryDict对象：
                    request对象中的GET、POST都属于QueryDict对象
                    方法：
                        get():
                            作用：根据键获取值
                            只能获取一个值
                            实例：?a=1&b=2&c=3
                        getlist():
                            将键的值以列表的形式返回
                            可以获取多个值
                            实例：?a=1&a=2&c=3
                
                GET属性：
                    获取浏览器传递过来给服务器的数据
                    实例1：
                        参数：?a=1&b=2&c=3
                        代码：
                            a = request.GET.get('a')
                            b = request.GET['b']  #另一种写法
                            c = request.GET.get('c')
                    实例2：
                        参数：?a=1&a=2&c=3
                        代码：
                            a = request.GET.getlist('a')    #获取?a=1&a=2&c=3参数中，多个a的值以列表状态返回
                            a1 = a[0]
                            a2 = a[1]
                            c = request.GET['c']
                POST属性：
                    使用表单提交POST请求
                    关闭csrf：
                        'django.middleware.csrf.CsrfViewMiddleware',
                    代码：
                        def showregist(request):
                            return render(request,'myapp/regist.html')
                        def regist(request):
                            name = request.POST.get('name')
                            gender = request.POST.get('gender')
                            age = request.POST.get('age')
                            hobby = request.POST.getlist('hobby')
                            print(name)
                            print(gender)
                            print(age)
                            print(hobby)
                            return HttpResponse('post')
                        
             HttpResponse对象:
                概述：
                    作用：给浏览器返回数据
                    HttpResonse对象是由django创建的，HttpResponse对象由程序员创建
                用法：
                    不调用模板，直接返回数据
                        代码：
                            def index(request):
                                return HttpResponse("Hello World!!!")
                    调用模板
                        使用render方法：
                            原型：render(request,templateName[context])
                            作用：结合数据和模板，返回完整的HTML页面
                            参数：request：请求体对象
                                 templateName：模板路径
                                 context:传递给需要渲染在模板上的数据
                            示例:
                                def index(request):
                                    return render(request,'myapp/index.html')
                属性：
                    content：表示返回的内容的内容
                    charset：编码格式
                    status_code：响应状态码（200、302、400、....）
                    content-type:指定输出的MIME类型
                方法：
                    init：使用页面内容实例化HttpResponse对象
                    write(content)：以文件的形式写入
                    flush()：以文件的形式输出缓存区
                    set_cookie(key,value='',max_age=None,exprise=None)
                    delete_cookie(key):
                        删除cookie
                        注意：如果删除一个不存在的key，就当什么都没发生
                
                子类HttpResponseRedirect:
                    功能：重定向，服务器跳转
                    简写：redirect(to)
                    to推荐使用反向解析
                    代码：
                        from django.http import HttpResponseRedirect
                        from django.shortcuts import redirect
                        def redirect1(request):
                            return redirect('/redirect2')
                        def redirect2(request):
                            return HttpResponse('this is redirect2 page!!!')
                
                子类JsonResponse：
                    返回json数据，一般用于异步请求
                    __init__(self,data)
                    data:字典对象
                    注意：content-type类型为application/json
            
            状态保持：    
                概述：
                    http协议是无状态的，每次请求都是一次新的请求，不记得以前的请求
                    客户端与服务器端的一次通信就是一次会话
                    实现状态保持，在客户端或者服务器端存储有关会话的数据
                    存储方式：
                        cookie：所有的数据存储在客户端，不要存敏感的数据
                        session：所有的数据存储在服务端，在客户端用cookie存储session_id
                    状态保持的目的：在一段时间内跟踪请求者的状态，可以实现跨页面访问当前的请求者的数据
                    注意：不同请求者之间不会共享这个数据，与请求者一一对应
                启用session：
                    setting文件中：
                        INSTALLED_APPS：'django.contrib.sessions'
                        MIDDLEWARE:django.contrib.sessions.middleware.SessionMiddleware
                使用session：
                    启用session后，每个HttpRequest对象都有一个session属性，就是一个类似字典的对象
                    get(key,default=None):根据键获取session
                    clear()：情况所有的会话
                    flush():删除当前的会话并删除会话的cookie
                
            
        





'''