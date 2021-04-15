from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    # return HttpResponse("Hello World!!!")
    return render(request,'myapp/index.html',{'text':'<h1>this is text</h1>'})

def content(request,num,num2=1):
    return HttpResponse("result:[%s-%s]"%(num,num2))

from .models import Grades

def grades(request):
    grades_list=Grades.objects.all()
    return render(request,'myapp/grades.html',{"grades":grades_list})

from .models import student
from django.db.models import Max

def students(request):
    student_list=student.stuobj.all().values()
    return render(request,'myapp/student.html',{"student_list":student_list})

#显示前3条数据
def student3(request):
    student_list = student.stuobj.all()[0:3]
    return render(request,'myapp/student.html',{'student_list':student_list})

#分页显示学生(每页5条)
def stupage(request,page):
    page= int(page)
    print((page-1)*5,page*5)
    studentsList = student.stuobj.all()[(page-1)*5:page*5]
    return render(request, 'myapp/student.html', {'student_list': studentsList})


#点击班级列表，跳转对应班级学生表
def grade_student(request,num):
    grades = Grades.objects.get(pk=num)
    student_list = grades.student_set.all()
    return render(request,'myapp/student.html',{"student_list":student_list})

#定义一个自增数据的方法
def addstudent(request):
    grade=Grades.objects.get(pk=1)
    stu = student.createStudent("谢霆锋",20,True,'长得帅',grade,'2020-08-01','2020-08-01',)
    stu.save()
    return HttpResponse('数据已生成')

def addstudent2(request):
    grade=Grades.objects.get(pk=1)
    stu = student.stuobj2.createStudent("张杰",20,True,'这就是爱~~~~',grade,'2020-08-02','2020-08-02',)
    stu.save()
    return HttpResponse('数据已生成')

#查询数据库中sname包含“谢”的数据
def studentsearch(request):
    # student_list=student.stuobj.filter(sname__contains='谢')
    # student_list=student.stuobj.filter(pk__in=[1,2,3,4])
    # student_list=student.stuobj.filter(sage__gt=15)
    # student_list=student.stuobj.filter(createTime__year=2020)

    grade = Grades.objects.filter(student__scontend__contains='xx')     #查询scontent字段值中带有‘xx’的班级
    print(grade)
    # maxAge = student.stuobj.aggregate(Max('sage'))     #students表中查询最大的年龄
    # print(maxAge)
    student_list = student.stuobj.filter(~Q(pk__lte=3))  #查询id小于等于3 或 年龄大于15的数据
    return render(request,'myapp/student.html',{"student_list":student_list})

from django.db.models import F,Q
def girl_class(request):
    g = Grades.objects.filter(ggirlnum__gt=F('gboynum')+20)    #查询女生比男生多的班级
    print(g)
    return HttpResponse('girls class!!!')

#get、post请求中的属性
def attribles(request):
    print(request.path)
    print(request.method)
    print(request.encoding)
    print(request.GET)
    print(request.POST)
    print(request.FILES)
    print(request.COOKIES)
    print(request.session)
    return HttpResponse('attribles')

#获取get请求的参数
def get1(request):
    a = request.GET.get('a')
    b = request.GET['b']  #另一种写法
    c = request.GET.get('c')
    return HttpResponse(a + ' ' + b + ' ' + c)

#get请求，获取?a=1&a=2&c=3参数中，多个a的值以列表状态返回
def get2(request):
    a = request.GET.getlist('a')
    a1 = a[0]
    a2 = a[1]
    c = request.GET['c']
    return HttpResponse(a1 + ' ' + a2 +' ' + c)

#post请求案例,获取post请求参数
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


#response中的参数
def showresponse(request):
    res = HttpResponse()
    res.content = b'hello world!'
    print(res.content)
    print(res.charset)
    print(res.status_code)
    print(res.content-type)

#cookie
def cookietest(request):
    res = HttpResponse()
    cookie = request.COOKIES
    res.write("<h1>" + cookie['django'] + "</h1>")
    # cookie = res.set_cookie("django","hello autumn!!!")
    return res

#重定向(HttpResponseRedirect与redirect效果一致)
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
def redirect1(request):
    return redirect('/redirect2')
