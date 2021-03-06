"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    https://www.bilibili.com/video/BV1vt41147K8?p=18
    django-celery     --3.3.1
    django-redis      --4.12.1
    celery-with-redis --3.0
    redis             --2.10.6
    celery            --3.1.26.post2
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),  #富文本编辑器
    path('user/', include(('user.urls','user'),namespace='user')),
    path('cart/', include(('cart.urls','cart'),namespace='cart')),
    path('order/', include(('order.urls','order'),namespace='order')),
    path('', include(('goods.urls','goods'),namespace='goods')),
]
