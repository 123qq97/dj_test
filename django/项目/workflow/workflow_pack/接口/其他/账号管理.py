import requests
from workflow_pack.接口.公共.登录 import login


class account_number():
    def __init__(self,account_name,assignType,assignEntityId,login_number='17666121214',head_url='http://192.168.0.58:82'):
        '''
        login_number:登录账号；尽量拿数据权限多的账号，否则会查询不到对应账号信息；考虑到不同环境测试账号不同，改为输入形式
        account_name：审批人或岗位名称；用于过滤数据
        assignType：审批类型；用于判断是按岗位id或人员id过滤数据
        assignEntityId：岗位id或人员id；用于找到对应审批账号
        head_url:域名;考虑不同环境测试，所以设为变量
        '''
        self.head_url = head_url
        self.account_name=account_name
        self.assignType=assignType
        self.assignEntityId=assignEntityId
        self.html,self.login_detail = login(url='http://189i0341c8.iok.la:27031/web-surety/login/login', username=login_number)
        global null, true,false
        null = 'null'
        true = 'true'
        false = 'false'


    #获取账号信息：  姓名、岗位、账号
    def queryPersonLink(self):
        try:
            # 查询所有平台机构orgid：   平台机构与平台机构是同级，都在亮度金服下，拿到不同机构orgid查询对应机构账号
            orgid_list=[]
            queryOrgTree_url=self.head_url+'/web-surety/security/open/org/queryOrgTree?status=ENABLED'
            org_response=self.html.get(queryOrgTree_url).text
            org_response=eval(org_response)
            for i in org_response['result']:
                orgid_list.append(i['id'])



            #查询对应机构账号
            account_number_list = []
            for orgId in orgid_list:
                #账号管理列表
                queryPersonLink_url =self.head_url+ '/web-surety/security/erp/auth/person/queryPersonLink?orgId='+orgId+'&searchName='+self.account_name
                response=self.html.get(queryPersonLink_url).text
                response=eval(response)

                #根据岗位类型，找出对应的id的人或岗位,且该员工为启用状态
                for i in response['result']['itemList']:
                    if self.assignType=='PERSON' and i['id']==self.assignEntityId and i['suretyStatus']=='ENABLED':
                        phone=i['phone']
                        # print(phone,i['name'],i['positionName'])
                        account_number_list.append(phone)
                    elif self.assignType=='POSITION' and i['positionLinkId']==self.assignEntityId and i['suretyStatus']=='ENABLED':
                        phone=i['phone']
                        account_number_list.append(phone)
                        # print(phone,i['name'],i['positionName'])

            print(account_number_list)
        except Exception as e:
            return print(e.args,'获取审批账号信息失败！！！')




    def ishave_jurisdiction(self):
        pass

    def is_admin(self):
        pass






if __name__ == '__main__':
    a=account_number(head_url='http://189i0341c8.iok.la:27031',login_number='17666121214',assignType='POSITION',account_name='风控经理',assignEntityId='6c0923db-044c-4675-a57e-15c3be698e18')
    a.queryPersonLink()