def redirect2(request):
    return HttpResponse('this is redirect2 page!!!')

#session
# def main(request):
#     username = request.session.get('name')     #取session中name对应的值，当name无值时，取后面的‘游客’做值
#     return render(request,'myapp/main.html',{'username':username})
def login(request):
    return render(request,'myapp/login.html')
def showmain(request):
    username = request.POST.get('username', '游客')
    print(username)
    # # 存储session
    request.session['name'] = username
    return HttpResponse(username)

#if语句
def if_example(request):
    return render(request,'myapp/if_example_html.html',{"num":10})

#for语句
def for_example(request):
    student_list = student.stuobj.all()
    return render(request,'myapp/for_example_demo.html',{'student_list':student_list,'str_name':'使用过滤器修改为大写：daxie','list_name':['good','nice','handsome'],'num':10})

def good(request):
    return render(request, 'myapp/good.html', {"good": "good"})

def base_main(request):
    return render(request, 'myapp/base_main.html')

def base_detail(request):
    return render(request,'myapp/base_detail.html')

def postfile(request):
    return render(request,'myapp/postfile.html')

def showinfo(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    return render(request,'myapp/showinfo.html',{'username' : username,'password' : password})

#绘制二维码
def verifycode(request):
    #引入绘图模块
    from PIL import Image,ImageDraw,ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB',(width,height),bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
    #定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机选取4个值作为验证码
    random_str = ''
    for i in range(0,4):
        random_str += str[random.randrange(0,len(str))]
    #构造字体对象
    font = ImageFont.truetype(r'C:\Windows\Fonts\Constantia\constanb.ttf',40)
    #构造字体颜色
    fontcolor1 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor2 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor3 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor4 = (255,random.randrange(0,255),random.randrange(0,255))
    #绘制4个字
    draw.text((5,2),random_str[0],font=font,fill=fontcolor1)
    draw.text((25,2),random_str[1],font=font,fill=fontcolor2)
    draw.text((50,2),random_str[2],font=font,fill=fontcolor3)
    draw.text((75,2),random_str[3],font=font,fill=fontcolor4)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verify'] = random_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf,'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(),'image/png')

def verifycodefile(request):
    f = request.session.get("flag",True)
    tips = ''
    if f == False:
        tips = '请重新输入'
    request.session.clear()
    return render(request,'myapp/verifycodefile.html',{'flag':tips})

from django.shortcuts import render,redirect
def verifycodecheck(request):
    code1 = request.POST.get("verifycode").upper()  #获取请求参数中的verifycode值
    code2 = request.session["verify"].upper()       #获取后台存储在session中的验证码
    if code1 == code2:                              #验证码是否一致
        return render(request,'myapp/success.html')
    else:
        request.session["flag"] = False
        return redirect('/verifycodefile/')

#上传文件
def upfile(request):
    return render(request,'myapp/upfile.html')

import os
from django.conf import settings
def savefile(request):
    if request.method == 'POST':
        f = request.FILES['file']
        #文件上传的路径
        filepath=os.path.join(settings.MEDIA_ROOT,f.name)

        with open(filepath,'wb') as fp:
            for info in f.chunks():             #chunks()：将一个大文件分为数个小文件流
                fp.write(info)
        return HttpResponse("上传成功")

    else:
        return HttpResponse("上传失败")

#分页
from .models import student
from django.core.paginator import Paginator
def studentpage(request, pageid):
    #所有学生列表
    allList = student.stuobj.all()

    paginator = Paginator(allList,6)
    page = paginator.page(pageid)

    return render(request,'myapp/studentpage.html',{"students":page})

#ajax
def ajaxstudent(request):
    return render(request,'myapp/ajaxstudent.html')

from django.http import JsonResponse
def studentinfo(request):
    stus = student.stuobj.all()
    list = []
    for stu in stus:
        list.append([stu.sname, stu.sage])

    return JsonResponse({"data":list})

#富文本
def edit(request):
    return render(request,'myapp/edit.html')

#celery 异步运行
import time
from myapp.task import test
def celery(request):
    a = test()
    return render(request,'myapp/celery.html')