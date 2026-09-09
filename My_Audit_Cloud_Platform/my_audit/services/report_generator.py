from datetime import datetime
from typing import Dict, Any, List
from my_audit.database import get_connection

class ReportGenerator:
    def __init__(self, db_path=None):
        self.db_path = db_path

    def _conn(self):
        return get_connection(self.db_path)

    def generate_lead_schedules(self, engagement_id: str) -> List[Dict[str, Any]]:
        conn = self._conn()
        rows = conn.execute("""
            SELECT a.fs_category, a.fs_line_item, a.code, a.name, a.net_balance, a.debit, a.credit,
                   tb.is_balanced
            FROM accounts a
            JOIN trial_balances tb ON tb.tb_id = a.tb_id
            WHERE tb.engagement_id = ?
            ORDER BY a.fs_category, a.code
        """, (engagement_id,)).fetchall()

        schedules = {}
        for r in rows:
            line_item = r['fs_line_item'] or 'General Accounts'
            if line_item not in schedules:
                schedules[line_item] = {
                    "line_item": line_item,
                    "fs_category": r['fs_category'],
                    "total_net": 0.0,
                    "accounts": []
                }
            schedules[line_item]['total_net'] += r['net_balance']
            schedules[line_item]['accounts'].append({
                "code": r['code'],
                "name": r['name'],
                "debit": r['debit'],
                "credit": r['credit'],
                "net": r['net_balance']
            })

        conn.close()
        return list(schedules.values())

    def generate_draft_financial_statements(self, engagement_id: str) -> Dict[str, Any]:
        schedules = self.generate_lead_schedules(engagement_id)

        balance_sheet = {"assets": [], "liabilities": [], "equity": []}
        income_statement = {"revenue": [], "cogs": [], "operating_expenses": [], "zakat_tax": []}

        total_assets = 0.0
        total_liab = 0.0
        total_equity = 0.0
        total_rev = 0.0
        total_cogs = 0.0
        total_opex = 0.0
        total_zakat = 0.0

        for s in schedules:
            cat = s['fs_category']
            val = s['total_net']

            if cat == 'CurrentAssets':
                balance_sheet['assets'].append({"item": s['line_item'], "amount": val, "type": "Current"})
                total_assets += val
            elif cat == 'NonCurrentAssets':
                balance_sheet['assets'].append({"item": s['line_item'], "amount": val, "type": "Non-Current"})
                total_assets += val
            elif cat == 'CurrentLiabilities':
                balance_sheet['liabilities'].append({"item": s['line_item'], "amount": -val, "type": "Current"})
                total_liab += -val
            elif cat == 'NonCurrentLiabilities':
                balance_sheet['liabilities'].append({"item": s['line_item'], "amount": -val, "type": "Non-Current"})
                total_liab += -val
            elif cat == 'Equity':
                balance_sheet['equity'].append({"item": s['line_item'], "amount": -val})
                total_equity += -val
            elif cat == 'Revenue':
                income_statement['revenue'].append({"item": s['line_item'], "amount": -val})
                total_rev += -val
            elif cat == 'CostOfGoodsSold':
                income_statement['cogs'].append({"item": s['line_item'], "amount": val})
                total_cogs += val
            elif cat == 'OperatingExpenses':
                income_statement['operating_expenses'].append({"item": s['line_item'], "amount": val})
                total_opex += val
            elif cat == 'ZakatTax':
                income_statement['zakat_tax'].append({"item": s['line_item'], "amount": val})
                total_zakat += val

        gross_profit = total_rev - total_cogs
        net_operating_profit = gross_profit - total_opex
        pbt = net_operating_profit
        net_income = pbt - total_zakat

        return {
            "balance_sheet": {
                "assets": balance_sheet['assets'],
                "total_assets": round(total_assets, 2),
                "liabilities": balance_sheet['liabilities'],
                "total_liabilities": round(total_liab, 2),
                "equity": balance_sheet['equity'],
                "total_equity": round(total_equity, 2),
                "total_liabilities_and_equity": round(total_liab + total_equity, 2)
            },
            "income_statement": {
                "revenue": income_statement['revenue'],
                "total_revenue": round(total_rev, 2),
                "cogs": income_statement['cogs'],
                "total_cogs": round(total_cogs, 2),
                "gross_profit": round(gross_profit, 2),
                "operating_expenses": income_statement['operating_expenses'],
                "total_operating_expenses": round(total_opex, 2),
                "operating_profit": round(net_operating_profit, 2),
                "profit_before_tax": round(pbt, 2),
                "zakat_and_tax": round(total_zakat, 2),
                "net_income": round(net_income, 2)
            }
        }

    def generate_auditor_report(self, engagement_id: str) -> Dict[str, Any]:
        conn = self._conn()
        eng = conn.execute("""
            SELECT e.*, c.name as client_name, c.tax_id as client_tax_id, c.industry
            FROM engagements e
            JOIN clients c ON c.client_id = e.client_id
            WHERE e.engagement_id = ?
        """, (engagement_id,)).fetchone()

        if not eng:
            conn.close()
            raise ValueError(f"Engagement {engagement_id} not found")

        risks = conn.execute("SELECT * FROM risks WHERE engagement_id = ? AND is_significant = 1", (engagement_id,)).fetchall()
        misstatements = conn.execute("SELECT * FROM misstatements WHERE engagement_id = ?", (engagement_id,)).fetchall()
        mat = conn.execute("SELECT * FROM materiality WHERE engagement_id = ? ORDER BY approved_at DESC LIMIT 1", (engagement_id,)).fetchone()
        conn.close()

        unadjusted = sum(m['amount'] for m in misstatements if m['is_adjusted'] == 0)
        pm = mat['performance_materiality'] if mat else 100000.0

        is_clean = unadjusted <= pm
        opinion_type = "Unmodified / Clean Opinion (رأي غير متحفظ)" if is_clean else "Modified / Qualified Opinion (رأي متحفظ)"

        # Formulate Key Audit Matters (ISA 701)
        kams = []
        for r in risks:
            kams.append({
                "title": f"مخاطر {r['account_category']} ({r['assertion']})",
                "description": r['description'],
                "audit_response": r['planned_response']
            })

        today_ar = datetime.now().strftime("%Y-%m-%d")
        client_name = eng['client_name']
        year = eng['fiscal_year']

        report_text = f"""
================================================================================
                      تقرير مراجع الحسابات المستقل
                     INDEPENDENT AUDITOR'S REPORT
================================================================================
إلى السادة / مساهمي شركة {client_name}
الرياض - المملكة العربية السعودية

أولاً: الرأي (Opinion):
راجعنا القوائم المالية لشركة {client_name} ("الشركة")، والتي تشتمل على قائمة المركز المالي كما في 31 ديسمبر {year}م، وقائمة الربح أو الخسارة والدخل الشامل الآخر، وقائمة التغيرات في حقوق الملكية، وقائمة التدفقات النقدية للسنة المنتهية في ذلك التاريخ، والإيضاحات المرفقة بالقوائم المالية بما في ذلك ملخص السياسات المحاسبية الهامة.

وفي رأينا، فإن القوائم المالية المرفقة تظهر بعدالة، من كافة النواحي الجوهرية، المركز المالي لشركة {client_name} كما في 31 ديسمبر {year}م، وأداءها المالي وتدفقاتها النقدية للسنة المنتهية في ذلك التاريخ وفقاً للمعايير الدولية للتقرير المالي المعتمدة في المملكة العربية السعودية (IFRS) والمعايير والإصدارات الأخرى المعتمدة من الهيئة السعودية للمراجعين والمحاسبين (SOCPA).

نوع الرأي الممنوح: {opinion_type}

ثانياً: أساس الرأي (Basis for Opinion):
تمت مراجعتنا وفقاً للمعايير الدولية للمراجعة المعتمدة في المملكة العربية السعودية (ISA). ونحن مستقلون عن الشركة وفقاً لقواعد سلوك وآداب المهنة المعتمدة في المملكة، وقد التزمنا بمسؤولياتنا الأخلاقية الأخرى وفقاً لتلك القواعد. ونعتقد أن أدلة المراجعة التي حصلنا عليها كافية ومناسبة لتوفير أساس لرأينا.

ثالثاً: أمور المراجعة الرئيسية (Key Audit Matters - ISA 701):
أمور المراجعة الرئيسية هي تلك الأمور التي، وفقاً لحكمنا المهني، كانت لها الأهمية القصوى في مراجعتنا للقوائم المالية للفترة الحالية:
"""
        for i, kam in enumerate(kams, 1):
            report_text += f"\n[{i}] {kam['title']}:\n- الوصف والخطر: {kam['description']}\n- كيفية معالجة الأمر في المراجعة: {kam['audit_response']}\n"

        report_text += f"""
رابعاً: مسؤوليات الإدارة والمكلفين بالحوكمة عن القوائم المالية:
الإدارة مسؤولة عن إعداد القوائم المالية وعرضها العادل وفقاً للمعايير الدولية للتقرير المالي المعتمدة في المملكة، ونظام الشركات، وتصميم نظام الرقابة الداخلية المناسب.

خامساً: تقرير حول المتطلبات النظامية والتنظيمية الأخرى:
وفقاً للمعلومات والتوضيحات المقدمة إلينا، لم يتبين لنا وجود مخالفة جوهرية لأحكام نظام الشركات السعودي أو عقد تأسيس الشركة خلال السنة المنتهية في 31 ديسمبر {year}م.

عن مكتب المراجعة: My Audit Partners
الشريك المسؤول: {eng['partner_name']}
ترخيص مهني صادر عن SOCPA
التاريخ: {today_ar}
================================================================================
"""
        return {
            "engagement_id": engagement_id,
            "client_name": client_name,
            "fiscal_year": year,
            "opinion_type": opinion_type,
            "partner_name": eng['partner_name'],
            "report_date": today_ar,
            "key_audit_matters": kams,
            "report_text": report_text.strip()
        }
