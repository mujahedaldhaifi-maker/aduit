import re
from typing import Dict, Any, Tuple

class MappingEngine:
    """
    Intelligent Account Mapping Engine:
    Maps Trial Balance accounts to IFRS / SOCPA Financial Statement line items.
    """

    MAPPING_RULES = [
        # Cash & Cash Equivalents
        (r'(نقد|صندوق|بنك|مصرف|cash|bank|petty)', 'CurrentAssets', 'Cash and Cash Equivalents', 0.98),
        # Accounts Receivable
        (r'(عملاء|مدينون|ذمم مدينة|زبائن|receivable|debtor|customer)', 'CurrentAssets', 'Trade Receivables', 0.95),
        # Prepayments & Other Receivables
        (r'(مدفوعات مقدما|إيجار مقدم|تأمينات|أرصدة مدينة أخرى|prepaid|advance)', 'CurrentAssets', 'Prepayments and Other Receivables', 0.90),
        # Inventory
        (r'(مخزون|بضاعة|مواد خام|إنتاج تحت التشغيل|inventory|stock)', 'CurrentAssets', 'Inventories', 0.96),
        # Property, Plant & Equipment
        (r'(أصول ثابتة|مباني|أراضي|سيارات|آلات|معدات|أثاث|ppe|property|equipment|vehicle|building)', 'NonCurrentAssets', 'Property, Plant and Equipment', 0.95),
        # Accumulated Depreciation
        (r'(مجمع إهلاك|مخصص استهلاك|accumulated depreciation)', 'NonCurrentAssets', 'Accumulated Depreciation', 0.97),
        # Accounts Payable
        (r'(موردون|دائنون|ذمم دائنة|payable|creditor|vendor|supplier)', 'CurrentLiabilities', 'Trade Payables', 0.95),
        # Accrued Expenses & Provisions
        (r'(مستحقات|مصروفات مستحقة|مخصص مكافأة نهاية الخدمة|رواتب مستحقة|accrued|provision)', 'CurrentLiabilities', 'Accruals and Other Payables', 0.92),
        # Short Term Loans
        (r'(قروض قصيرة|تسهيلات بنكية|short term loan|bank overdraft)', 'CurrentLiabilities', 'Short-term Borrowings', 0.94),
        # Zakat & Income Tax
        (r'(زكاة|ضريبة|zakat|tax|vat|zatca)', 'CurrentLiabilities', 'Zakat and Tax Payable', 0.95),
        # Long Term Debt
        (r'(قروض طويلة|تسهيلات طويلة|long term loan|term debt)', 'NonCurrentLiabilities', 'Long-term Borrowings', 0.94),
        # End of Service Benefits (Long-Term)
        (r'(مكافأة نهاية الخدمة|منافع موظفين|end of service|employee benefits)', 'NonCurrentLiabilities', 'Employees End of Service Benefits', 0.95),
        # Share Capital
        (r'(رأس المال|حصة الشركاء|share capital|paid in capital)', 'Equity', 'Share Capital', 0.99),
        # Statutory Reserve & Retained Earnings
        (r'(احتياطي نظامي|أرباح مبقاة|أرباح مدورة|خسائر متراكمة|statutory reserve|retained earnings)', 'Equity', 'Retained Earnings and Reserves', 0.98),
        # Revenue
        (r'(إيراد|مبيعات|خدمات|revenue|sales|turnover)', 'Revenue', 'Revenue from Contracts with Customers', 0.96),
        # Cost of Goods Sold
        (r'(تكلفة المبيعات|تكلفة البضاعة|مشتريات|تكلفة النشاط|cost of sales|cogs|direct cost)', 'CostOfGoodsSold', 'Cost of Sales', 0.95),
        # Operating Expenses (SG&A)
        (r'(رواتب|أجور|إيجار|تسويق|عمومية وإدارية|استهلاك|صيانة|salary|rent|marketing|admin|depreciation expense|utility)', 'OperatingExpenses', 'General, Administrative and Selling Expenses', 0.94),
        # Zakat & Tax Expense
        (r'(مصروف الزكاة|مخصص الزكاة الشرعية|zakat expense)', 'ZakatTax', 'Zakat and Income Tax Expense', 0.95)
    ]

    @classmethod
    def suggest_mapping(cls, code: str, name: str) -> Tuple[str, str, float]:
        name_clean = name.lower().strip()
        code_clean = str(code).strip()

        # Check code prefixes first if standardized (1: Assets, 2: Liab, 3: Equity, 4: Rev, 5: Cost, 6: Exp)
        if code_clean.startswith('1'):
            default_cat = 'CurrentAssets'
        elif code_clean.startswith('2'):
            default_cat = 'CurrentLiabilities'
        elif code_clean.startswith('3'):
            default_cat = 'Equity'
        elif code_clean.startswith('4'):
            default_cat = 'Revenue'
        elif code_clean.startswith('5'):
            default_cat = 'CostOfGoodsSold'
        elif code_clean.startswith('6'):
            default_cat = 'OperatingExpenses'
        else:
            default_cat = 'OperatingExpenses'

        for pattern, category, line_item, confidence in cls.MAPPING_RULES:
            if re.search(pattern, name_clean):
                return category, line_item, confidence

        return default_cat, f"Unclassified ({name})", 0.50
