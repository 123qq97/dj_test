import requests
from workflow_pack.接口.公共.登录 import login
import json
from workflow_pack.接口.其他.时间转换 import local_to_utc
from workflow_pack.接口.其他.时间转换 import local_to_time_stamp
import datetime
import time
from workflow_pack.接口.公共.筛选替换文字 import screen
from workflow_pack.接口.其他.增加额度 import add_quota
from workflow_pack.接口.其他.流程审批 import task_approval


# 链接    面签['查询列表get','请求办理post']
url = {
    '报单列表': ['http://192.168.0.58:82/web-surety/security/business/guarantee/guaranteePage?keyWord=',
             'http://192.168.0.58:82/web-surety/security/open/guarantee/pickGuaranteeMessage?id='],
    '资金机构': ['http://192.168.0.58:82/web-surety/security/fundPackage/insertFundPackage'],
    '面签': [
        'http://192.168.0.58:82/web-surety/security/interviewVisa/queryInterviewVisaRiskPage?pageSize=20&currentPage=1&keyword=E2005110012&productId=&businessSourceId=&interviewState=&checkStatus=',
        'http://192.168.0.58:82/web-surety/security/interviewVisa/submitInterviewVisa'],
    '核行': [
        'http://192.168.0.58:82/web-surety/security/checkBank/queryCheckBankRiskPage?pageSize=20&currentPage=1&keyword=E2005110012&productId=&businessSourceId=&interviewState=&checkStatus=',
        'http://192.168.0.58:82/web-surety/security/checkBank/commitCheckBank'],
    '运营初审': [
        'http://192.168.0.58:82/web-surety/security/risk/riskOperateApproval/queryRiskOperateToBeApprovalPage?pageSize=20&currentPage=1&keyword=E2005110012&productId=&isReceive=&businessSourceId=&examinerId=&companyId=f0cfce2d-765d-4a11-99fb-7a572628c883',
        'http://192.168.0.58:82/web-surety/security/risk/riskOperateApproval/receive',
        'http://192.168.0.58:82/web-surety/security/risk/riskOperateApproval/approvalPass'],
    '风控初审': [
        'http://192.168.0.58:82/web-surety/security/risk/riskFirstApproval/queryRiskFirstToBeApprovalPage?companyId=f0cfce2d-765d-4a11-99fb-7a572628c883&&orgId=2dbb1bc7-8f87-431b-b64b-7fb9850233aa&keyword=E2005110012',
        'http://192.168.0.58:82/web-surety/security/risk/riskFirstApproval/receive',
        'http://192.168.0.58:82/web-surety/security/risk/riskFirstApproval/selectApprovalInfoById?id=',
        'http://192.168.0.58:82/web-surety/security/risk/riskApprovalSub/selectFundInfo?',
        'http://192.168.0.58:82/web-surety/security/risk/riskFirstApproval/approvalPass'],
    '风控复审': [
        'http://192.168.0.58:82/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?processName=E2005110012&startDate=&endDate=&systemKey=RISK_SYS&finishPerson=0f15e23f-e317-414a-a990-c7cd31d073c9&currentPage=1&pageSize=20&positionId=2820f1ef-6a9e-42d6-af6b-f7705beebfef',
        'http://192.168.0.58:82/web-surety/security/open/task/getHisAndRunTaskListByProcInstId?id=',
        'http://192.168.0.58:82/web-surety/security/workflow/task/passTask'],
    '收费': [
        'http://192.168.0.58:82/web-surety/security/fee/queryFundFeePage?limitStartDate=&limitEndDate=&companyId=&feeStage=&pageSize=20&currentPage=1&keyword=E2005110012',
        'http://192.168.0.58:82/web-surety/security/fee/insertBeforeLoanFee'],
    '收要件': [
        'http://192.168.0.58:82/web-surety/security/fnEssentialsTake/queryFnEssentialsTakePage?essentialsTakeStatus=&pageSize=20&currentPage=1&companyId=&keyword=E2005110012',
        'http://192.168.0.58:82/web-surety/security/fnEssentialsTake/saveFnEssentialsTake',
        'http://192.168.0.58:82/web-surety/security/fnEssentialsTake/takeCompleteConfirm'],
    '执行岗备注': [
        'http://192.168.0.58:82/web-surety/security/risk/riskExecutionRemarks/queryToBeRiskExecutionRemarksPage?pageSize=20&currentPage=1&keyword=E2005110012&orgId=2dbb1bc7-8f87-431b-b64b-7fb9850233aa&companyId=f0cfce2d-765d-4a11-99fb-7a572628c883',
        'http://192.168.0.58:82/web-surety/security/risk/riskExecutionRemarks/insertRiskExecutionRemarks'],
    '保函寄送': [
        'http://192.168.0.58:82/web-surety/security/risk/riskGuaranteeMain/queryRiskGuaranteeMainPage?pageSize=20&currentPage=1&keyword=E2005110012&productId=&businessSourceId=&sendState=',
        'http://192.168.0.58:82/web-surety/security/risk/riskGuaranteeSend/insertRiskGuaranteeSend'],
    '资金到账': {'资金安排': ['http://192.168.0.58:82/web-surety/security/fundApply/queryFundApplyPage?keyword=E2005110012',
                      'http://192.168.0.58:82/web-surety/security/fundApply/pickFundApplyInfo?id=',
                      'http://192.168.0.58:82/web-surety/security/fundApply/submitFundApply',
                      'http://192.168.0.58:82/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?startDate=&endDate=&systemKey=FUND_SYS&finishPerson=0f15e23f-e317-414a-a990-c7cd31d073c9&currentPage=1&pageSize=20&positionId=2820f1ef-6a9e-42d6-af6b-f7705beebfef&processName=',
                      'http://192.168.0.58:82/web-surety/security/open/task/getHisAndRunTaskListByProcInstId?id=',
                      'http://192.168.0.58:82/web-surety/security/workflow/task/passTask'], '资料推送': [
        'http://192.168.0.58:82/web-surety/security/fundApply/queryNoPushFundApplyPage?keyword=E2005110012',
        'http://192.168.0.58:82/web-surety/security/fundApply/getPayeeAccountByOrderId?id=',
        'http://192.168.0.58:82/web-surety/security/fundApply/pushFundOrg'], '到账管理': [
        'http://192.168.0.58:82/web-surety/security/fundApply/queryIsArrivalAccountFundApplyPage?planBillingStartDate=&planBillingEndDate=&fundOrgId=&cityCode=&companyId=&keyword=E2005110012&pageSize=20&currentPage=1',
        'http://192.168.0.58:82/web-surety/security/fundApply/updateArrivalAccountStatus']},
    '查档查诉讼': [
        'http://192.168.0.58:82/web-surety/security/risk/riskCheckDocLawsuit/queryUncheckOrders?pageSize=20&currentPage=1&companyId=&productId=&keyWord=E2005110012&planUseTime=&planEndTime=',
        'http://192.168.0.58:82/web-surety/security/risk/riskCheckDocLawsuit/checkDocAndLawsuitDetail?checkDocLawsuitId=',
        'http://192.168.0.58:82/web-surety/security/risk/riskCheckDocLawsuit/updateCheckDocAndLawsuit'],
    '收取保证金': [
        'http://192.168.0.58:82/web-surety/security/billing/queryBillingPage?realBillingStartDate=&realBillingEndDate=&keyword=E2005110012&companyId=&billingStatus=&currentPage=1&pageSize=20',
        'http://192.168.0.58:82/web-surety/security/fnBusinessAssure/saveFnBusinessAssure'],
    '出款申请': [
        'http://192.168.0.58:82/web-surety/security/fnRedeem/queryFnRedeemPage?redeemStartDate=&redeemEndDate=&redeemStatus=&companyId=&keyword=E2005110012&currentPage=1&pageSize=20',
        'http://192.168.0.58:82/web-surety/security/billing/queryLoanDetails?orderId=',
        'http://192.168.0.58:82/web-surety/security/billing/applyBilling'],
    '出款审批': [
        'http://192.168.0.58:82/web-surety/security/billing/queryBillingPage?realBillingStartDate=&realBillingEndDate=&keyword=E2005110012&companyId=&billingStatus=&currentPage=1&pageSize=20',
        'http://192.168.0.58:82/web-surety/security/billing/findBillingAccountByBillingDetailsId?id=',
        'http://192.168.0.58:82/web-surety/security/billing/auditBilling'],
    '流程审批': [
        'http://192.168.0.58:82/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?processName=E2005110012&startDate=&endDate=&systemKey=FUND_SYS&finishPerson=0f15e23f-e317-414a-a990-c7cd31d073c9&currentPage=1&pageSize=20&positionId=2820f1ef-6a9e-42d6-af6b-f7705beebfef',
        'http://192.168.0.58:82/web-surety/security/open/task/getHisAndRunTaskListByProcInstId?id=',
        'http://192.168.0.58:82/web-surety/security/workflow/task/passTask'],
    '出款': [
        'http://192.168.0.58:82/web-surety/security/billing/queryBillingPage?realBillingStartDate=&realBillingEndDate=&keyword=E2005110012&companyId=&billingStatus=&currentPage=1&pageSize=20',
        'http://192.168.0.58:82/web-surety/security/billing/confirmBilling',
        'http://192.168.0.58:82/web-surety/security/billing/billingCheckOtp'],
    '赎楼': [
        'http://192.168.0.58:82/web-surety/security/fnRedeem/queryFnRedeemPage?redeemStartDate=&redeemEndDate=&redeemStatus=&companyId=&keyword=E2005110012&currentPage=1&pageSize=20',
        'http://192.168.0.58:82/web-surety/security/fnRedeem/saveFnRedeem'],
    '取原证': [
        'http://192.168.0.58:82/web-surety/security/fnCertTake/queryFnCertTakePage?companyId=&pageSize=20&takeCertStatus=&takeCertDateStart=&takeCertDateEnd=&currentPage=1&keyword=E2005110012',
        'http://192.168.0.58:82/web-surety/security/fnCertTake/insertFnCertTake'],
    '权证管理': ['http://192.168.0.58:82/web-surety/security/platformProductEvid/list?keyword=E2005110012',
             'http://192.168.0.58:82/web-surety/security/platformProductEvid/sendOrerRecord',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/queryCertLogout?keyWord=E2005110012&positionType=CERT_LOGOUT',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/redeemCertLLogoutSave',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/queryTransfer?keyWord=E2005110012&positionType=TRANSFER',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/redeemTransferSave',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/queryTakeNewCert?keyWord=E2005110012&positionType=TAKE_NEW_CERT',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/redeemTakeNewCertSave',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/queryTakeNewCert?keyWord=E2005110012&positionType=MORTGAGE',
             'http://192.168.0.58:82/web-surety/security/risk/handleAfterForeclosure/redeemMortgageSave']

}
# 转换为本地链接
url = eval(screen(url, key='192.168.0.58:82', value='189i0341c8.iok.la:27031'))


