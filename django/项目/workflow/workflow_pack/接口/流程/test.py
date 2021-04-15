
pack_dict={
    '面签':p.face_signature,
    '核行':p.nuclear_row,
    '运营初审':p.preliminary_operation_review,
    '风控初审':p.risk_review,
    '风控复审':p.risk_recheck,
    '贷前收费':p.charge,
    '收要件':p.collection_requirements,
    '执行岗备注':p.insertRiskExecutionRemarks,
    '保函寄送':p.queryRiskGuaranteeMainPage,
    '资金到账':p.updateArrivalAccountStatus,
    '查档查诉讼':p.updateCheckDocAndLawsuit,
    '收取保证金':p.deposit_collection,
    '出款申请':p.disbursement_application,
    '出款审批':p.auditBilling,
    '流程审批':p.process_approval,
    '出款、复核':p.payment,
    '赎楼':p.foreclosure_building,
    '取原证':p.insertFnCertTake,
    '原证注销':p.cancellation_of_original_certificate,
    '过户':p.transfer,
    '取新证':p.take_new_evidence,
    '抵押登记':p.mortgage_registration,
}

print(sa[0:2])