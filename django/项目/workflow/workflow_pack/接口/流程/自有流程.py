import requests
import json
from 接口.公共.登录 import login
import datetime
# from 可调用文件.接口.数据库查询.数据库查询 import select

url = {'审查员审查': {'接收': ['/web-surety/security/business/examinerReview/pageQueryToBeExamine?keyword=',
                        '/web-surety/security/business/examinerReview/receive'],
                 '审查': ['/web-surety/security/business/examinerReview/pickExaminerReviewById?id=',
                        '/web-surety/security/business/examinerReview/approveExaminerReview']},
       '收费': ['/web-surety/security/business/finance/queryCharge?positionType=WARRANTY&keyWord=',
              '/web-surety/security/business/finance/tollSave'],
       '风控复审': {'风控经理': [
           '/web-surety/security/workflow/workflowapprove/queryTaskOfCurrentPerson?processName=P202005281417257657&finishPerson=aaa9aa4a-32d7-4fd5-ae61-ca4e66017f1b&positionId=6c0923db-044c-4675-a57e-15c3be698e18',
           '/web-surety/security/workflow/task/passTask'],
                '风控总监': ['', ''],
                '区域审查经理': ['', ''],
                '城市总经理': ['', '']},
       '寄保函':['/web-surety/security/business/complex/queryRedemptionEnsure?keyWord=','/web-surety/security/business/complex/redemptionEnsureSave']
       }


