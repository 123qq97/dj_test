import requests
from workflow_pack.接口.公共.登录 import login
import json


class task_approval:
    def __init__(self, odd_num, head_url='http://192.168.0.58:82',node_name=''):
        if odd_num=='':
            return print('单号不能为空')
        else:
            self.node_name=node_name
            self.head_url = head_url
            self.odd_num = odd_num
            self.html, result = login(url='http://189i0341c8.iok.la:27031/web-surety/login/login', username='17666121214')
            global null, true
            null = ''
            true = ''
            self.processInstanceId=self.task_list()

    def task_list(self):

        # 流程审批列表
        task_list_url = self.head_url + '/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?finishPerson=0f15e23f-e317-414a-a990-c7cd31d073c9&positionId=2820f1ef-6a9e-42d6-af6b-f7705beebfef&processName=' + self.odd_num
        response = self.html.get(task_list_url).text
        response = eval(response)
        processInstanceId = response['result']['itemList'][0]['processInstanceId']
        return processInstanceId


    # 平台流程审批
    def platform_task(self):
        try:
            # 流程审批窗口
            task_select_url = self.head_url + '/web-surety/security/open/task/getHisAndRunTaskListByProcInstId?id=' + self.processInstanceId
            # 流程审批办理
            task_handle_url = self.head_url + '/web-surety/security/workflow/task/passTask'

            response = self.html.get(task_select_url).text
            response = eval(response)

            for j, i in enumerate(response['result']):
                if i['taskStatus'] == 'RUNNING':
                    operatorId = response['result'][j]['updateOperatorId']
                    taskId = response['result'][j]['id']

                    # 流程审批办理
                    data1 = {"operatorId": operatorId, "taskId": taskId, "remark": ""}
                    data1 = json.dumps(data1, ensure_ascii=False)
                    response1 = self.html.post(task_handle_url, data1.encode(),
                                               headers={'Content-Type': 'application/json'})
                    print(response1.text, self.node_name+'审批成功')
                    self.platform_task()
                    # break
                    return response1.text, self.node_name+'审批成功'
        except Exception as e:
            print(e.args,'流程审批异常')


if __name__ == '__main__':
    t = task_approval(head_url='http://189i0341c8.iok.la:27031', odd_num='')
    t.platform_task()
