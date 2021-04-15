'''
-----------------------------------------------------模板---------------------------------------------------------------
定义模板：
    变量：
        视图传递给模板的数据
        要遵守标识符规则
        语法：{{ var }}
        注意：如果使用的变量不存在，则插入的是空字符串
        在模板中使用点语法：
            字典查询
            属性或方法
            数字索引
        在模板中调用对象的方法：
            注意：不能传递参数
    
    标签：
        语法：{{% tag %}}
        作用：
            在输出中创建文本
            控制逻辑和循环
        if：
            格式：
                例1：
                    {% if 表达式 %}
                    语句
                    {% endif %}
                例2：
                    {% if 表达式1 %}
                    语句1
                    {% else %}
                    语句2
                    {% endif %}
                例3：
                    {% if 表达式1 %}
                    语句1
                    {% elif 表达式2%}
                    语句2
                    {% elif 表达式n %}
                    语句n
                    {% else %}
                    语句e
                    {% endif %}
            代码：
                {% if num %}
                    num:{{num}}
                {% endif %}
                    
        for：
            格式：
                例1：
                    {% for 变量 in 列表 %}
                    语句
                    {% endfor %}
                例2：
                    {% for 变量 in 列表 %}
                    语句1
                    {% empty %}
                    语句2
                    {% endfor %}
                    注意：列表为空或列表不存在时执行语句2
                例3：{{ forloop.counter }} 表示当前是第几次循环
            代码：
                <ul>
                    {% for i in student_lists %}
                        <li>
                            {{ forloop.counter }}--{{ i.sname }}
                        </li>
                    {% empty %}
                        <li>此列表没有学生</li>
                    {% endfor %}
                </ul>
        
        comment:
            作用：多行注释
            格式：
                {% comment %}
                内容
                {% endcomment%}
            代码：
            {% comment %}
            <p>321321321</p>
            <p>注释的内容</p>
            {% endcomment %}
            
        ifequal、ifnotequal：
            作用：如果值1=值2，执行语句
            代码：
                {% ifequal '值1' '值1' %}
                    <p>判断值1=值2，等于则输出</p>
                {% endifequal %}
        
        include：
            作用：加载模板并以标签内的参数渲染
            格式：{% include '模板目录' 参数1 参数2 %}
        
        url：
            作用：反向解析
            格式：{% url'namespace:name' p1 p2 %}
        
        csrf_token:
            作用：用于跨站请求伪造保护
            格式：{% csrf_token %}
        
        block、extends:
            作用：用于模板的继承
            
        autoescape：
            作用：用于HTML的转义
    
    过滤器：
        语法：{{var|过滤器}}
        作用：在变量被显示前修改它
        小写：
            lower
        大写：
            upper:
                代码：<h1>{{ str_name|upper }}</h1>
        过滤器可以传递参数，参数用引号引起来：
            join：
                格式：{{ 列表|join:'#' }}
                示例：<h1>{{ list_name|join:'#' }}</h1>
        如果一个值没有被提供，或者值为False、空，可以使用默认值：
            default：
                格式：{{ var|default:'默认值' }}
                示例：<h1>{{ test|default:'没有这个值' }}</h1>
        根据给定格式转换日期为字符串：
            data：
                格式：{{ dataVal|data:'y-m-d' }}
        HTML转义：
            作用：
                将接收到的code当成普通字符串渲染：
                    escape：
                        格式：{{ code|escape }}
                将接收到的字符串当成HTML代码渲染：
                    代码：
                        方法一（单行）：
                            {{变量|safe}}
                        方法二（多行）：
                            {% autoescape off %}
                            {{变量}}
                            {% endautoescape %}
            
        加减乘除：
            代码：
                <h1>num= {{num}}</h1>
                <!--  num+10  -->
                <h1>{{num|add:10}}</h1>
                <!--  num-5  -->
                <h1>{{num|add:-5}}</h1>
                <!--  num*5  -->
                <h1>{% widthratio num 1 5 %}</h1>
                <!--  num/5  -->
                <h1>{% widthratio num 5 1 %}</h1>
        
        注释：
            单行注释：
                格式：{# 注释内容 #}
        
        反向解析：
            作用：方便编写url地址，例如："index/for_example",可以简写为"for_example"
            
        模板继承：
            作用：模板继承可以减少页面内容的重复定义，实现页面的重用
            block标签：
                作用：在父模板中预留区域，子模板去填充
                语法：
                    {% block 标签名 %}
                    {% endblock 标签名 %}
            extend标签：继承模板，需要写在模板文件的第一行
            示例：
                定义父模板:
                    代码：详见myapp/base.html
                定义子模版    
                    代码：详见myapp/base_main.html
        
        CSRF（系统默认启用）:
            防止跨站请求伪造：某些恶意网站包含链接、表单、按钮、js，利用登录用户在浏览器中认证，从而攻击服务
            如何关闭CSRF校验：
                方法一：在setting.py文件中，MIDDLEWARE中注释'django.middleware.csrf.CsrfViewMiddleware'这段
                方法二：
                    {% csrf_token %}，插入这段代码，详见：postfile.html与showinfo.html文件



















'''