class Own_process:
    def __init__(self, odd_num):
        self.odd_num = odd_num
        self.html = login(username='13323594169')[0]
        self.html1 = login(username='13417664959')[0]
        self.url_adress = 'http://192.168.0.58:82'
        self.takeDate = str(datetime.date.today())

        entry_details_url = self.url_adress + '/web-surety/security/business/guarantee/guaranteePage?keyWord=' + self.odd_num
        null = ''
        true = 'true'
        response = self.html.get(entry_details_url).text
        response = eval(response)
        self.fundType = response['result']['items'][0]['fundType']
        self.transactionType = response['result']['items'][0]['transactionType']

    def examination(self):
        try:
            # 审查员审查列表内容
            message_url = self.url_adress + url['审查员审查']['接收'][0] + self.odd_num
            receive_url = self.url_adress + url['审查员审查']['接收'][1]
            null = ''
            true = 'true'
            response_text = self.html.get(message_url).text
            response_text = eval(response_text)
            id = response_text['result']['items'][0]['id']
            examinerReviewId = response_text['result']['items'][0]['examinerReviewId']

            # 办理审查员接收
            data = {"id": id}
            data = json.dumps(data)
            response = self.html.post(receive_url, data, headers={'Content-Type': 'application/json'})
            print(response.text, '审查员接收成功')
        except Exception as e:
            print(e.args, '审查员审查节点失败')

        else:
            # 审查弹窗内容
            message_url1 = self.url_adress + url['审查员审查']['审查'][0] + examinerReviewId
            examination_url = self.url_adress + url['审查员审查']['审查'][1]
            null = ''
            true = 'true'
            response_text1 = self.html.get(message_url1).text
            response_text1 = eval(response_text1)
            approvalReview = response_text1['result']['approvalReview']
            auctionPrice = response_text1['result']['auctionPrice']
            businessFormType = response_text1['result']['businessFormType']
            createOperatorId = response_text1['result']['createOperatorId']
            createTime = response_text1['result']['createTime']
            creditSituation = response_text1['result']['creditSituation']
            currentLoanAmount = response_text1['result']['currentLoanAmount']
            currentLoanDays = response_text1['result']['currentLoanDays']
            debtRatio = response_text1['result']['debtRatio']
            examinerId = response_text1['result']['examinerId']
            examinerName = response_text1['result']['examinerName']
            examinerPhone = response_text1['result']['examinerPhone']
            examinerTime = response_text1['result']['examinerTime']
            finalPriceInspect = response_text1['result']['finalPriceInspect']
            finalPriceInspectRemark = response_text1['result']['finalPriceInspectRemark']
            firstInstallment = response_text1['result']['firstInstallment']
            folkInquiry = response_text1['result']['folkInquiry']
            guaranteeId = response_text1['result']['guaranteeId']
            guaranteeSource = response_text1['result']['guaranteeSource']
            guarantorSituation = response_text1['result']['guarantorSituation']
            id = response_text1['result']['id']
            lawsuit = response_text1['result']['lawsuit']
            loanAmount = response_text1['result']['loanAmount']
            loanRatio = response_text1['result']['loanRatio']
            mergeLoanAmount = response_text1['result']['mergeLoanAmount']
            oldLoanSituation = response_text1['result']['oldLoanSituation']
            paidDeposit = response_text1['result']['paidDeposit']
            paymentRatio = response_text1['result']['paymentRatio']
            propertyValueDetermination = response_text1['result']['propertyValueDetermination']
            purchaseQualification = response_text1['result']['purchaseQualification']
            receiveTime = response_text1['result']['receiveTime']
            redeemHouseAmount = response_text1['result']['redeemHouseAmount']
            redemptionRatio = response_text1['result']['redemptionRatio']
            relateGuaranteeId = response_text1['result']['relateGuaranteeId']
            relateGuaranteeNumber = response_text1['result']['relateGuaranteeNumber']
            relatedLoanAmount = response_text1['result']['relatedLoanAmount']
            returnSource = response_text1['result']['returnSource']
            reviewBusinessType = response_text1['result']['reviewBusinessType']
            status = response_text1['result']['status']
            theCertificateBegins = response_text1['result']['theCertificateBegins']
            theCertificateEnds = response_text1['result']['theCertificateEnds']
            transactionPrice = response_text1['result']['transactionPrice']
            updateOperatorId = response_text1['result']['updateOperatorId']
            updateTime = response_text1['result']['updateTime']

            # 办理审查员审查
            data1 = {"acceptanceOfOpinions": "通过", "approvalReview": approvalReview, "auctionPrice": auctionPrice,
                     "businessFormType": businessFormType, "createOperatorId": createOperatorId,
                     "createTime": createTime,
                     "creditSituation": creditSituation, "currentLoanAmount": currentLoanAmount,
                     "currentLoanDays": currentLoanDays, "debtRatio": debtRatio,
                     "examinerId": examinerId, "examinerName": examinerName,
                     "examinerPhone": examinerPhone, "examinerTime": examinerTime,
                     "finalPriceInspect": finalPriceInspect,
                     "finalPriceInspectRemark": finalPriceInspectRemark, "firstInstallment": firstInstallment,
                     "folkInquiry": folkInquiry,
                     "guaranteeId": guaranteeId, "guaranteeSource": guaranteeSource,
                     "guarantorSituation": guarantorSituation, "id": id, "lawsuit": lawsuit,
                     "loanAmount": loanAmount, "loanRatio": loanRatio, "mergeLoanAmount": mergeLoanAmount,
                     "oldLoanSituation": oldLoanSituation, "paidDeposit": paidDeposit,
                     "paymentRatio": paymentRatio, "propertyValueDetermination": propertyValueDetermination,
                     "purchaseQualification": purchaseQualification,
                     "receiveTime": receiveTime, "redeemHouseAmount": redeemHouseAmount,
                     "redemptionRatio": redemptionRatio,
                     "relateGuaranteeId": relateGuaranteeId, "relateGuaranteeNumber": relateGuaranteeNumber,
                     "relatedLoanAmount": relatedLoanAmount,
                     "returnSource": returnSource, "reviewBusinessType": reviewBusinessType, "status": status,
                     "theCertificateBegins": theCertificateBegins, "theCertificateEnds": theCertificateEnds,
                     "transactionPrice": transactionPrice,
                     "updateOperatorId": updateOperatorId, "updateTime": updateTime, "fundType": self.fundType,
                     "transactionType": self.transactionType}

            data1 = json.dumps(data1, ensure_ascii=False)
            response1 = self.html.post(examination_url, data1.encode(), headers={'Content-Type': 'application/json'})
            print(response1.text, '审查员审查成功')

    def charge(self):
        try:
            #收费列表内容
            message_url = self.url_adress + url['收费'][0] + self.odd_num
            charge_url = self.url_adress + url['收费'][1]
            null = ''
            true = 'true'
            response_text = self.html.get(message_url).text
            response_text = eval(response_text)
            handlingFee = response_text['result']['items'][0]['charges']
            tollAmount = response_text['result']['items'][0]['planTotalCharges']
            payerId = response_text['result']['items'][0]['buyerModelList'][0]['id']
            payerName = response_text['result']['items'][0]['buyerModelList'][0]['cltName']
            guaranteeId = response_text['result']['items'][0]['id']

            # 办理收费
            data = {"payType": "BANK", "companyAccountName": "李兆旭", "handlingFee": handlingFee, "isInvoice": "NO",
                    "invoiceName": "", "tollAmount": tollAmount, "chargeDate": self.takeDate, "monthBankAccountId": "",
                    "monthBankName": "", "nameAll": "中国农业银行-李兆旭(6217902000000211244)",
                    "payerId": payerId, "payerName": payerName,
                    "companyAccountId": "8999CEC1F3131C97E055000000000001", "chargeType": "WARRANTY",
                    "guaranteeId": guaranteeId, "id": ""}
            data = json.dumps(data, ensure_ascii=False)
            response = self.html.post(charge_url, data.encode(), headers={'Content-Type': 'application/json'})
        except Exception as e:
            print(e.args, '收费失败')
        else:
            pass

    def risk_control_review(self):
        try:
            #风控复审列表内容
            serial_number = select().select_risk_serial_number(self.odd_num)
            message_url = self.url_adress + url['风控复审']['风控经理'][0] + serial_number
            examination_url=self.url_adress+url['风控复审']['风控经理'][1]
            null=''
            true='true'
            response_text = self.html1.get(message_url).text
            response_text=eval(response_text)
            taskId=response_text['result']['itemList'][0]['id']

            #办理风控经理审查
            data={"operatorId":"aaa9aa4a-32d7-4fd5-ae61-ca4e66017f1b","taskId":taskId,"remark":"通过"}
            data=json.dumps(data,ensure_ascii=False)
            response=self.html1.post(examination_url,data.encode(),headers={'Content-Type': 'application/json'})
            print(response.text,'风控经理审查成功')
        except Exception as e:
            print(e.args, '风控复审失败')
        else:
            pass


    def letter_of_guarantee(self):
        try:
            #寄保函列表内容
            message_url = self.url_adress + url['寄保函'][0] + self.odd_num
            letter_url = self.url_adress + url['寄保函'][1]
            null = ''
            true = 'true'
            response_text = self.html1.get(message_url).text
            response_text = eval(response_text)
            guaranteeId = response_text['result']['items'][0]['id']

            #办理寄保函
            data={"guaranteeId":guaranteeId,"positionType":"SEND","recipientName":"银行客户经理","sendDate":self.takeDate,"sendRemark":"保函已寄出"}
            data=json.dumps(data,ensure_ascii=False)
            response=self.html.post(letter_url,data.encode(),headers={'Content-Type': 'application/json'})
            print(response.text,'保函已寄送')

        except Exception as e:
            print(e.args,"寄保函失败")
        else:
            pass




if __name__ == '__main__':
    o = Own_process('E2005280005')  # X2005270035
    # o.examination()
    # o.charge()
    # o.risk_control_review()
    o.letter_of_guarantee()