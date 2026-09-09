from typing import List, Dict, Any

class TrialBalanceEngine:
    """
    Trial Balance import, balance verification, anomaly detection,
    financial ratios, horizontal and vertical analysis.
    """

    @staticmethod
    def verify_balance(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_debit = sum(float(acc.get('debit', 0.0)) for acc in accounts)
        total_credit = sum(float(acc.get('credit', 0.0)) for acc in accounts)
        diff = abs(total_debit - total_credit)
        is_balanced = diff < 0.01

        return {
            "total_debit": round(total_debit, 2),
            "total_credit": round(total_credit, 2),
            "difference": round(diff, 2),
            "is_balanced": is_balanced
        }

    @staticmethod
    def detect_anomalies(accounts: List[Dict[str, Any]], prior_accounts: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        anomalies = []

        prior_map = {acc['code']: acc for acc in (prior_accounts or [])}

        for acc in accounts:
            code = acc.get('code', '')
            name = acc.get('name', '').lower()
            debit = float(acc.get('debit', 0.0))
            credit = float(acc.get('credit', 0.0))
            net = debit - credit

            # 1. Cash / Bank accounts with negative balance (credit balance)
            if any(k in name for k in ['نقد', 'صندوق', 'بنك', 'cash', 'bank']):
                if net < 0:
                    anomalies.append({
                        "account_code": code,
                        "account_name": acc.get('name'),
                        "type": "Negative Cash / Overdraft",
                        "severity": "High",
                        "detail": f"حساب النقدية بالبنوك أو الصندوق ذو رصيد دائن غير اعتيادي بقيمة {abs(net):,.2f} ر.س."
                    })

            # 2. Expense accounts with credit net balance
            if any(k in name for k in ['مصروف', 'تكلفة', 'رواتب', 'إيجار', 'expense', 'cost', 'salary', 'rent']):
                if net < 0:
                    anomalies.append({
                        "account_code": code,
                        "account_name": acc.get('name'),
                        "type": "Unexpected Credit Balance in Expenses",
                        "severity": "Medium",
                        "detail": f"حساب المصروفات يظهر برصيد دائن غير طبيعي بقيمة {abs(net):,.2f} ر.س."
                    })

            # 3. Revenue accounts with debit net balance
            if any(k in name for k in ['إيراد', 'مبيعات', 'revenue', 'sales', 'turnover']):
                if net > 0:
                    anomalies.append({
                        "account_code": code,
                        "account_name": acc.get('name'),
                        "type": "Unexpected Debit Balance in Revenue",
                        "severity": "High",
                        "detail": f"حساب الإيرادات يظهر برصيد مدين غير طبيعي بقيمة {net:,.2f} ر.س."
                    })

            # 4. Significant drift/growth compared to prior year (> 25% and > 50,000)
            if code in prior_map:
                prior_acc = prior_map[code]
                prior_net = float(prior_acc.get('debit', 0.0)) - float(prior_acc.get('credit', 0.0))
                if abs(prior_net) > 1000:
                    var_pct = ((abs(net) - abs(prior_net)) / abs(prior_net)) * 100
                    if abs(var_pct) > 25 and abs(net - prior_net) > 50000:
                        anomalies.append({
                            "account_code": code,
                            "account_name": acc.get('name'),
                            "type": "Significant Fluctuation",
                            "severity": "Medium",
                            "detail": f"تغير جوهري في رصيد الحساب بنسبة {var_pct:+.1f}% عن العام السابق (الفارق: {abs(net - prior_net):,.2f} ر.س)."
                        })

        return anomalies

    @staticmethod
    def calculate_financial_metrics(mapped_accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes key financial summary figures and ratios.
        """
        totals = {
            "current_assets": 0.0,
            "non_current_assets": 0.0,
            "current_liabilities": 0.0,
            "non_current_liabilities": 0.0,
            "equity": 0.0,
            "revenue": 0.0,
            "cogs": 0.0,
            "operating_expenses": 0.0,
            "zakat_tax": 0.0,
            "net_profit": 0.0
        }

        for acc in mapped_accounts:
            fs_cat = acc.get('fs_category', '')
            net = float(acc.get('debit', 0.0)) - float(acc.get('credit', 0.0))

            if fs_cat == 'CurrentAssets':
                totals['current_assets'] += net
            elif fs_cat == 'NonCurrentAssets':
                totals['non_current_assets'] += net
            elif fs_cat == 'CurrentLiabilities':
                totals['current_liabilities'] += -net
            elif fs_cat == 'NonCurrentLiabilities':
                totals['non_current_liabilities'] += -net
            elif fs_cat == 'Equity':
                totals['equity'] += -net
            elif fs_cat == 'Revenue':
                totals['revenue'] += -net
            elif fs_cat == 'CostOfGoodsSold':
                totals['cogs'] += net
            elif fs_cat == 'OperatingExpenses':
                totals['operating_expenses'] += net
            elif fs_cat == 'ZakatTax':
                totals['zakat_tax'] += net

        total_assets = totals['current_assets'] + totals['non_current_assets']
        total_liabilities = totals['current_liabilities'] + totals['non_current_liabilities']
        gross_profit = totals['revenue'] - totals['cogs']
        operating_profit = gross_profit - totals['operating_expenses']
        pbt = operating_profit  # assuming no other expenses
        net_income = pbt - totals['zakat_tax']

        current_ratio = round(totals['current_assets'] / totals['current_liabilities'], 2) if totals['current_liabilities'] > 0 else 0.0
        debt_to_equity = round(total_liabilities / totals['equity'], 2) if totals['equity'] > 0 else 0.0
        gross_margin = round((gross_profit / totals['revenue']) * 100, 2) if totals['revenue'] > 0 else 0.0
        operating_margin = round((operating_profit / totals['revenue']) * 100, 2) if totals['revenue'] > 0 else 0.0
        roe = round((net_income / totals['equity']) * 100, 2) if totals['equity'] > 0 else 0.0

        return {
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "total_equity": round(totals['equity'], 2),
            "revenue": round(totals['revenue'], 2),
            "cogs": round(totals['cogs'], 2),
            "gross_profit": round(gross_profit, 2),
            "operating_expenses": round(totals['operating_expenses'], 2),
            "operating_profit": round(operating_profit, 2),
            "profit_before_tax": round(pbt, 2),
            "net_income": round(net_income, 2),
            "current_ratio": current_ratio,
            "debt_to_equity": debt_to_equity,
            "gross_margin_pct": gross_margin,
            "operating_margin_pct": operating_margin,
            "roe_pct": roe
        }
