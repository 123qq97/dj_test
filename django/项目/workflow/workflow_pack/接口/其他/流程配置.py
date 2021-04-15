import requests
from workflow_pack.接口.公共.登录 import login


class process_configuration:
    def __init__(self,bizCode,login_number,nodeId,head_url='http://192.168.0.58:82'):
        '''
                nodeid：节点id
                start_nodeid:初始值为开始节点id，后面将destinationId字段值赋给他
                end_nodeid：结束节点id
                destinationId:目的节点（下一节点）
                fromid：来源节点（当前节点）
                assignType:审批类型
                assignEntityName:审批对象名
                assignEntityId:审批对象id
        '''
        self.head_url=head_url
        self.bizCode=bizCode
        self.nodeId=nodeId
        self.html=login(url='http://189i0341c8.iok.la:27031/web-surety/login/login', username=login_number)[0]
        global null,true,false
        null='null'
        true='true'
        false = 'false'

    #获取审批人员信息
    def process_details(self):
        try:
            details_url = self.head_url + '/web-surety/security/workflow/process/searchProcessByCode?status=ENABLED&bizCode=' + self.bizCode
            response = self.html.get(details_url).text
            response = eval(response)
            node_lsit = {}  # 整理返回后的数据

            #当节点id相同时，返回审批人员的信息
            for i in response['result']['nodeList']:
                if self.nodeId==i['id']:
                    node_lsit['assignType'] = i['assignType']
                    node_lsit['assignEntityName'] = i['assignEntityName']
                    node_lsit['assignEntityId'] = i['assignEntityId']

            print(node_lsit)
            return node_lsit
        except Exception as e:
            return print(e.args,'获取审批人员信息')











    #(不用)流程节点排序，并获取子流程节点:     审批类型、审批对象名称、审批对象id
    def process_order(self):
        global start_nodeid, end_nodeid
        details_url=self.head_url+'/web-surety/security/workflow/process/searchProcessByCode?status=ENABLED&bizCode='+self.bizCode
        response=self.html.get(details_url).text
        response=eval(response)
        node_lsit={}                            #整理返回后的数据

        #获取开始、结束节点的id
        for j,i in enumerate(response['result']['nodeList']):
            nodeName = i['nodeName']
            nodeid = i['id']
            if nodeName=='开始节点':
                start_nodeid=nodeid
            elif nodeName=='结束节点':
                end_nodeid=nodeid

        # 节点顺序排序
        def node_order(start_nodeid,end_nodeid):
            for i in response['result']['nodeList']:#获取接口中nodeList的信息(节点的详细信息；如：id、名称、审批人、类型等)
                nodeName = i['nodeName']
                nodeid = i['id']
                assignType = i['assignType']
                assignEntityName = i['assignEntityName']
                assignEntityId = i['assignEntityId']


                for j in response['result']['lineList']: #获取接口中lineList的信息(从某节点到某节点的顺序)
                    destinationId = j['destinationId']
                    fromid = j['from']

                    if nodeid==start_nodeid :                           #判断节点的id是否等于start_nodeid;   start_nodeid:变量，初始值为开始节点id，后面将destinationId字段值赋给他
                        if fromid==start_nodeid:                        #判断fromid是否等于start_nodeid
                            if nodeName=='开始节点':
                                # node_lsit[nodeName] = [nodeid,destinationId]
                                pass
                            else:
                                node_lsit[nodeName]=[assignType,assignEntityName,assignEntityId]

                            start_nodeid=destinationId
                            node_order(start_nodeid,end_nodeid)
                            return

                        elif end_nodeid==start_nodeid:
                            # node_lsit[nodeName] = [nodeid]
                            return

        # 调用方法，对节点排序
        node_order(start_nodeid,end_nodeid)
        return node_lsit





if __name__ == '__main__':
    p=process_configuration(head_url='http://189i0341c8.iok.la:27031',bizCode='291',login_number='13323594169',nodeId='b0f27618-2303-48d4-8415-ea8d6eee3bc4')
    assign=p.process_details()

    from 接口.其他.账号管理 import account_number
    account_name = assign['assignEntityName'].split('-')
    account_name = account_name[-1]
    a = account_number(head_url='http://189i0341c8.iok.la:27031', login_number='17666121214', assignType=assign['assignType'],
                       account_name=account_name, assignEntityId=assign['assignEntityId'])
    a.queryPersonLink()


