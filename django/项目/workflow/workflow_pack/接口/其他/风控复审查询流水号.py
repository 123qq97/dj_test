import requests
from workflow_pack.接口.公共.登录 import login


def select_risk_num(odd_num):
    html, response = login(url='http://189i0341c8.iok.la:27031/web-surety/login/login', username='13417664959')
    head_url = 'http://189i0341c8.iok.la:27031'
    # 待审查列表
    will_list_url = head_url + '/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?positionId=6c0923db-044c-4675-a57e-15c3be698e18&finishPerson=aaa9aa4a-32d7-4fd5-ae61-ca4e66017f1b&configCode=WIND_CONTROL'
    # 审查弹窗
    message_url = head_url + '/web-surety/security/open/task/pickExaminerReviewApproveInfo?id='
    # 已审查列表
    already_list_url = head_url + '/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPersonApproved?finishPerson=aaa9aa4a-32d7-4fd5-ae61-ca4e66017f1b&configCode=WIND_CONTROL'

    null = ''
    true = 'true'
    false='false'
    #待审批列表返回的数据个数
    response1 = html.get(will_list_url).text
    response1 = eval(response1)
    will_recordCount=response1['result']['recordCount']
    #已审批列表返回的数据个数
    response3 = html.get(already_list_url).text
    response3 = eval(response3)
    already_recordCount = response3['result']['recordCount']
    all_list={}
    all_list['will_list'] = {}
    all_list['already_list'] = {}

    #查找待审批列表
    for x in range(int(will_recordCount / 20) + 1):
        currentPage = x + 1
        will_list_url1 = already_list_url + '&currentPage=' + str(currentPage)
        response1_1 = html.get(will_list_url1).text
        response1_1 = eval(response1_1)
        for j, i in enumerate(response1_1['result']['itemList']):
            will_bizEntityId = i['bizEntityId']
            will_instanceNumber=i['instanceNumber']
            message_url1 = message_url + will_bizEntityId
            response2 = html.get(message_url1).text
            response2 = eval(response2)
            guaranteeNum = response2['result']['guaranteeMessage']['guarantee']['guaranteeNum']
            all_list['will_list'][guaranteeNum]=will_instanceNumber


    #查找已审批列表
    for x in range(int(already_recordCount / 20) + 1):
        currentPage=x+1
        already_list_url1=already_list_url+'&currentPage='+str(currentPage)
        response4=html.get(already_list_url1).text
        response4=eval(response4)
        for y in response4['result']['itemList']:
            already_bizEntityId=y['bizEntityId']
            already_instanceNumber=y['instanceNumber']
            message_url2 = message_url + already_bizEntityId
            response5=html.get(message_url2).text
            response5=eval(response5)
            guaranteeNum1=response5['result']['guaranteeMessage']['guarantee']['guaranteeNum']
            all_list['already_list'][guaranteeNum1]=already_instanceNumber

    if odd_num in all_list['will_list'].keys():
        instanceNumber=all_list['will_list'][odd_num]
        return instanceNumber
    elif odd_num in all_list['already_list'].keys():
        instanceNumber=all_list['already_list'][odd_num]
        return instanceNumber
    else:
        print('未找到单号对应的流水号！')

print(select_risk_num('E2005280005'))
