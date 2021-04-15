# 资金银行增加额度

from workflow_pack.接口.公共.登录 import login
import requests
import json
from workflow_pack.接口.其他.时间转换 import local_to_time_stamp
import datetime


class add_quota:
    def __init__(self, head_url='http://192.168.0.58:82', fundOrgId='646157c7-28dc-4cd0-86b6-03c1e1147e8c',
                 username='17666121214'):
        self.head_url = head_url
        self.html = login(username=username)[0]
        self.mytime = str(datetime.date.today())
        self.fundOrgId = fundOrgId

        # 当前时间的时间戳
        self.locl_time_stamp = local_to_time_stamp()
        global null, true
        null = ''
        true = ''

    # 添加资金包
    def add_insertFundPackage(self):
        # 资金机构接口
        queryFundPackage_url = self.head_url + '/web-surety/security/fundInfo/selectById?id=' + self.fundOrgId
        insertFundPackage_url = self.head_url + '/web-surety/security/fundPackage/insertFundPackage'
        response = self.html.get(queryFundPackage_url).text
        response = eval(response)
        self.paidAssureMoney = response['result']['enabledPackageList'][0]['paidAssureMoney']

        # 添加资金包
        data = {"assureRate": "1", "enableLimit": "1000000000", "endTime": self.mytime,
                "fundOrgId": self.fundOrgId, "id": "", "packageName": "1",
                "paidAssureMoney": self.paidAssureMoney, "startTime": self.mytime}
        data = json.dumps(data, ensure_ascii=False)
        response1 = self.html.post(insertFundPackage_url, data.encode(), headers={'Content-Type': 'application/json'})
        print(response1.text, '--------添加资金包')

        # 添加资金包后保存
        self.save()

    def save(self):
        # 资金机构接口
        queryFundPackage_url = self.head_url + '/web-surety/security/fundInfo/selectById?id=' + self.fundOrgId
        saveFundInfo_url = self.head_url + '/web-surety/security/fundInfo/saveFundInfo'
        response = self.html.get(queryFundPackage_url).text
        response = eval(response)
        self.paidAssureMoney = response['result']['enabledPackageList'][0]['paidAssureMoney']
        self.channelCodeFormula = response['result']['fundRateFormulaModel']['channelCodeFormula']
        self.channelFeeRate = response['result']['fundRateFormulaModel']['channelFeeRate']
        self.channelFormula = response['result']['fundRateFormulaModel']['channelFormula']
        self.createOperatorId = response['result']['fundRateFormulaModel']['createOperatorId']
        self.createTime = response['result']['fundRateFormulaModel']['createTime']
        self.fundBusinessRate = response['result']['fundRateFormulaModel']['fundBusinessRate']
        self.fundorgId = response['result']['fundRateFormulaModel']['fundOrgId']
        self.hasChannelFee = response['result']['fundRateFormulaModel']['hasChannelFee']
        self.hasInterest = response['result']['fundRateFormulaModel']['hasInterest']
        self.hasPremiumFee = response['result']['fundRateFormulaModel']['hasPremiumFee']
        self.hasServiceFee = response['result']['fundRateFormulaModel']['hasServiceFee']
        self.hasStampTax = response['result']['fundRateFormulaModel']['hasStampTax']
        self.id = response['result']['fundRateFormulaModel']['id']
        self.interestCodeFormula = response['result']['fundRateFormulaModel']['interestCodeFormula']
        self.interestFormula = response['result']['fundRateFormulaModel']['interestFormula']
        self.premiumCodeFormula = response['result']['fundRateFormulaModel']['premiumCodeFormula']
        self.premiumFormula = response['result']['fundRateFormulaModel']['premiumFormula']
        self.serviceCodeFormula = response['result']['fundRateFormulaModel']['serviceCodeFormula']
        self.serviceFeeRate = response['result']['fundRateFormulaModel']['serviceFeeRate']
        self.serviceFormula = response['result']['fundRateFormulaModel']['serviceFormula']
        self.stampCodeFormula = response['result']['fundRateFormulaModel']['stampCodeFormula']
        self.stampFormula = response['result']['fundRateFormulaModel']['stampFormula']
        self.stampTaxRate = response['result']['fundRateFormulaModel']['stampTaxRate']
        self.updateOperatorId = response['result']['fundRateFormulaModel']['updateOperatorId']
        self.fundOrgAbbr = response['result']['fundOrgAbbr']
        self.fundOrgName = response['result']['fundOrgName']
        self.fundCode = response['result']['fundCode']
        #授信额度
        self.creditLimit = 9920100000
        self.cashSourceId = response['result']['cashSourceId']
        self.isSendGuarantee = response['result']['isSendGuarantee']
        self.minAssureMoney = response['result']['minAssureMoney']
        self.singleUpperLimit = response['result']['singleUpperLimit']
        self.clintSingleUpperLimit = response['result']['clintSingleUpperLimit']
        self.businessLimitDays = response['result']['businessLimitDays']
        self.supportBusiness = response['result']['supportBusiness']
        self.fundMainSupport = response['result']['fundMainSupport']
        self.fundPackageMargins = response['result']['fundPackageMargins']
        self.settlingDays = response['result']['settlingDays']
        self.remark = response['result']['remark']
        self.payAccountBankName = response['result']['fundPaymentAccountModel']['payAccountBankName']
        self.payAccountName = response['result']['fundPaymentAccountModel']['payAccountName']
        self.payAccountNum = response['result']['fundPaymentAccountModel']['payAccountNum']
        self.payeeAccountBankName = response['result']['payeeAccountBankName']
        self.payeeAccountName = response['result']['payeeAccountName']
        self.payeeAccountNum = response['result']['payeeAccountNum']
        self.payeeAccountId = response['result']['payeeAccountId']
        self.cityCodes = response['result']['cityCodes']
        self.packageIds = ''
        for i in response['result']['enabledPackageList']:
            self.packageIds=self.packageIds+','+i['id']
            if self.packageIds[0]==',':
                self.packageIds=self.packageIds[1:]

        print(self.packageIds)
        self.productIds = response['result']['productIds']

        # 资金机构接口
        data = {"id": self.fundOrgId,
                "fundRateFormulaSaveForm": {"channelCodeFormula": self.channelCodeFormula,
                                            "channelFeeRate": self.channelFeeRate,
                                            "channelFormula": self.channelFormula,
                                            "createOperatorId": self.createOperatorId, "createTime": self.createTime,
                                            "fundBusinessRate": self.fundBusinessRate,
                                            "fundOrgId": self.fundorgId, "hasChannelFee": self.hasChannelFee,
                                            "hasInterest": self.hasInterest, "hasPremiumFee": self.hasPremiumFee,
                                            "hasServiceFee": self.hasServiceFee,
                                            "hasStampTax": self.hasStampTax, "id": self.id,
                                            "interestCodeFormula": self.interestCodeFormula,
                                            "interestFormula": self.interestFormula,
                                            "premiumCodeFormula": self.premiumCodeFormula,
                                            "premiumFormula": self.premiumFormula,
                                            "serviceCodeFormula": self.serviceCodeFormula,
                                            "serviceFeeRate": self.serviceFeeRate,
                                            "serviceFormula": self.serviceFormula,
                                            "stampCodeFormula": self.stampCodeFormula,
                                            "stampFormula": self.stampFormula,
                                            "stampTaxRate": self.stampTaxRate,
                                            "updateOperatorId": self.updateOperatorId,
                                            "updateTime": self.locl_time_stamp}, "fundOrgAbbr": self.fundOrgAbbr,
                "fundOrgName": self.fundOrgName, "fundCode": self.fundCode, "creditLimit": self.creditLimit,
                "cashSourceId": self.cashSourceId, "isSendGuarantee": self.isSendGuarantee,
                "minAssureMoney": self.minAssureMoney, "singleUpperLimit": self.singleUpperLimit,
                "clintSingleUpperLimit": self.clintSingleUpperLimit,
                "businessLimitDays": self.businessLimitDays, "supportBusiness": self.supportBusiness,
                "fundMainSupport": self.fundMainSupport,
                "fundPackageMargins": self.fundPackageMargins, "settlingDays": self.settlingDays, "remark": self.remark,
                "hasPremium": "YES",
                "feeRateList": [],
                "fundPaymentAccountSaveForm": {"payAccountBankName": self.payAccountBankName,
                                               "payAccountName": self.payAccountName,
                                               "payAccountNum": self.payAccountNum},
                "payeeAccountBankName": self.payeeAccountBankName, "payeeAccountName": self.payeeAccountName,
                "payeeAccountNum": self.payeeAccountNum, "payeeAccountId": self.payeeAccountId,
                "packageIds": self.packageIds,
                "productIds": self.productIds,
                "cityCodes": self.cityCodes, "operateType": "EDIT"}

        data = json.dumps(data, ensure_ascii=False)

        response1 = self.html.post(saveFundInfo_url, data.encode(), headers={'Content-Type': 'application/json'})
        print(response1.text, '--------保存修改')


if __name__ == '__main__':
    a = add_quota()
    a.add_insertFundPackage()
