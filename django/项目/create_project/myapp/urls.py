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
    path('attribles/',views.attribles),
    path('get1/',views.get1),
    path('get2/',views.get2),
    path('showregist/',views.showregist),
    path('showregist/regist/',views.regist),
    path('showresponse/',views.showresponse),
    path('cookietest/',views.cookietest),
    path('redirect1/',views.redirect1),
    path('redirect2/',views.redirect2),
    # path('main/',views.main),
    path('login/',views.login),
    path('showmain/',views.showmain),
    path('ifexample/',views.if_example),
    path('forexample/',views.for_example),
    path('forexample/good/',views.good),
    path('base_main/',views.base_main),
    path('base_detail/',views.base_detail),
    path('postfile/',views.postfile),
    path('showinfo/',views.showinfo),

    path('verifycode/',views.verifycode),
    path('verifycodefile/',views.verifycodefile),
    path('verifycodecheck/',views.verifycodecheck),

    path('upfile/',views.upfile),
    path('savefile/',views.savefile),

    re_path(r'^studentpage/(\d+)/$',views.studentpage),

    path('ajaxstudent/',views.ajaxstudent),
    path('studentinfo/',views.studentinfo),

    path('edit/',views.edit),

    path('celery/',views.celery)
]