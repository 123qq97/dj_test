'''
表模型字段:
    CharField(max_length=字符长度):字符串类型，默认的表单样式是 TextInput
    
    TextField:大文本类型，一般超过4000字符使用，默认的表单控件是Textarea
    
    IntegerField:整数类型
    
    DecimalField(max_digits=None,decimal_places=None):小数类型
        ·使用python的Decimal实例表示的十进制浮点数
        ·DecimalField.max_digits    位数总数
        ·DecimalField.decimal_places    小数点后的数字位数
        
    FloatField:浮点型,用python的float实例来表示的浮点数
    
    BooleanField:布尔类型，值为true/false，此字段的默认表单控制是CheckboxInput
    
    NullBooleanField:布尔类型，支持null、true、false三种值
    
    DateField():日期类型，使用python的datetime.date实例表示的日期，参数同DateField
        DateField(auto_now=True):有字段修改时，自动更新为最后的修改时间；
        DateField(auto_now_add=True):当对象第一次被创建时自动设置为当前时间；
        auto_now_add与auto_now无法同时使用
    
    TimeField():时间类型，使用python的datetime.time实例表示的时间，参数同DateField
    
    DateTimeField():日期和时间类型，参数同DateField
    
    FileField():上传文件的类型
    
    ImageField():继承了FileField的所有属性和方法，但会对上传的文件进行校验，确保他是个有效的image


元选项：
    在模型类中定义Meta类，用于设置元信息
    db_table：定义数据表名，推荐使用小写字母，数据表名默认为:项目名小写_类名小写
    ordering:对象的默认排序字段，获取对象的列表时使用；
            升序：ordering['id'],降序：ordering['-id']
            注意：排序会增加数据库的开销
            
模型成员：
    类属性：
        object：
            ①是Manager类型的一个对象，作用是与数据库进行交互；
            ②当定义模型类没有指定管理器，则Django为模型创建了一个名为objects的管理器
        
        自定义管理器名：
            名称1 = models.Manager()
            当为模型指定模型管理器，Django就不再为模型类生成objects模型管理器 
        
        自定义管理器Manager类
            模型管理器是Django的模型进行与数据库进行交互的接口，一个模型可以有多个模型管理器
            作用：
                向管理器中添加额外的方法
                修改管理器返回的原始查询集（重写get_queryset()方法）
            例子：
                #自定义的管理器方法
                class StudentManager(models.Manager):
                    def get_queryset(self):
                        return super(StudentManager,self).get_queryset().filter(isDelete=False)     #从返回的列表中筛选出isDelete=False的数据
                
                class student(models.Model):
                    stuobj=models.Manager()         #自定义的模型管理器名 stuobj
                    stuobj2=StudentManager()        #自定义的模型管理器   stuobj2
        
        创建对象：
            目的：向数据库中添加数据
            当创建对象时，django不会对数据库进行读写操作，当调用save()方式时才与数据库交互，将对象保存到数据库表中
            注意:__init__方法已经在父类models.Model中使用，在自定义的模型中无法使用
            方法：在模型类中添加一个类方法：
                        def createStudent(cls,name,age,gender,contend,grade,lastT,creatT,isD=False):     #    cls:代表继承自student，与createStudent(student)的效果一致
                            stu = cls(sname=name,sage=age,sgender=gender,scontend=contend,sgrade=grade,lastTime=lastT,createTime=creatT)
                            return stu
                  
                  在自定义管理器中添加一个方法：
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
        
        模型查询：
            概述：
                查询集表示从数据库获取的对象的集合
                查询集可以有多个过滤器
                过滤器就是一个函数，基于所给的参数限制查询集结果
                从sql角度来说，查询集合select语句等价，过滤器就像where条件
            
            查询集：
                在管理器上调用过滤器方法返回查询集
                查询集经过过滤器筛选后返回新的查询集，所以可以写成链式调用
                惰性执行：
                    创建查询集不会带来任何数据的访问，直到调用数据时，才会访问数据
                    
                直接访问数据的情况：
                    迭代
                    序列化
                    与if合用
                    
                返回查询集的方法成为过滤器：
                    all()：返回查询集中的所有数据
                    filter:返回符合条件的数据
                        filter(键=值)
                        filter(键=值，键=值)
                        filter(键=值),filter(键=值)
                    exclucle():
                        过滤掉符合条件的数据
                    order_by():排序
                    values():一条数据就是一个对象（字典），返回一个列表
                
                返回单个数据：
                    get():
                        满足一个条件的对象
                        注意：
                            如果没有找到符合条件的对象，会引发“模型类.DoesNotExist”异常
                            如果找到多个对象，会引发“模型类.MultipleObjectsReturned”异常
                    count():返回当前查询集的对象个数
                    first():返回查询集中的第一个对象
                    last():返回查询集中的最后一个对象
                    exists():判断查询集是否有数据，如果有数据返回true
                
                限制查询集：
                    查询集返回列表，可以使用下标的方法进行限制，等同于sql中的limit语句
                    代码：student_list = student.stuobj.all()[0:3]
                    注意：下标不能是负数
                
                查询集的缓存
                    概述：
                        每个查询集都包含一个缓存，来最小化对数据库访问
                        在新建的查询集缓存中，缓存首次为空，第一次对查询集求值，会发生数据缓存，django会将查询出来的数据做一个缓存
                
                字段查询：
                    概述：
                        实现sql中的where语句，作为方法filter()、exclude()、get()的参数
                        语法：属性名称_比较运算符=值
                        外键：属性名_id
                        转义：
                            like语句中使用%是为了匹配占位，匹配数据中带有%的数据（where like '\%'）
                            代码：filter(sanme__contains='%')
                    比较运算符：
                        exact：
                            判断，大小写敏感
                            等同：filter(siDelte=False)
                        contains：
                            是否包含，大小写敏感
                            代码：student_list=student.stuobj.filter(sname__contains='谢')
                        startswith、endswith：
                            以value开头或者结尾，大小写敏感
                            代码：student_list=student.stuobj.filter(sname__startswith='谢')
                        以上四个在前面加上i，就表示不区分大小写(iexact、icontains、istartswith、iendswith)
                        isnull、isnotnull：
                            是否为空
                            代码：filter(sname__isnull=False)
                        in：
                            是否包含在范围内
                            代码：student_list=student.stuobj.filter(pk__in=[1,2,3,4])
                        gt、gte、lt、lte：
                            （大于、大于等于、小于、小于等于）
                            代码：student_list=student.stuobj.filter(sage__gt=15)
                            
                        year、month、day、week_day、hour、minute、second：
                                （年、月、日、周期、时、分、秒）
                                代码：student_list=student.stuobj.filter(createTime__year=2020)
                        跨关联查询：
                            处理join查询:
                                语法：模型类名__属性名__比较运算符
                                代码：
                                    grade = Grades.objects.filter(student__scontend__contains='xx')     #查询scontent字段值中带有‘xx’的班级
                                    print(grade)
                        
                        查询快捷：
                            pk:
                                代表主键
                    
                    聚合函数：
                        使用aggregate()函数返回聚合函数的值
                        Avg
                        Count
                        Max:
                            代码：
                                from django.db.models import Max
                                maxAge = student.stuobj.aggregate(Max('sage'))
                        Min
                        Sum
                    
                    F对象：
                        可以使用模型的A属性与B属性进行比较：                       
                            代码：
                                from django.db.models import F,Q
                                def girl_class(request):
                                    g = Grades.objects.filter(ggirlnum__gt=F('gboynum'))    #查询女生比男生多的班级
                                    print(g)
                                    return HttpResponse('girls class!!!')
                        
                        支持F对象的算术运算：
                            代码：g = Grades.objects.filter(ggirlnum__gt=F('gboynum')+20)    #查询女生比男生多的班级
                    
                    Q对象：
                        概述：
                            过滤器的方法中的关键字参数，条件为And模式
                        需求：
                            进行or查询
                        解决：
                            使用Q对象
                        代码：
                            student_list = student.stuobj.filter(Q(pk__lte=3) | Q(sage__gt=15))  #查询id小于等于3 或 年龄大于15的数据
                            student_list = student.stuobj.filter(Q(pk__lte=3))  #只有一个Q对象，就是用于匹配
                            student_list = student.stuobj.filter(~Q(pk__lte=3)) #加~，取相反的结果
                        




'''
