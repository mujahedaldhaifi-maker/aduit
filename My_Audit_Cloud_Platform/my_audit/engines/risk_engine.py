from typing import List, Dict, Any

class RiskEngine:
    """
    ISA 315 (Revised) Risk Assessment Engine:
    Calculates Risk of Material Misstatement (RMM) from Inherent & Control Risk,
    maps assertions, and generates automatic risk suggestions.
    """

    MATRIX = {
        ('High', 'High'): 'Significant',
        ('High', 'Medium'): 'High',
        ('High', 'Low'): 'Medium',
        ('Medium', 'High'): 'High',
        ('Medium', 'Medium'): 'Medium',
        ('Medium', 'Low'): 'Low',
        ('Low', 'High'): 'Medium',
        ('Low', 'Medium'): 'Low',
        ('Low', 'Low'): 'Low'
    }

    ASSERTIONS = [
        "Existence",              # الوجود
        "Completeness",           # الاكتمال
        "Accuracy & Valuation",   # الدقة والتقييم
        "Rights & Obligations",   # الحقوق والالتزامات
        "Cut-off",                # الفصل الزمني
        "Presentation & Disclosure" # العرض والإفصاح
    ]

    @classmethod
    def evaluate_rmm(cls, inherent_risk: str, control_risk: str) -> Dict[str, Any]:
        key = (inherent_risk.capitalize(), control_risk.capitalize())
        rmm = cls.MATRIX.get(key, 'Medium')
        is_significant = 1 if rmm == 'Significant' else 0

        # Suggested response based on ISA 330
        if rmm in ['Significant', 'High']:
            planned_response = "Extended Substantive Testing + Specific Tests of Details"
        elif rmm == 'Medium':
            planned_response = "Combined Approach (Tests of Controls & Substantive Analytical Procedures)"
        else:
            planned_response = "Standard Substantive Analytical Procedures"

        return {
            "inherent_risk": inherent_risk,
            "control_risk": control_risk,
            "rmm": rmm,
            "is_significant": is_significant,
            "planned_response": planned_response
        }

    @classmethod
    def suggest_risks_from_financials(cls, financial_metrics: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        AI-assisted rule generator for risks based on ISA 315.
        """
        suggested = []

        # 1. Presumed risk of fraud in revenue recognition (ISA 240)
        suggested.append({
            "account_category": "Revenue",
            "fs_line_item": "Revenue from Contracts with Customers",
            "description": "خطر تضخيم الإيرادات أو الاعتراف المبكر بها قبل استيفاء التزامات الأداء (افتراض احتيال وفق ISA 240).",
            "assertion": "Existence",
            "inherent_risk": "High",
            "control_risk": "Medium",
            "rmm": "High",
            "is_significant": 1,
            "planned_response": "فحص عينة من فواتير المبيعات مع بوالص الشحن واختبارات الفصل الزمني Cut-off واختبار قيود اليومية."
        })

        # 2. Risk in Cash & Bank if overdraft or large balance
        if any(a.get('type') == 'Negative Cash / Overdraft' for a in anomalies):
            suggested.append({
                "account_category": "Cash",
                "fs_line_item": "Cash and Cash Equivalents",
                "description": "خطر عدم صحة رصيد النقدية وظهور رصيد سالب قد يشير إلى قيود معلقة أو سحب على المكشوف غير مفصح عنه.",
                "assertion": "Accuracy & Valuation",
                "inherent_risk": "High",
                "control_risk": "High",
                "rmm": "Significant",
                "is_significant": 1,
                "planned_response": "إرسال مصادقات بنكية مباشرة لجميع البنوك ومراجعة مذكرة تسوية البنك وفحص الشيكات المعلقة."
            })

        # 3. Inventory Valuation if inventory is significant
        if financial_metrics.get('total_assets', 0) > 0:
            suggested.append({
                "account_category": "Inventory",
                "fs_line_item": "Inventories",
                "description": "خطر تقادم المخزون وعدم كفاية مخصص الهبوط إلى صافي القيمة القابلة للتحقق (NRV).",
                "assertion": "Accuracy & Valuation",
                "inherent_risk": "Medium",
                "control_risk": "Medium",
                "rmm": "Medium",
                "is_significant": 0,
                "planned_response": "حضور الجرد الفعلي للمخزون، اختبار تقادم الأصناف ومقارنة تكلفة المخزون بأسعار البيع اللاحقة."
            })

        # 4. Going Concern risk if high leverage
        debt_to_equity = financial_metrics.get('debt_to_equity', 0)
        if debt_to_equity > 2.0:
            suggested.append({
                "account_category": "GoingConcern",
                "fs_line_item": "Financial Sustainability",
                "description": f"مخاطر استمرارية المنشأة نظرًا لارتفاع نسبة المديونية إلى حقوق الملكية ({debt_to_equity}x).",
                "assertion": "Presentation & Disclosure",
                "inherent_risk": "High",
                "control_risk": "Medium",
                "rmm": "High",
                "is_significant": 1,
                "planned_response": "مراجعة توقعات التدفقات النقدية للإدارة لـ 12 شهرًا قادمة وفحص خطابات التمويل والتسهيلات البنكية."
            })

        return suggested
