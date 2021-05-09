from django.contrib.auth.decorators import login_required   #登录session校验函数，session超时自动跳转登录页

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        #调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)