import requests
import json

'''
environment:切换测试、预发布环境
if else判断是否为传入的链接
'''


def login(url='http://192.168.0.58:82/web-surety/login/login',username='13714028085',password='123456',wxOpenId='',loading='false',environment='58'):
    if url!='http://192.168.0.58:82/web-surety/login/login':
        params = 'userName=' + username + '&password=' + password + '&wxOpenId=' + wxOpenId + '&loading=' + loading
        html = requests.session()
        response = html.get(url,params=params)
        return html,response

    else:
        params='userName='+username+'&password='+password+'&wxOpenId='+wxOpenId+'&loading='+loading
        url=url.replace('192.168.0.58','192.168.0.'+environment)
        html=requests.session()
        response=html.get(url,params=params)
        return html,response


