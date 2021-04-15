from django.db import models

# Create your models here.
class Grades(models.Model):
    gname= models.CharField(max_length=20)
    gdate=models.DateTimeField()
    ggirlnum=models.IntegerField()
    gboynum=models.IntegerField()
    isDelete=models.BooleanField(default=False)

    #关联的外键可以选这里返回的值
    def __str__(self):
        return self.gname
    #元选项，定义表名为grades
    class Meta:
        db_table='grades'

#自定义的管理器方法
class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager,self).get_queryset().filter(isDelete=False)     #从返回的查询集中筛选出isDelete=False的数据，get_queryset():返回查询集

    #为调用的类定义一个增加数据的方法（目前在student类中调用，为student添加一条数据）
    def createStudent(self,name,age,gender,contend,grade,lastT,creatT,isD=False):
        stu = self.model()
        # print(type(stu))  #查看调用的类
        stu.sname = name
        stu.sage = age
        stu.sgender = gender
        stu.scontend = contend
        stu.sgrade = grade
        stu.lastTime = lastT
        stu.createTime = creatT
        return stu


class student(models.Model):
    stuobj=models.Manager()         #自定义的模型管理器名 stuobj
    stuobj2=StudentManager()        #自定义的模型管理器   stuobj2
    sname=models.CharField(max_length=20)
    sgender=models.BooleanField(default=True)
    sage=models.IntegerField()
    scontend=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)
    #关联外键
    sgrade=models.ForeignKey("Grades",on_delete=models.CASCADE)

    def __str__(self):
        return self.sname

    lastTime = models.DateTimeField(auto_now=True)
    createTime = models.DateTimeField(auto_now_add=True)
    #元选项，定义表名为students
    class Meta:
        db_table="students"
        ordering=['id']

    #为student类定义一个类方法创建对象
    @classmethod    #声明下面为一个类方法
    def createStudent(cls,name,age,gender,contend,grade,lastT,creatT,isD=False):     #    cls:代表继承自student，与createStudent(student)的效果一致
        stu = cls(sname=name,sage=age,sgender=gender,scontend=contend,sgrade=grade,lastTime=lastT,createTime=creatT)
        #两种写法，一种直接在类上赋值，一种初始化类，再进行赋值
        # stu =cls()
        # stu.sname=name
        # stu.sage=age
        # stu.sgender=gender
        # stu.scontend=contend
        # stu.sgrade=grade
        # stu.lastTime=lastT
        # stu.createTime=creatT
        return stu

from tinymce.models import HTMLField
class Text(models.Model):
    str = HTMLField()
