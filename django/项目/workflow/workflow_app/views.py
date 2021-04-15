from django.shortcuts import render
import sys

sys.path.append('D:\python\Python\python\Python\working')
import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from workflow_pack.接口.流程.平台流程 import process
from django.http import HttpResponse,JsonResponse


pack_list = ['面签', '核行', '运营初审', '风控初审', '风控复审', '贷前收费', '收要件', '执行岗备注', '保函寄送', '资金到账', '查档查诉讼', '收取保证金', '出款申请',
             '出款审批', '流程审批', '出款、复核', '赎楼', '取原证', '原证注销', '过户', '取新证', '抵押登记']

def index(request):
    value=pack_list
    return render(request,"login.html",{'hello':value})

@csrf_exempt
def run(request):
    can_dict={}
    value = pack_list

    if request.POST:
        start=request.POST['start']
        end=request.POST['end']
        odd_num=request.POST['odd_num']
        can_dict['result']=[]
        p = process(odd_num)

        pack_dict = {
            '面签': p.face_signature,
            '核行': p.nuclear_row,
            '运营初审': p.preliminary_operation_review,
            '风控初审': p.risk_review,
            '风控复审': p.risk_recheck,
            '贷前收费': p.charge,
            '收要件': p.collection_requirements,
            '执行岗备注': p.insertRiskExecutionRemarks,
            '保函寄送': p.queryRiskGuaranteeMainPage,
            '资金到账': p.updateArrivalAccountStatus,
            '查档查诉讼': p.updateCheckDocAndLawsuit,
            '收取保证金': p.deposit_collection,
            '出款申请': p.disbursement_application,
            '出款审批': p.auditBilling,
            '流程审批': p.process_approval,
            '出款、复核': p.payment,
            '赎楼': p.foreclosure_building,
            '取原证': p.insertFnCertTake,
            '原证注销': p.cancellation_of_original_certificate,
            '过户': p.transfer,
            '取新证': p.take_new_evidence,
            '抵押登记': p.mortgage_registration,
        }

        for x,y in enumerate(pack_dict):
            if start==y:
                can_dict['start_index']=x

            elif end==y:
                can_dict['end_index']=x+1

        for node_name in list(pack_dict.keys())[can_dict['start_index']:can_dict['end_index']]:
            result=pack_dict[node_name]()
            can_dict['result'].append(result)

        return  render(request,"login.html",{'hello':value,'start':start,'end':end,'odd_num':odd_num,'result':can_dict['result']})

@csrf_exempt
def test_ajax(request):
    if request.method == 'POST':
        inp1 = request.POST.get('inp1')
        inp2 = request.POST.get('inp2')
        inp3 = int(inp1) + int(inp2)
        d = {'sum':inp3}

        #JsonResponse:传值类型为json类型
        return JsonResponse(d)
    return render(request,'test.html')