class process:
    def __init__(self, odd_num):
        self.html, result = login(url='http://189i0341c8.iok.la:27031/web-surety/login/login', username='17666121214')
        self.odd_num = odd_num
        self.companyId = "f0cfce2d-765d-4a11-99fb-7a572628c883"
        self.takeDate = str(datetime.date.today())
        self.chargeDate = local_to_utc()
        self.stampDate = local_to_time_stamp()
        global null, true

        # 查询担保单列表,获取单号对应id
        guarateeID_url = url['报单列表'][0] + odd_num
        null = ''
        true = ''
        false = ''
        response = self.html.get(guarateeID_url).text
        response = eval(response)
        # 取值字段
        id = response['result']['items'][0]['id']

        guarateetype_url = url['报单列表'][1] + id
        response1 = self.html.get(guarateetype_url).text
        response1 = eval(response1)
        self.fundType = response1['result']['bizTypeModel']['fundType']
        self.transactionType = response1['result']['bizTypeModel']['transactionType']

    # def start(self):
    #     self.face_signature()

    # 面签
    def face_signature(self):
        try:
            # 查询面签列表,获取单号对应id
            face_url = url['面签'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            id = response['result']['items'][0]['id']

            # 办理面签,需要获取列表单号对应id
            data = {
                "associatesFileInfoList": [], "handlePersonType": "MECHANISM_HANDLE", "interviewAddress": "面签地址1",
                "interviewTime": "2020-05-11T01:32:37.258Z", "remark": "备注1", "source": "PC",
                "transactorOperatorName": "张admin", "id": id, "systemKey": "RISK_SYS"
            }
            data = json.dumps(data)
            response1 = self.html.post(url['面签'][1], data, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------平台面签')
            return response1.text, '----------------平台面签'
            # self.nuclear_row()
        except:
            return print('平台面签失败')

    # 核行  (原贷款：LOAN_SELLER|新贷款：LOAN_BUYER)
    def nuclear_row(self, loanType=['LOAN_SELLER', 'LOAN_BUYER']):
        for i, j in enumerate(loanType):
            try:
                # 查询核行列表
                face_url = url['核行'][0].replace('E2005110012', self.odd_num)
                null = ''
                true = ''
                response = self.html.get(face_url).text
                response = eval(response)
                # 取值字段
                checkBankGeneralId = response['result']['items'][0]['id']
                orderId = response['result']['items'][0]['orderId']

                # 办理核行,需要获取列表单号对应id
                data = {"associatesFileIdList": [], "checkBankDetail": {"address": "核行地址1", "backContactPerson": "梁涛",
                                                                        "backContactPhone": "15592245136",
                                                                        "checkBankGeneralId": checkBankGeneralId,
                                                                        "checkTime": "2020-05-11T02:10:28.172Z",
                                                                        "checkType": "SITE_CHECKED_BANK",
                                                                        "handlePersonName": "张admin",
                                                                        "handlePersonType": "MECHANISM_HANDLE",
                                                                        "loanBackName": "中国人民银行南头支行",
                                                                        "loanBackId": "84E6FDE441A44D37E055000000000001",
                                                                        "loanType": j, "remark": "备注1", "source": "PC"
                                                                        }, "orderId": orderId, "systemKey": "RISK_SYS"}
                data = json.dumps(data)
                response1 = self.html.post(url['核行'][1], data, headers={'Content-Type': 'application/json'})
                if j == 'LOAN_SELLER':
                    print('平台原贷款核行通过')
                    return '平台原贷款核行通过'
                elif j == 'LOAN_BUYER':
                    print('平台新贷款核行通过')
                    return '平台新贷款核行通过'
            except:
                if j == 'LOAN_SELLER':
                    return print('平台原贷款核行不通过')
                elif j == 'LOAN_BUYER':
                    return print('平台新贷款核行不通过')
                    # self.preliminary_operation_review()

    def preliminary_operation_review(self):
        try:
            # 查询运营初审列表
            face_url = url['运营初审'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            orderId = response['result']['items'][0]['orderId']
            riskApprovalId = response['result']['items'][0]['riskApprovalId']

            # 办理运营初审接收,需要获取列表单号对应orderId、riskApprovalId
            data1 = {"orderId": orderId, "riskApprovalId": riskApprovalId, "companyId": self.companyId}
            data1 = json.dumps(data1)
            response1 = self.html.post(url['运营初审'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------运营初审接收')

            # 办理运营初审审查,需要获取列表单号对应id、riskApprovalId、riskApprovalId
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            id = response['result']['items'][0]['id']

            data2 = {"approvalState": "PASS", "normalType": "NORMAL", "rejectType": "", "addFileExtendIds": "",
                     "addFileIds": "", "addFileNames": "", "acceptCondition": "",
                     "addFileRemark": "", "createOperatorId": "0f15e23f-e317-414a-a990-c7cd31d073c9",
                     "createTime": 1589167393000, "examineTime": null,
                     "examinerId": "0f15e23f-e317-414a-a990-c7cd31d073c9", "examinerName": "", "id": id,
                     "isAddFile": "NO", "isBankCheck": "YES",
                     "isFaceCheck": "YES", "isUsePlatform": null, "orderId": orderId,
                     "orgId": "2dbb1bc7-8f87-431b-b64b-7fb9850233aa", "receiveTime": 1589167393000,
                     "refType": "", "rejectReason": "", "riskApprovalId": riskApprovalId,
                     "riskFundInfoModelList": [{"contractNumbers": 1, "createOperatorId": "",
                                                "createTime": null, "fundOrgAbbr": "工行", "fundOrgName": "工行", "id": "",
                                                "isSelect": "NO", "updateOperatorId": "", "updateTime": null}],
                     "status": "ENABLED", "unusualExplain": "",
                     "unusualReason": "", "updateOperatorId": "0f15e23f-e317-414a-a990-c7cd31d073c9",
                     "updateTime": 1589167393000, "approvalType": "NORMAL", "addFileExtendNameList": [""],
                     "fundIds": ""}
            data2 = json.dumps(data2)
            response2 = self.html.post(url['运营初审'][2], data2, headers={'Content-Type': 'application/json'})
            print(response2.text, '----------------运营初审审查')
            return response2.text, '----------------运营初审审查'
            # self.risk_review()
        except:
            return print("运营初审不通过")

    # 风控初审
    def risk_review(self):
        try:
            # 查询风控初审列表
            face_url = url['风控初审'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            orderId = response['result']['items'][0]['orderId']
            riskApprovalId = response['result']['items'][0]['riskApprovalId']
            #
            # # 办理风控初审接收,需要获取列表单号对应orderId、riskApprovalId
            data1 = {"orderId": orderId, "riskApprovalId": riskApprovalId, "companyId": self.companyId}
            data1 = json.dumps(data1)
            response1 = self.html.post(url['风控初审'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '---------风控初审接收')

            # 办理风控初审审查,需要获取列表单号对应riskApprovalId、riskApprovalId
            response = self.html.get(face_url).text
            response = eval(response)
            id = response['result']['items'][0]['id']
            selectApprovalInfoById_url=url['风控初审'][2]+id
            selectFundInfo_url=url['风控初审'][3]+'riskApprovalId='+riskApprovalId+'&orderId='+orderId+'&id='+id
            response1 = self.html.get(selectApprovalInfoById_url).text
            response1 = eval(response1)
            response2 = self.html.get(selectFundInfo_url).text
            response2 = eval(response2)

            fundIds = response2['result']['fundIds']
            addFileRemark = response1['result']['addFileRemark']
            allocationAssureMoney = response1['result']['allocationAssureMoney']
            buyAllowRemark = response1['result']['buyAllowRemark']
            channelAssureMoney = response1['result']['channelAssureMoney']
            channelMargin = response1['result']['channelMargin']
            companyId = response1['result']['companyId']
            createOperatorId = response1['result']['createOperatorId']
            creditSituation = response1['result']['creditSituation']
            creditSituationRemark = response1['result']['creditSituationRemark']
            dealPriceCheckExplain = response1['result']['dealPriceCheckExplain']
            dealPriceCheckState = response1['result']['dealPriceCheckState']
            debtRatio = response1['result']['debtRatio']
            depositMargin = response1['result']['depositMargin']
            estateValue = response1['result']['estateValue']
            examinerId = response1['result']['examinerId']
            examinerName = response1['result']['examinerName']
            guarantorSituationRemark = response1['result']['guarantorSituationRemark']
            id = response1['result']['id']
            isAddFile = response1['result']['isAddFile']
            isAllocation = response1['result']['isAllocation']
            isBuyAllow = response1['result']['isBuyAllow']
            isGuarantorSituation = response1['result']['isGuarantorSituation']
            isOwnerCivilDisputes = response1['result']['isOwnerCivilDisputes']
            isOwnerLawsuit = response1['result']['isOwnerLawsuit']
            isUseChannel = response1['result']['isUseChannel']
            oldLoanSituation = response1['result']['oldLoanSituation']
            orderId = response1['result']['orderId']
            orgId = response1['result']['orgId']
            ownerCivilDisputesRemark = response1['result']['ownerCivilDisputesRemark']
            ownerLawsuitRemark = response1['result']['ownerLawsuitRemark']
            redeemHouseAmount = response1['result']['redeemHouseAmount']
            redemptionRatio = response1['result']['redemptionRatio']
            refType = response1['result']['refType']
            returnSource = response1['result']['returnSource']
            riskApprovalId = response1['result']['riskApprovalId']
            status = response1['result']['status']
            transactionPrice = response1['result']['transactionPrice']
            updateOperatorId = response1['result']['updateOperatorId']

            data2 = {"approvalType": "NORMAL", "fundIds": fundIds, "addFileRemark": addFileRemark, "allocationAssureMoney": allocationAssureMoney,
                     "approvalOpinions": "通过", "approveState": "PASS", "buyAllowRemark": buyAllowRemark,
                     "channelAssureMoney": channelAssureMoney, "channelMargin": channelMargin, "companyId": companyId,
                     "createOperatorId": createOperatorId,
                     "createTime": self.stampDate, "creditSituation": creditSituation, "creditSituationRemark": creditSituationRemark,
                     "dealPriceCheckExplain": dealPriceCheckExplain, "dealPriceCheckState": dealPriceCheckState, "debtRatio": debtRatio, "depositMargin": depositMargin,
                     "estateValue": estateValue, "examineTime": self.stampDate,
                     "examinerId": examinerId, "examinerName": examinerName,
                     "guarantorSituationRemark": guarantorSituationRemark,
                     "id": id, "isAddFile": isAddFile, "isAllocation": isAllocation, "isBuyAllow": isBuyAllow, "isGuarantorSituation": isGuarantorSituation,
                     "isOwnerCivilDisputes": isOwnerCivilDisputes, "isOwnerLawsuit": isOwnerLawsuit,
                     "isUseChannel": isUseChannel, "normalType": "NORMAL", "oldLoanSituation": oldLoanSituation, "orderId": orderId,
                     "orgId": orgId,
                     "ownerCivilDisputesRemark": ownerCivilDisputesRemark, "ownerLawsuitRemark": ownerLawsuitRemark, "receiveTime": self.stampDate,
                     "redeemHouseAmount": redeemHouseAmount, "redemptionRatio": redemptionRatio, "refType": refType, "returnSource": returnSource,
                     "riskApprovalId": riskApprovalId, "status": status, "transactionPrice": transactionPrice,
                     "transactionType": self.transactionType,
                     "updateOperatorId": updateOperatorId, "updateTime": self.stampDate,
                     "addFileExtendNameList": [""], "isRejectToStartNode": "NO"}
            data2 = json.dumps(data2,ensure_ascii=False)
            response3 = self.html.post(url['风控初审'][4], data2.encode(), headers={'Content-Type': 'application/json'})
            print(response3.text, '----------------风控初审')
            return response3.text, '----------------风控初审'
            # self.risk_recheck()
        except:
            return print("风控初审不通过")

    # 风控复审
    def risk_recheck(self):
        try:
            #风控复审办理
            t = task_approval(head_url='http://189i0341c8.iok.la:27031', odd_num=self.odd_num,node_name='风控复审')
            t.platform_task()
            time.sleep(1)
            # self.charge()
        except Exception as e:
            return print(e.args, '风控复审审查失败')

    # 收费
    def charge(self):
        try:
            # 查询财务收费列表
            face_url = url['收费'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            planTotalFee = response['result']['items'][0]['planTotalFee']
            feeGeneralId = response['result']['items'][0]['feeGeneralId']

            # 收费办理
            data1 = {"currentCollectFeeMoney": planTotalFee, "chargeDate": self.chargeDate,
                     "companyAccountBank": "中国建设银行", "companyAccountId": "27522659-6ba6-47ba-a7bd-c69dfd379c98",
                     "companyAccountName": "张三", "companyAccountNumber": "65200001", "fundFnFeeGeneralId": feeGeneralId}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['收费'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------贷前收费')
            return response1.text, '----------------贷前收费'
            # self.collection_requirements()
        except:
            return print('收费失败')

    # 收要件
    def collection_requirements(self):
        try:
            # 查询收要件列表
            face_url = url['收要件'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            id = response['result']['items'][0]['id']

            # 收取要件
            data1 = {"essentialsType": ["REDEEM"], "fnEssentialsTakeRecordList": [
                {"essentialsAssort": "PERSON", "essentialsContent": ["ID_CARD", "OTHER"], "essentialsId": id,
                 "essentialsTakeAccountList": [
                     {"accountBank": "开户行1", "accountName": "账户名1", "accountNumber": "123456453135", "id": null,
                      "isEbank": "NO"}], "essentialsType": "REDEEM"
                    , "id": null, "remark": "备注1", "takeDate": self.takeDate}], "id": id, "isNeed": "YES"}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['收要件'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '收取要件成功')

            # 确认收齐
            data2 = {"id": id}
            data2 = json.dumps(data2)
            response2 = self.html.post(url['收要件'][2], data2, headers={'Content-Type': 'application/json'})
            print(response2.text, '----------------确认收齐')
            return response2.text, '----------------收要件'
            # self.insertRiskExecutionRemarks()
        except:
            return print('收取要件失败')

    # 执行岗备注
    def insertRiskExecutionRemarks(self):
        try:
            # 查询执行岗备注列表
            face_url = url['执行岗备注'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            id = response['result']['items'][0]['id']
            orderId = response['result']['items'][0]['orderId']
            riskApprovalId = response['result']['items'][0]['riskApprovalId']

            # 执行岗备注办理
            data1 = {"companyId": self.companyId, "id": id, "informationSituation": "COMPLETE"
                , "orderId": orderId, "riskApprovalId": riskApprovalId,
                     "riskExecutionRemarksFileFormList": [], "approvalOpinions": "执行岗备注通过"}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['执行岗备注'][1], data1, headers={'Content-Type': 'application/json'})
            print('执行岗备注成功')
            return response1.text,'----------------执行岗备注成功'
            # if self.fundType == 'CASH':
            #     self.updateArrivalAccountStatus()
            # else:
            #     self.queryRiskGuaranteeMainPage()
        except:
            return print('执行岗备注失败')

    # 保函寄送
    def queryRiskGuaranteeMainPage(self):
        try:
            # 查询收要件列表
            face_url = url['保函寄送'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            guaranteeMainId = response['result']['items'][0]['id']
            orderId = response['result']['items'][0]['orderId']
            fundIds = response['result']['items'][0]['fundIds']

            # 保函寄送办理
            data1 = {"guaranteeMainId": guaranteeMainId, "sendTime": self.takeDate, "addressee": "",
                     "addresseeType": "BANK"
                , "fundId": fundIds, "sendType": "EXPRESS", "remark": "备注1"}
            data1 = json.dumps(data1)
            response1 = self.html.post(url['保函寄送'][1], data1, headers={'Content-Type': 'application/json'})
            print('保函寄送成功')
            return response1.text,'----------------保函寄送成功'
            # self.updateArrivalAccountStatus()
        except:
            return print('保函寄送失败')

    # 资金到账
    def updateArrivalAccountStatus(self):
        try:
            if self.fundType == 'CASH':
                # 资金安排
                def financial_arrangement():
                    time.sleep(1)
                    face_url = url['资金到账']['资金安排'][0].replace('E2005110012', self.odd_num)
                    null = ''
                    true = ''
                    false = ''
                    response = self.html.get(face_url).text
                    response = eval(response)
                    id = response['result']['items'][0]['id']
                    applyMoney = response['result']['items'][0]['loanMoney']

                    face_url1 = url['资金到账']['资金安排'][1] + id
                    response1 = self.html.get(face_url1).text
                    response1 = eval(response1)
                    fundApplyRecordId = response1['result']['fundOrgList'][0]['fundApplyRecordId']
                    fundOrgId = response1['result']['fundOrgList'][0]['fundOrgId']

                    data = {"id": id, "remark": "无", "fundOrgList": [{"applyDays": 1, "applyMoney": applyMoney,
                                                                      "fundApplyRecordId": fundApplyRecordId,
                                                                      "fundOrgId": fundOrgId}]}

                    data = json.dumps(data, ensure_ascii=False)
                    response1 = self.html.post(url['资金到账']['资金安排'][2], data.encode(),
                                               headers={'Content-Type': 'application/json'})

                    if '实时可用额度不足' in eval(response1.text)['message']:
                        a = add_quota(fundOrgId=fundOrgId)
                        a.add_insertFundPackage()
                        response1 = self.html.post(url['资金到账']['资金安排'][2], data.encode(),
                                               headers={'Content-Type': 'application/json'})


                    # 资金选择工行需审批
                    response = self.html.get(face_url).text
                    response = eval(response)
                    if response['result']['items']==[]:
                        pass
                    else:
                        #办理审批
                        t = task_approval(head_url='http://189i0341c8.iok.la:27031', odd_num=self.odd_num,node_name='资金安排')
                        t.platform_task()
                        print(response1.text, '资金安排成功')

                #资金安排方法调用
                financial_arrangement()
                # 资料推送
                time.sleep(1)
                face_url2 = url['资金到账']['资料推送'][0].replace('E2005110012', self.odd_num)
                null = ''
                true = ''
                false = ''
                response2 = self.html.get(face_url2).text
                response2 = eval(response2)
                id = response2['result']['items'][0]['fundApplyRecordId']
                orderId = response2['result']['items'][0]['orderId']

                face_url3 = url['资金到账']['资料推送'][1] + orderId
                response3 = self.html.get(face_url3).text
                response3 = eval(response3)
                payeeAccountBank = response3['result'][0]['accountBank']
                payeeAccountName = response3['result'][0]['accountName']
                payeeAccountNumber = response3['result'][0]['accountNumber']

                data2 = {"id": id, "payeeAccountBank": payeeAccountBank, "payeeAccountName": payeeAccountName,
                         "payeeAccountNumber": payeeAccountNumber, "remark": ""}

                data2 = json.dumps(data2, ensure_ascii=False)
                response2 = self.html.post(url['资金到账']['资料推送'][2], data2.encode(),
                                           headers={'Content-Type': 'application/json'})
                print(response2.text, '资金推送成功')

            else:
                pass

            # 查询资金到账列表
            face_url = url['资金到账']['到账管理'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            fundApplyRecordId = response['result']['items'][0]['fundApplyRecordId']
            orderId = response['result']['items'][0]['orderId']
            loanMoney = response['result']['items'][0]['loanMoney']

            # 到账办理
            data1 = {"sourceAccountName": "丽丽", "sourceAccountNumber": "130000000000", "sourceAccountBank": "高新园分行",
                     "payeeAccountName": "碧桂园",
                     "payeeAccountNumber": "6226682121007773322", "payeeAccountBank": "南阳商业银行南阳商业银行",
                     "arrivalAccountMoney": loanMoney,
                     "isBankEnterpriseAccount": "NO", "payeeAccountId": "82eb9f57-89fd-48f7-90a5-ce22bfd9c43c",
                     "orderId": orderId,
                     "id": fundApplyRecordId, "arrivalAccountDate": self.takeDate, "arrivalRemark": ""}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['资金到账']['到账管理'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------资金到账成功')
            return response1.text, '----------------资金到账成功'
            # self.updateCheckDocAndLawsuit()
        except Exception as e:
            return print(e.args, '资金到账失败')

    # 查档查诉讼
    def updateCheckDocAndLawsuit(self):
        try:
            # 查询查档查诉讼列表
            face_url = url['查档查诉讼'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            checkDocLawsuitId = response['result']['items'][0]['checkDocLawsuitId']
            orderId = response['result']['items'][0]['orderId']

            face_url1 = url['查档查诉讼'][1] + checkDocLawsuitId
            response1 = self.html.get(face_url1).text
            response1 = eval(response1)
            riskCheckLawSuitId = response1['result']['lawsuitModelList'][0]['riskCheckLawSuitId']
            id = response1['result']['id']

            # 查档查诉讼办理
            data1 = {"approvalOpinions": "通过", "approvalState": "PASS", "checkDocLawsuitId": checkDocLawsuitId,
                     "id": id, "lawsuitFormList": [{"cardId": "110101199003070732",
                                                    "cardType": "P01", "createOperatorId": "", "createTime": null,
                                                    "id": "", "identityType": "SELLER",
                                                    "lawsuitState": "DISABLE", "name": "业主1", "orderId": "",
                                                    "remark": "", "riskApprovalId": "",
                                                    "riskCheckLawSuitId": riskCheckLawSuitId, "updateOperatorId": "",
                                                    "updateTime": null}], "orderId": orderId}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['查档查诉讼'][2], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------查档查诉讼成功')
            return response1.text,'----------------查档查诉讼成功'
            # self.deposit_collection()
        except:
            return print('查档查诉讼失败')

    # 收取保证金
    def deposit_collection(self):
        try:
            # 查询出款列表
            face_url = url['收取保证金'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            totalPlanAssureMoney = response['result']['items'][0]['totalPlanAssureMoney']
            orderId = response['result']['items'][0]['orderId']

            # 收取保证金办理
            data1 = {"takeMoney": totalPlanAssureMoney, "takeDate": self.chargeDate, "accountBank": "中国建设银行",
                     "accountId": "27522659-6ba6-47ba-a7bd-c69dfd379c98",
                     "accountName": "张三", "accountNumber": "65200001", "orderId": orderId, "remark": "备注1"}

            data1 = json.dumps(data1)
            response1 = self.html.post(url['收取保证金'][1], data1, headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------收取保证金成功')
            return response1.text, '----------------收取保证金成功'
            # self.disbursement_application()
        except:
            return print('收取保证金失败')

    # 出款申请
    def disbursement_application(self):
        try:
            # 查询赎楼列表
            face_url = url['出款申请'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            billingDetailsId = response['result']['items'][0]['billingDetailsId']
            arrivalAccountMoney = response['result']['items'][0]['arrivalAccountMoney']
            orderId = response['result']['items'][0]['orderId']

            face_url1 = url['出款申请'][1] + orderId
            response1 = self.html.get(face_url1).text
            response1 = eval(response1)

            # 循环发起申请
            for i in range(len(response1['result'])):
                response1 = self.html.get(face_url1).text
                response1 = eval(response1)

                # 根据金额判断能否发起申请
                if response1['result'][i]['notBillingOutMoney'] == 0:
                    continue
                else:
                    loanDetailsId = response1['result'][i]['id']
                    notBillingOutMoney = response1['result'][i]['notBillingOutMoney']

                    # 出款申请办理
                    data1 = {"billingDetailsId": billingDetailsId,
                             "billingAccountList": [{"billingMoney": notBillingOutMoney,
                                                     "payeeAccountBank": "收款开户行1", "payeeAccountName": "收款账户1",
                                                     "payeeAccountNumber": "13135435435", "payeeAccountType": "ELSE"}],
                             "billingTotalMoney": notBillingOutMoney, "loanDetailsId": loanDetailsId,
                             "orderId": orderId, "orgId": "2dbb1bc7-8f87-431b-b64b-7fb9850233aa", "remark": "备注1"}

                    data1 = json.dumps(data1, ensure_ascii=False)
                    response1 = self.html.post(url['出款申请'][2], data1.encode(),
                                               headers={'Content-Type': 'application/json'})
                    print(response1.text, '----------------出款申请成功')

            return '----------------出款申请成功'
            # self.auditBilling()
        except Exception as e:
            return print(e.args, '出款申请失败')

    # 出款审批
    def auditBilling(self):
        try:
            # 查询出款审批列表
            face_url = url['出款审批'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            billingDetailsId = response['result']['items'][0]['billingDetailsId']
            face_url1 = url['出款审批'][1] + billingDetailsId
            response1 = self.html.get(face_url1).text
            response1 = eval(response1)

            sourceAccountBank = response1['result']['bankList'][0]['accountBank']
            sourceAccountName = response1['result']['bankList'][0]['accountName']
            sourceAccountNumber = response1['result']['bankList'][0]['accountNumber']
            isBankEnterpriseAccount = response1['result']['bankList'][0]['isBankEnterpriseAccount']
            totalBillingMoney = response1['result']['totalBillingMoney']
            orderId = response1['result']['orderId']

            # 循环获取对应出款的所需字段
            billingAccountList = []
            for i in range(len(response1['result']['billingAccountList'])):
                id = response1['result']['billingAccountList'][i]['id']
                billingMoney = response1['result']['billingAccountList'][i]['billingMoney']
                billingRecordId = response1['result']['billingAccountList'][i]['billingRecordId']
                payeeAccountBank = response1['result']['billingAccountList'][i]['payeeAccountBank']
                payeeAccountName = response1['result']['billingAccountList'][i]['payeeAccountName']
                payeeAccountNumber = response1['result']['billingAccountList'][i]['payeeAccountNumber']

                billingAccountList_add = {"id": id, "billingMoney": billingMoney, "billingRecordId": billingRecordId,
                                          "showBank": payeeAccountBank, "payeeAccountBank": payeeAccountBank,
                                          "payeeAccountBankNum": "", "payeeAccountName": payeeAccountName,
                                          "payeeAccountNumber": payeeAccountNumber,
                                          "payeeAccountType": "ELSE", "payeeType": 1,
                                          "sourceAccountBank": sourceAccountBank,
                                          "sourceAccountName": sourceAccountName,
                                          "sourceAccountNumber": sourceAccountNumber,
                                          "isBankEnterpriseAccount": isBankEnterpriseAccount}
                billingAccountList.append(billingAccountList_add)

            # 出款审批办理
            data1 = {"billingAccountList": billingAccountList, "billingDetailsId": billingDetailsId,
                     "billingTotalMoney": totalBillingMoney, "orderId": orderId,
                     "orgId": "2dbb1bc7-8f87-431b-b64b-7fb9850233aa", "remark": ""}

            data1 = json.dumps(data1, ensure_ascii=False)

            response1 = self.html.post(url['出款审批'][2], data1.encode(), headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------出款审批成功')
            return response1.text, '----------------出款审批成功'
            # self.process_approval()
        except Exception as e:
            return print(e.args, '出款审批失败')

    # 流程审批
    def process_approval(self):
        try:
            t = task_approval(head_url='http://189i0341c8.iok.la:27031', odd_num=self.odd_num,node_name='出款流程')
            t.platform_task()
        except Exception as e:
            return print(e.args,'流程审批失败')

    # 出款、复核
    def payment(self):
        # try:
        # 查询出款列表
        face_url = url['出款'][0].replace('E2005110012', self.odd_num)
        null = ''
        true = ''
        response = self.html.get(face_url).text
        response = eval(response)
        # 取值字段
        billingDetailsId = response['result']['items'][0]['billingDetailsId']
        billingTotalMoney = response['result']['items'][0]['loanMoney']

        # 出款、复核办理
        data1 = {"billingDetailsId":billingDetailsId,"billingDate":self.takeDate,"billingTotalMoney":billingTotalMoney}
        data1 = json.dumps(data1, ensure_ascii=False)
        response1 = self.html.post(url['出款'][1], data1.encode(), headers={'Content-Type': 'application/json'})
        print(response1.text, '-------------出款')
        return response1.text, '-------------出款'

        #复核操作
        # data2 = {"billingDetailsId": billingDetailsId, "billingDate": self.takeDate,
        #          "billingTotalMoney": billingTotalMoney}
        # data2 = json.dumps(data2, ensure_ascii=False)
        # response2 = self.html.post(url['出款'][2], data2.encode(), headers={'Content-Type': 'application/json'})
        # print(response2.text, '-------------复核')
        # self.foreclosure_building()
        # except:
        #     return print('出款、复核失败')

    # 赎楼
    def foreclosure_building(self):
        try:
            # 查询赎楼列表
            face_url = url['赎楼'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            orderId = response['result']['items'][0]['orderId']

            for i in range(len(response['result']['items'][0]['billingRecordList'])):
                if response['result']['items'][0]['billingRecordList'][i]['isRedeem'] == 'YES':
                    continue
                else:
                    billingMoney = response['result']['items'][0]['billingRecordList'][i]['billingMoney']
                    billingRecordId = response['result']['items'][0]['billingRecordList'][i]['id']

                    # 赎楼办理
                    data1 = {"billingMoney": billingMoney, "billingRecordId": billingRecordId, "orderId": orderId,
                             "fileIdList": [], "interest": 0, "penaltyInterest": 0, "personReplenishment": 0,
                             "realRepayAmount": billingMoney, "redeemBalance": 0, "redeemDate": self.takeDate,
                             "redeemTotalAmount": billingMoney, "remark": ""}

                    data1 = json.dumps(data1, ensure_ascii=False)
                    response1 = self.html.post(url['赎楼'][1], data1.encode(),
                                               headers={'Content-Type': 'application/json'})
                    print(response1.text, '----------------赎楼成功')

            return '----------------赎楼成功'
                    # self.insertFnCertTake()
        except:
            return print('赎楼失败')

    # 取原证
    def insertFnCertTake(self):
        try:
            # 查询取原证列表
            face_url = url['取原证'][0].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            # 取值字段
            orderId = response['result']['items'][0]['orderId']

            # 取原证办理
            data1 = {"efcertNumber": "0112571", "guaranteeId": "", "orderId": orderId, "fileIdList": [],
                     "takeCertDate": self.takeDate, "remark": ""}

            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(url['取原证'][1], data1.encode(), headers={'Content-Type': 'application/json'})
            print(response1.text, '----------------取原证成功')
            return response1.text, '----------------取原证成功'
        except Exception as e:
            return print(e.args,'取原证失败')

    # CERT_LOGOUT=注销、TRANSFER=过户、TAKE_NEW_CERT=取新证、MORTGAGE=抵押登记
    def cancellation(self, itemCode):
        # 注销
        if itemCode == 'CERT_LOGOUT':
            # 查询原证注销列表
            face_url = url['权证管理'][2].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            orderId = response['result']['items'][0]['id']
            riskHandleId = response['result']['items'][0]['riskHandleId']

            # 办理原证注销
            data1 = {"bizFinishTime": self.takeDate, "bizCode": "021134", "orderId": orderId,
                     "riskHandleId": riskHandleId, "id": "", "itemCode": itemCode, "fileList": []}
            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][3], data1.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------办理原证注销')
            return response1.text, '--------办理原证注销'
        # 过户
        elif itemCode == 'TRANSFER':
            # 查询过户列表
            face_url = url['权证管理'][4].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            orderId = response['result']['items'][0]['id']
            riskHandleId = response['result']['items'][0]['riskHandleId']

            # 办理过户
            data1 = {"bizFinishTime": self.chargeDate, "bizCode": "021134", "orderId": orderId,
                     "riskHandleId": riskHandleId, "id": "", "itemCode": itemCode, "fileList": []}
            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][5], data1.encode(), headers={'Content-Type': 'application/json'})
            print(response1.text, '--------办理过户')
            return response1.text, '--------办理过户'
        # 取新证
        elif itemCode == 'TAKE_NEW_CERT':
            # 查询取新证列表
            face_url = url['权证管理'][6].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            orderId = response['result']['items'][0]['id']
            riskHandleId = response['result']['items'][0]['riskHandleId']

            # 办理过户
            data1 = {"bizFinishTime": self.chargeDate, "bizCode": "021134", "orderId": orderId,
                     "riskHandleId": riskHandleId, "id": "", "itemCode": itemCode, "fileList": []}
            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][7], data1.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------办理取新证')
            return response1.text, '--------办理取新证'
        # 抵押登记
        elif itemCode == 'MORTGAGE':
            # 查询取新证列表
            face_url = url['权证管理'][8].replace('E2005110012', self.odd_num)
            null = ''
            true = ''
            response = self.html.get(face_url).text
            response = eval(response)
            orderId = response['result']['items'][0]['id']
            riskHandleId = response['result']['items'][0]['riskHandleId']

            # 办理过户
            data1 = {"bizFinishTime": self.chargeDate, "bizCode": "021134", "orderId": orderId,
                     "riskHandleId": riskHandleId, "id": "", "itemCode": itemCode, "fileList": []}
            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][9], data1.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------办理抵押登记')
            return response1.text, '--------办理抵押登记'

    # 发指令
    def give_orders(self):
        # 查询权证管理列表
        face_url = url['权证管理'][0].replace('E2005110012', self.odd_num)
        null = ''
        true = ''
        time.sleep(0.5)
        response = self.html.get(face_url).text
        response = eval(response)
        cancelStatus = response['result']['items'][0]['cancelStatus']
        transferNamesStatus = response['result']['items'][0]['transferNamesStatus']
        getNewLicnseStatus = response['result']['items'][0]['getNewLicnseStatus']
        mortgageRegistrationStatus = response['result']['items'][0]['mortgageRegistrationStatus']
        guaranteeId = response['result']['items'][0]['guaranteeId']

        # 注销发指令、
        if cancelStatus == 'WAIT_SEND':
            data = {"guaranteeId": guaranteeId, "orderApplyId": "001", "orderDate": self.chargeDate}
            data = json.dumps(data, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][1], data.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------原证注销发指令')
            return response1.text, '--------原证注销发指令'
        # 过户发指令
        elif transferNamesStatus == 'WAIT_SEND':
            data = {"guaranteeId": guaranteeId, "orderApplyId": "002", "orderDate": self.chargeDate}
            data = json.dumps(data, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][1], data.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------过户发指令')
            return response1.text, '--------过户发指令'
        # 取新证发指令
        elif getNewLicnseStatus == 'WAIT_SEND':
            data = {"guaranteeId": guaranteeId, "orderApplyId": "003", "orderDate": self.chargeDate}
            data = json.dumps(data, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][1], data.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------取新证发指令')
            return response1.text, '--------取新证发指令'
        # 抵押登记发指令
        elif mortgageRegistrationStatus == 'WAIT_SEND':
            data = {"guaranteeId": guaranteeId, "orderApplyId": "004", "orderDate": self.chargeDate}
            data = json.dumps(data, ensure_ascii=False)
            response1 = self.html.post(url['权证管理'][1], data.encode(),
                                       headers={'Content-Type': 'application/json'})
            print(response1.text, '--------抵押登记发指令')
            return response1.text, '--------抵押登记发指令'

    # 原证注销
    def cancellation_of_original_certificate(self):
        self.give_orders()
        self.cancellation('CERT_LOGOUT')

    # 过户
    def transfer(self):
        self.give_orders()
        self.cancellation('TRANSFER')

    # 取新证
    def take_new_evidence(self):
        self.give_orders()
        self.cancellation('TAKE_NEW_CERT')

    # 抵押登记
    def mortgage_registration(self):
        self.give_orders()
        self.cancellation('MORTGAGE')


#

# if __name__ == '__main__':
#     p = process(odd_num='X2007040001')
#     p.face_signature()
#     p.nuclear_row()
#     p.preliminary_operation_review()
#     p.risk_review()
#     p.risk_recheck()
    # time.sleep(1)
    # p.charge()
    # p.collection_requirements()
    # p.insertRiskExecutionRemarks()  # 执行岗备注
    # p.queryRiskGuaranteeMainPage()  # 保函寄送
    #
    # p.updateArrivalAccountStatus()  # 资金到账
    # p.updateCheckDocAndLawsuit()  # 查档查诉讼
    # p.deposit_collection()  # 收取保证金
    # p.disbursement_application()  # 出款申请
    # p.auditBilling()  # 出款审批
    # p.process_approval()  # 流程审批
    # p.payment()  # 出款、复核
    # p.foreclosure_building()  # 赎楼
    # p.insertFnCertTake()  # 取原证
    # p.cancellation_of_original_certificate()  # 原证注销
    # p.transfer()  # 过户
    # p.take_new_evidence()  # 取新证
    # p.mortgage_registration()  # 抵押登记
