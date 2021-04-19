from django.urls import path,re_path
from .views import RegisterView,ActiveView,LoginView

urlpatterns = [
    # path('register/', views.register, name='register'), #注册
    # path('register_handle', views.register_handle, name='register_handle'), #注册
    path('register/', RegisterView.as_view(), name='register'), #注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), #用户激活
    path('login/', LoginView.as_view(), name='login'), #登录
]
