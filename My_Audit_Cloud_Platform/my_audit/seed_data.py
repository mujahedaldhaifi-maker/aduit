import os
import json
from my_audit.database import init_db
from my_audit.services.audit_service import AuditService
from my_audit.services.report_generator import ReportGenerator

def load_seed_data(db_path=None):
    init_db(db_path)
    service = AuditService(db_path)
    reporter = ReportGenerator(db_path)

    # 1. Client Master
    client = service.create_client({
        "client_id": "CL-RUWAD-01",
        "name": "شركة الرواد للتجارة والصناعة (شركة مساهمة مقفلة)",
        "tax_id": "300123456700003",
        "industry": "تجارة وتصنيع المواد الاستهلاكية",
        "accounting_system": "SAP S/4HANA Cloud",
        "fiscal_year_end": "2026-12-31"
    }, user_name="Admin")

    # 2. Client Acceptance (ISA 210)
    service.evaluate_acceptance({
        "client_id": client["client_id"],
        "independence_passed": True,
        "integrity_passed": True,
        "conflict_of_interest": False,
        "risk_level": "Medium",
        "decision": "Accepted",
        "notes": "تم التحقق من استقلالية المكتب وأعضاء الفريق وعدم وجود أي تعارض مصالح أو خدمات غير تأكيدية محظورة.",
        "evaluated_by": "أ. محمد القحطاني (Engagement Partner)"
    }, user_name="Engagement Partner")

    # 3. Engagement Setup
    engagement = service.create_engagement({
        "engagement_id": "ENG-2026-RUWAD",
        "client_id": client["client_id"],
        "title": "مراجعة القوائم المالية السنوية للسنة المنتهية في 31 ديسمبر 2026م",
        "fiscal_year": 2026,
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "partner_name": "أ. محمد القحطاني",
        "manager_name": "أ. سارة العتيبي",
        "senior_name": "أ. أحمد الشهري",
        "auditor_name": "أ. خالد الدوسري",
        "eqcr_reviewer": "أ. د. فهد المنصور (Independent EQCR Partner)",
        "budgeted_hours": 160.0
    }, user_name="Engagement Partner")

    eng_id = engagement["engagement_id"]

    # 4. Trial Balance Accounts (Debits == Credits == 25,670,000.00)
    raw_tb = [
        {"code": "1010", "name": "النقدية لدى البنوك - الحسابات الجارية", "debit": 2450000.0, "credit": 0.0},
        {"code": "1020", "name": "صندوق العهدة النقدية (Petty Cash)", "debit": 50000.0, "credit": 0.0},
        {"code": "1200", "name": "العملاء والذمم المدينة التجارية", "debit": 4120000.0, "credit": 0.0},
        {"code": "1290", "name": "مخصص الخسائر الائتمانية المتوقعة (ECL)", "debit": 0.0, "credit": 180000.0},
        {"code": "1300", "name": "المخزون السلعي - بضاعة تامة الصنع", "debit": 3500000.0, "credit": 0.0},
        {"code": "1400", "name": "مصروفات وتأمينات مدفوعة مقدماً", "debit": 250000.0, "credit": 0.0},
        {"code": "1500", "name": "الممتلكات والآلات والمعدات (PPE)", "debit": 4980000.0, "credit": 0.0},
        {"code": "1590", "name": "مجمع إهلاك الممتلكات والمعدات", "debit": 0.0, "credit": 800000.0},
        {"code": "2010", "name": "الموردون والذمم الدائنة التجارية", "debit": 0.0, "credit": 2850000.0},
        {"code": "2020", "name": "مصروفات ورواتب مستحقة الدفع", "debit": 0.0, "credit": 450000.0},
        {"code": "2030", "name": "مخصص الزكاة الشرعية المستحقة", "debit": 0.0, "credit": 120000.0},
        {"code": "2100", "name": "قروض وتسهيلات بنكية طويلة الأجل", "debit": 0.0, "credit": 1220000.0},
        {"code": "2500", "name": "مخصص مكافأة نهاية الخدمة للموظفين", "debit": 0.0, "credit": 650000.0},
        {"code": "3010", "name": "رأس المال المدفوع", "debit": 0.0, "credit": 5000000.0},
        {"code": "3020", "name": "الاحتياطي النظامي", "debit": 0.0, "credit": 1000000.0},
        {"code": "3030", "name": "الأرباح المبقاة (المجمعة)", "debit": 0.0, "credit": 1000000.0},
        {"code": "4010", "name": "إيرادات المبيعات والخدمات", "debit": 0.0, "credit": 12400000.0},
        {"code": "5010", "name": "تكلفة المبيعات المباشرة (COGS)", "debit": 8200000.0, "credit": 0.0},
        {"code": "6010", "name": "رواتب ومزايا موظفي الإدارة والتسويق", "debit": 1200000.0, "credit": 0.0},
        {"code": "6020", "name": "إيجار ومرافق عمومية ومصاريف تسويق", "debit": 530000.0, "credit": 0.0},
        {"code": "6030", "name": "استهلاك الممتلكات والآلات والمعدات", "debit": 270000.0, "credit": 0.0},
        {"code": "6040", "name": "مصروف الزكاة الشرعية للعام الحالي", "debit": 120000.0, "credit": 0.0}
    ]

    tb_result = service.import_trial_balance(eng_id, raw_tb, user_name="Auditor")

    # 5. Materiality Engine (ISA 320)
    pbt = 2200000.0
    materiality = service.calculate_and_set_materiality(
        engagement_id=eng_id,
        benchmark_type="ProfitBeforeTax",
        benchmark_amount=pbt,
        overall_percentage=5.0,
        performance_percentage=75.0,
        trivial_percentage=5.0,
        user_name="أ. محمد القحطاني (Engagement Partner)"
    )

    # 6. Risk Assessment (ISA 315)
    r1 = service.add_risk({
        "engagement_id": eng_id,
        "account_category": "Revenue",
        "fs_line_item": "Revenue from Contracts with Customers",
        "description": "خطر تضخيم الإيرادات والاعتراف المبكر بالمبيعات حول نهاية السنة المالية (افتراض احتيال ISA 240).",
        "assertion": "Existence",
        "inherent_risk": "High",
        "control_risk": "Medium",
        "planned_response": "فحص عينة MUS لفواتير المبيعات وبوالص الشحن، واختبارات الفصل الزمني Cut-off واختبار قيود اليومية."
    }, user_name="Senior Auditor")

    r2 = service.add_risk({
        "engagement_id": eng_id,
        "account_category": "Inventory",
        "fs_line_item": "Inventories",
        "description": "خطر عدم كفاية مخصص هبوط المخزون إلى صافي القيمة القابلة للتحقق (NRV) وتقادم البضاعة.",
        "assertion": "Accuracy & Valuation",
        "inherent_risk": "Medium",
        "control_risk": "Medium",
        "planned_response": "حضور الجرد الفعلي، فحص تقرير تقادم المخزون، ومقارنة تكلفة المخزون مع أسعار البيع اللاحقة."
    }, user_name="Senior Auditor")

    r3 = service.add_risk({
        "engagement_id": eng_id,
        "account_category": "Cash",
        "fs_line_item": "Cash and Cash Equivalents",
        "description": "خطر وجود تسويات بنكية معلقة غير مسجلة بالدفاتر أو تحويلات مكررة.",
        "assertion": "Existence",
        "inherent_risk": "High",
        "control_risk": "Low",
        "planned_response": "إرسال مصادقات بنكية مباشرة لـ 100% من البنوك المتعامل معها وفحص مذكرات التسوية بعد نهاية السنة."
    }, user_name="Senior Auditor")

    r4 = service.add_risk({
        "engagement_id": eng_id,
        "account_category": "Receivables",
        "fs_line_item": "Trade Receivables",
        "description": "خطر تعثر ديون قديمة وعدم كفاية مخصص خسائر الائتمان المتوقعة وفق المعيار الدولي IFRS 9.",
        "assertion": "Accuracy & Valuation",
        "inherent_risk": "High",
        "control_risk": "Medium",
        "planned_response": "مصادقات عينة العملاء الكبار، اختبار مصفوفة الأعمار الزمنية واختبار التحصيلات اللاحقة."
    }, user_name="Senior Auditor")

    # 7. Audit Programs & Procedures (ISA 330)
    p_rev = service.create_program(eng_id, "Revenue", "برنامج مراجعة الإيرادات والمبيعات (ISA 330)")
    p_bnk = service.create_program(eng_id, "Cash & Bank", "برنامج مراجعة النقد وما في حكمه بالبنوك")
    p_inv = service.create_program(eng_id, "Inventory", "برنامج مراجعة المخزون السلعي وتكلفة المبيعات")
    p_rec = service.create_program(eng_id, "Receivables", "برنامج مراجعة العملاء والذمم المدينة التجارية")

    proc1 = service.add_procedure({
        "program_id": p_rev["program_id"],
        "risk_id": r1["risk_id"],
        "procedure_type": "SubstantiveTest",
        "description": "اختبار تفاصيل المبيعات والفصل الزمني (Cut-off) وعينة MUS للفواتير الكبيرة.",
        "assertion": "Existence",
        "population_size": 12400000,
        "sample_size": 45
    })

    proc2 = service.add_procedure({
        "program_id": p_bnk["program_id"],
        "risk_id": r3["risk_id"],
        "procedure_type": "SubstantiveTest",
        "description": "الحصول على مصادقات البنوك المباشرة 100% ومطابقة مذكرات التسوية البنكية وكشوف الحسابات.",
        "assertion": "Existence",
        "population_size": 2450000,
        "sample_size": 3
    })

    proc3 = service.add_procedure({
        "program_id": p_inv["program_id"],
        "risk_id": r2["risk_id"],
        "procedure_type": "SubstantiveTest",
        "description": "حضور الجرد الفعلي للمخزون بمستودعات الرياض وجدة وفحص اختبارات NRV.",
        "assertion": "Accuracy & Valuation",
        "population_size": 3500000,
        "sample_size": 60
    })

    proc4 = service.add_procedure({
        "program_id": p_rec["program_id"],
        "risk_id": r4["risk_id"],
        "procedure_type": "SubstantiveTest",
        "description": "إرسال مصادقات العملاء وفحص التحصيلات اللاحقة وتقييم مخصص التعثر IFRS 9.",
        "assertion": "Accuracy & Valuation",
        "population_size": 4120000,
        "sample_size": 35
    })

    # 8. Sampling Engine Run (ISA 530)
    sample_run = service.calculate_sampling({
        "procedure_id": proc1["procedure_id"],
        "population_value": 12400000.0,
        "tolerable_misstatement": materiality["performance_materiality"],
        "expected_misstatement": 0.0,
        "confidence_level": 0.95
    })

    # 9. Working Papers (ISA 230)
    wp1 = service.document_working_paper({
        "procedure_id": proc1["procedure_id"],
        "title": "ورقة عمل اختبار تفاصيل المبيعات والفصل الزمني للمبيعات (Cut-off)",
        "objective": "التحقق من صحة واكتمال الإيرادات وعدم وجود اعتراف وهمي أو مبكر قبل التسليم.",
        "assertion": "Existence & Cut-off",
        "procedures_performed": "تم اختيار عينة MUS شملت 45 فاتورة مبيعات، ومطابقتها مع أوامر الشراء المعتمدة وبوالص الشحن الموقعة بالاستلام، وفحص آخر 15 عملية قبل وبعد تاريخ الإقفال.",
        "results": "كافة فواتير العينة موثقة ومطابقة لمستندات الشحن والتسليم. لم يُلاحظ أي تجاوز زمني في المبيعات المسجلة.",
        "exceptions_noted": "لا توجد أي استثناءات جوهرية.",
        "conclusion": "الإيرادات مسجلة بصورة عادلة ووفقًا للمعيار الدولي للتقرير المالي IFRS 15.",
        "prepared_by": "أ. خالد الدوسري (Staff Auditor)",
        "reviewed_by": "أ. سارة العتيبي (Audit Manager)"
    })

    wp2 = service.document_working_paper({
        "procedure_id": proc2["procedure_id"],
        "title": "ورقة عمل مطابقة الأرصدة البنكية ومذكرات التسوية والمصادقات",
        "objective": "التحقق من صحة ووجود أرصدة النقدية لدى البنوك.",
        "assertion": "Existence & Rights",
        "procedures_performed": "تم إرسال خطابات مصادقة مباشرة لجميع البنوك، ومطابقة الأرصدة المصادق عليها مع الدفاتر ومذكرات التسوية.",
        "results": "وردت كافة المصادقات البنكية مباشرة للمكتب، وتطابقت 100% مع الأرصدة الدفترية ومذكرات التسوية البنكية المعتمدة.",
        "exceptions_noted": "لا توجد فروقات معلقة.",
        "conclusion": "أرصدة النقدية لدى البنوك صحيحة ومطابقة ومملوكة للشركة وخالية من أي رهونات غير معلنة.",
        "prepared_by": "أ. خالد الدوسري (Staff Auditor)",
        "reviewed_by": "أ. أحمد الشهري (Audit Senior)"
    })

    wp3 = service.document_working_paper({
        "procedure_id": proc3["procedure_id"],
        "title": "ورقة عمل حضور جرد المخزون واختبار صافي القيمة القابلة للتحقق",
        "objective": "التحقق من الوجود المادي للمخزون وحالته وتقييمه بالتكلفة أو صافي القيمة القابلة للتحقق أيهما أقل.",
        "assertion": "Existence & Valuation",
        "procedures_performed": "حضور فريق المراجعة للجرد الفعلي بمستودعات الرياض وجدة، والقيام بعدّ اختباري لـ 60 صنفاً، ومقارنة التكلفة بأسعار البيع اللاحقة بعد خصم مصاريف البيع.",
        "results": "تطابقت نتائج العد الاختباري بنسبة 99.8% مع كشوفات الجرد الدفترية. متوسط هامش الربح إيجابي لكافة الأصناف ولم تظهر حاجة لزيادة مخصص الهبوط.",
        "exceptions_noted": "فارق عجز طبيعي بسيط جداً بمبلغ 1,400 ر.س تمت معالجته دفترياً.",
        "conclusion": "المخزون موجود ومُقَيّم وفقًا للمعيار المحاسبي الدولي IAS 2.",
        "prepared_by": "أ. أحمد الشهري (Audit Senior)",
        "reviewed_by": "أ. سارة العتيبي (Audit Manager)"
    })

    wp4 = service.document_working_paper({
        "procedure_id": proc4["procedure_id"],
        "title": "ورقة عمل فحص أرصدة العملاء ومخصص الخسائر الائتمانية IFRS 9",
        "objective": "التحقق من وجود وقابلية تحصيل الذمم المدينة التجارية وملاءمة مخصص التعثر.",
        "assertion": "Accuracy & Valuation",
        "procedures_performed": "إرسال مصادقات لأكبر 10 عملاء يمثلون 70% من إجمالي الرصيد، وفحص التحصيلات البنكية اللاحقة بعد تاريخ الميزانية حتى تاريخ الفحص.",
        "results": "وردت المصادقات متطابقة، وتم تحصيل 82% من رصيد العملاء حتى نهاية شهر فبراير 2027.",
        "exceptions_noted": "لا توجد استثناءات.",
        "conclusion": "رصيد العملاء ومخصص الخسائر الائتمانية البالغ 180,000 ر.س كافٍ وعادل.",
        "prepared_by": "أ. خالد الدوسري (Staff Auditor)",
        "reviewed_by": "أ. محمد القحطاني (Engagement Partner)"
    })

    # 10. Evidence Management
    service.attach_evidence({
        "procedure_id": proc1["procedure_id"],
        "wp_id": wp1["wp_id"],
        "file_name": "Sales_Invoices_Sample_Signed_PODs.pdf",
        "file_type": "PDF",
        "file_size": 2450000,
        "description": "صور فواتير المبيعات وبوالص الشحن الموقعة بالاستلام لعينة المبيعات.",
        "source": "ClientPBC"
    })

    service.attach_evidence({
        "procedure_id": proc2["procedure_id"],
        "wp_id": wp2["wp_id"],
        "file_name": "Bank_Confirmations_Direct_Rajhi_SNB.pdf",
        "file_type": "PDF",
        "file_size": 1150000,
        "description": "خطابات المصادقة البنكية الواردة مباشرة من مصرف الراجحي والبنك الأهلي السعودي.",
        "source": "ThirdPartyBank"
    })

    # 11. External Confirmations (ISA 505)
    c1 = service.create_confirmation({
        "engagement_id": eng_id,
        "recipient_name": "مصرف الراجحي - الإدارة الإقليمية",
        "recipient_type": "Bank",
        "account_reference": "SA1280000123456789012345",
        "book_balance": 1850000.0,
        "confirmed_balance": 1850000.0,
        "notes": "تمت المصادقة والمطابقة الكاملة مع كشف الحساب البنكي."
    })
    service.reconcile_confirmation(c1["confirmation_id"], 1850000.0, "تمت المطابقة مع رصيد الدفاتر.")

    c2 = service.create_confirmation({
        "engagement_id": eng_id,
        "recipient_name": "البنك الأهلي السعودي (SNB)",
        "recipient_type": "Bank",
        "account_reference": "SA4510000987654321098765",
        "book_balance": 600000.0,
        "confirmed_balance": 600000.0,
        "notes": "مطابقة تامة لرصيد الحساب الجاري."
    })
    service.reconcile_confirmation(c2["confirmation_id"], 600000.0, "تمت المطابقة.")

    # 12. Review Notes / Findings
    rn = service.raise_review_note({
        "engagement_id": eng_id,
        "wp_id": wp1["wp_id"],
        "raised_by": "أ. سارة العتيبي (Audit Manager)",
        "assigned_to": "أ. خالد الدوسري (Staff Auditor)",
        "priority": "High",
        "note_text": "يرجى التحقق من الفاتورة رقم 8841 بمبلغ 120,000 ر.س والتأكد من إرفاق بوليصة الشحن الأصلية."
    })
    service.clear_review_note(
        rn["note_id"],
        "تم فحص بوليصة الشحن الأصلية الموقعة من العميل بتاريخ 28 ديسمبر 2026 وإرفاقها بملف الدليل ورقة العمل.",
        user_name="أ. سارة العتيبي (Audit Manager)"
    )

    # 13. Misstatements / Adjustments (ISA 450)
    service.record_misstatement({
        "engagement_id": eng_id,
        "description": "فارق في احتساب استهلاك أصل ثابت طفيف لا يتجاوز عتبة الخطأ التافه.",
        "amount": 3200.0,
        "misstatement_type": "Judgmental",
        "is_adjusted": False,
        "impact_on_pnl": -3200.0
    })

    # 14. EQCR Review (ISA 220, ISQM 2)
    service.submit_eqcr_review({
        "engagement_id": eng_id,
        "reviewer_name": "أ. د. فهد المنصور (EQCR Partner)",
        "is_eqcr_required": True,
        "checklist_results": {
            "independence_reassessed": True,
            "risk_assessment_appropriate": True,
            "materiality_justified": True,
            "sufficient_appropriate_evidence": True,
            "kams_properly_formulated": True,
            "unadjusted_misstatements_immaterial": True
        },
        "reviewer_comments": "تمت مراجعة جودة الارتباط بصفة مستقلة، وتبين استيفاء متطلبات معايير المراجعة الدولية (ISA) وجودة التوثيق الكافي، والموافقة التامة على إصدار تقرير المراجع غير المتحفظ.",
        "approved": True
    })

    print(f"Seed data successfully populated for engagement {eng_id}")
    return eng_id

if __name__ == "__main__":
    load_seed_data()
