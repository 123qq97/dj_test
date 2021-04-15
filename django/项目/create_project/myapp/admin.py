from django.contrib import admin

# Register your models here.
from .models import Grades,student

#表新增数据时，同时为另一张表创建数据
class StudentsInfo(admin.TabularInline):  #admin.StackedInline:另一种显示方式
    model = student     #控制哪张表要创建数据
    extra = 2           #控制一次必须创建几条数据

#自定义成绩列表数据的显示（创建/修改）
class GradesAdmin(admin.ModelAdmin):

    #列表页属性
    list_display = ['id','gname','gdate','ggirlnum','gboynum','isDelete']
    list_filter = ['id']
    search_fields = ['gname']
    list_per_page = 5

    #添加、修改列表页的属性
    inlines = [StudentsInfo]                                    #新增（/修改）时，同时显示另一个表的可填写的字段
    # fields = ['gdate','gname','ggirlnum,gboynum,isDelete']   #控制新增（修改）时的字段显示
    fieldsets = [                                               #控制新增（修改）时的字段分组显示
        ("num",{"fields":['ggirlnum','gboynum']}),
        ("base",{"fields":['gname','gdate','isDelete']})
    ]

#自定义学生列表数据的显示（创建/修改）
@admin.register(student)            #装饰器，作用就是替代下面的类调用
class studentAdmin(admin.ModelAdmin):
    def isgender(self):
        if self.sgender:
            return '男'
        else:
            return '女'

    #定义列名的函数
    def id_head(self):
        return self.id

    #列表页
    isgender.short_description = "性别"    #修改列表页列名
    id_head.short_description = '单号'     #修改列表页列名

    list_display = [id_head,'sname',isgender,'sage','sgrade','scontend','isDelete']
    list_filter = ['id']
    search_fields = ['sname']
    list_per_page = 5

    actions_on_top = False                  #控制顶部不显示动作栏
    actions_on_bottom = True                #控制底部显示动作栏

    #新增（修改）列表页的属性
    fields = ['sgender','sage','sgrade','sname','scontend','isDelete']


admin.site.register(Grades, GradesAdmin)
# admin.site.register(student,studentAdmin)

#富文本
from .models import Text
admin.site.register(Text)