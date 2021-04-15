'''
其他：导包无法获取路径，使用自定路径
import sys
sys.path.append("路径地址")

命令：
1、创建项目：django-admin startproject 项目名称
    创建项目自带的文件功能：
        1、manage.py文件：一个命令行工具，可以使我们用多种方式对django项目进行交互
        2、settings.py文件:项目的配置文件
            数据库配置：
                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': 数据库名,
                        'USER' : 用户名,
                        'PASSWORD' ：数据库密码,
                        'HOST'：数据库服务器ip,
                        'PORT'：端口
                    }
                }
    
        3、urls.py文件：项目的url声明
        4、wsgi.py文件：项目与WSGI兼容的web端服务器入口
    启动项目：
        1、进入到有manage.py文件的这一层目录，输入python manage.py runserver 0.0.0.0:8000启动项目 
2、配置musql：
    2.1、在init文件中写入 import pymysql;  pymysql.install_as_MySQLdb() 
    2.2、pymysql.version_info = (1, 3, 13, "final", 0)；这句非必须写，只是高django版本必写，否则会报错
    2.3、再修改和添加setting文件的databases中对应的元素

3、创建应用：再对应项目文件夹下，运行python manage.py startapp '项目名'
    创建应用自带的文件功能：
        1、admin.py文件：站点配置
        2、models.py文件：模型
        3、views.py文件：试图
    
3、激活应用：再setting文件中，将创建的应用，加入到INSTALLED_APPS列表中

4、定义models模型：一个数据表，对应有一个模型

5、生成数据表：
    5.1、生成迁移文件：命令行执行：python manage.py makemigrations
    5.2、执行迁移操作：命令行执行：python manage.py migrate

6、表操作
    查询表内容，类似select * from： 
        表类名.objects.all().values()                                         例：Test.objects.all()
        
        
    按条件查询内容，类似select * from   where:
        表类名.objects.filter(输入的条件).values()                             例：Test.objects.filter(id=1) 
        
        
    给表字段赋值,类似insert into：
        变量=表类名(表字段1='输入的值'，表字段2='输入的值')                     例：test1 = Test(name='runoob')   test1.save()
        变量.save()
        
        
    修改表字段值，类似update：
        表类名.objects.filter(输入的条件).update('需要修改的条件')             例：Test.objects.filter(id=1).update(name='Google')
        
    数据排序，类似order by：
        表类名.objects.order_by(列名)                                         例：Test.objects.order_by("id")
    
    删除数据，类似delete xx from xx  where：
        表类名.objects.filter(id=1).delete()                                  例：Test.objects.filter(id=1).delete()
    
    上面的方法可以连锁使用：
        表类名.objects.filter().order_by()                                    例：Test.objects.filter(name="runoob").order_by("id")

    关联对象：
        获取关联对象的集合，类似表连接：
            对象名（表类名1的变量）.表类名2(小写)_set.all()                     例：grade=grader（）    grade.students_set.all()
        直接赋值，无需save：
            对象名（表类名1的变量）.表类名2(小写)_set.create(字段1='',字段2='')  例：grade.students_set.create(sanme='张三',sage=14)
        关联表，可以选取被关联表返回的值：
            def __str__(self):
                return self.字段名
        
7、管理admin站点 admin.py:
    1、创建admin管理员账户: python manage.py createsuperuser  
    2、自定义管理页面：
        修改admin显示中文与中国时间:  将setting文件中后面两字段值改变  LANGUAGE_CODE = 'zh-hans'   TIME_ZONE = 'Asia/Shanghai'
        将数据表显示在admin页面中: admin.site.register(表名)
        自定义列表页：
        ①需要先自定义一个类（例：class 类名1(admin.ModelAdmin)），然后在admin.site.register(表名,自定义的类)调用这个类
            列表页属性：
                list_display = ['字段名1','字段名2']: 列表显示字段名1、字段名2
                list_filter = ['字段名1']:列表添加一个过滤器，可以找出字段名1的那一条数据
                search_fields = ['字段名1']:列表添加一个搜索栏，可以搜索字段名1的数据
                list_per_page = 5:列表页添加分页器，每5条数据一页
                
                #修改列表页列名：
                    ①先定义一个方法:
                        def id_head(self):
                            return self.字段名1
                    ②id_head.short_description = '自定义列名'：列表页显示自定义的列名
        
            添加(/修改)列表页属性：
                注：fields、fieldssets不能同时使用，只能使用其一
                fields = ['字段名1','字段名2']: 添加(/修改)列表页显示字段名1、字段名2
                fieldsets = [("组1",{"fields":['字段名1']}),("组2",{"fields":['字段名2']})]:将添加（/修改）列表页的字段，进行分组显示，将字段名1放在组1栏，字段名2放在组2栏显示
                
                #多表同时创建(/修改)数据
                    ①先自定义一个类（例：class 类名2(admin.TabularInline)）
                    ②inlines = ['类名2']: 控制新增(/修改)时，显示另一个表的可填写的字段

8、视图 views.py、urls.py
    path :匹配绝对路径
    re_path:匹配相对路径,使用正则匹配
    include('myapp.urls'):匹配对应文件的url，用于匹配不同文件目录下的url
    自定义方法，通过点击班级跳转对应学生表，例：def grade_student(request,num)  位置：createproject—myapp —grade_student
    
9、模板 templates
    模板是html页面，可以根据视图传递过来进行填充
    配置路径:   'DIRS': [os.path.join(BASE_DIR,'templates')] ,
    

'''
