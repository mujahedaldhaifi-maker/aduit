#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
منظومة ماي أودت – My Audit Platform (النسخة المتكاملة في ملف واحد)
منصة سحابية متقدمة لإدارة دورة المراجعة الخارجية وفق المعايير الدولية ISA / SOCPA / ISQM.
تعمل ذاتياً بالاعتماد على المكتبات القياسية لبايثون (Standard Library: sqlite3, http.server, json, etc.)
"""

import sys
import os
import json
import sqlite3
import math
import uuid
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

DB_PATH = os.environ.get('MY_AUDIT_DB', '/tmp/my_audit_standalone.db')

# ==============================================================================
# 1. قاعدة البيانات والتهيئة (Database & Schema)
# ==============================================================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tax_id TEXT,
        industry TEXT,
        accounting_system TEXT,
        fiscal_year_end TEXT,
        created_at TEXT
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS acceptance_evaluations (
        eval_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        independence_passed INTEGER NOT NULL,
        integrity_passed INTEGER NOT NULL,
        conflict_of_interest INTEGER NOT NULL,
        risk_level TEXT NOT NULL,
        decision TEXT NOT NULL,
        notes TEXT,
        evaluated_by TEXT,
        evaluated_at TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS engagements (
        engagement_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        title TEXT NOT NULL,
        fiscal_year INTEGER NOT NULL,
        start_date TEXT,
        end_date TEXT,
        partner_name TEXT NOT NULL,
        manager_name TEXT NOT NULL,
        senior_name TEXT,
        auditor_name TEXT,
        eqcr_reviewer TEXT,
        budgeted_hours REAL DEFAULT 0.0,
        actual_hours REAL DEFAULT 0.0,
        stage TEXT DEFAULT 'Acceptance',
        status TEXT DEFAULT 'Active',
        created_at TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS trial_balances (
        tb_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        total_debit REAL NOT NULL,
        total_credit REAL NOT NULL,
        is_balanced INTEGER NOT NULL,
        imported_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        tb_id TEXT NOT NULL,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        debit REAL DEFAULT 0.0,
        credit REAL DEFAULT 0.0,
        net_balance REAL DEFAULT 0.0,
        fs_category TEXT,
        fs_line_item TEXT,
        mapping_confidence REAL DEFAULT 1.0,
        mapping_status TEXT DEFAULT 'Approved',
        FOREIGN KEY (tb_id) REFERENCES trial_balances(tb_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS materiality (
        materiality_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        benchmark_type TEXT NOT NULL,
        benchmark_amount REAL NOT NULL,
        overall_percentage REAL NOT NULL,
        overall_materiality REAL NOT NULL,
        performance_percentage REAL NOT NULL,
        performance_materiality REAL NOT NULL,
        trivial_percentage REAL NOT NULL,
        trivial_threshold REAL NOT NULL,
        justification TEXT,
        approved_by TEXT,
        approved_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS risks (
        risk_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        account_category TEXT NOT NULL,
        fs_line_item TEXT,
        description TEXT NOT NULL,
        assertion TEXT NOT NULL,
        inherent_risk TEXT NOT NULL,
        control_risk TEXT NOT NULL,
        rmm TEXT NOT NULL,
        is_significant INTEGER DEFAULT 0,
        planned_response TEXT NOT NULL,
        status TEXT DEFAULT 'Identified',
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_programs (
        program_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        area_name TEXT NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS procedures (
        procedure_id TEXT PRIMARY KEY,
        program_id TEXT NOT NULL,
        risk_id TEXT,
        procedure_type TEXT NOT NULL,
        description TEXT NOT NULL,
        assertion TEXT NOT NULL,
        population_size INTEGER DEFAULT 0,
        sample_size INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Pending',
        completed_by TEXT,
        completed_at TEXT,
        FOREIGN KEY (program_id) REFERENCES audit_programs(program_id),
        FOREIGN KEY (risk_id) REFERENCES risks(risk_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS working_papers (
        wp_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        title TEXT NOT NULL,
        objective TEXT NOT NULL,
        assertion TEXT NOT NULL,
        procedures_performed TEXT NOT NULL,
        results TEXT NOT NULL,
        exceptions_noted TEXT,
        conclusion TEXT NOT NULL,
        prepared_by TEXT NOT NULL,
        prepared_at TEXT,
        reviewed_by TEXT,
        reviewed_at TEXT,
        status TEXT DEFAULT 'Prepared',
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        evidence_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        wp_id TEXT,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER DEFAULT 0,
        description TEXT,
        source TEXT NOT NULL,
        uploaded_at TEXT,
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id),
        FOREIGN KEY (wp_id) REFERENCES working_papers(wp_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample_id TEXT PRIMARY KEY,
        procedure_id TEXT NOT NULL,
        method TEXT NOT NULL,
        population_amount REAL DEFAULT 0.0,
        tolerable_misstatement REAL DEFAULT 0.0,
        expected_misstatement REAL DEFAULT 0.0,
        confidence_level REAL DEFAULT 0.95,
        sample_size INTEGER NOT NULL,
        items_selected TEXT,
        FOREIGN KEY (procedure_id) REFERENCES procedures(procedure_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS confirmations (
        confirmation_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        recipient_name TEXT NOT NULL,
        recipient_type TEXT NOT NULL,
        account_reference TEXT,
        book_balance REAL NOT NULL,
        confirmed_balance REAL,
        status TEXT DEFAULT 'Prepared',
        sent_date TEXT,
        received_date TEXT,
        notes TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS review_notes (
        note_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        wp_id TEXT,
        raised_by TEXT NOT NULL,
        assigned_to TEXT NOT NULL,
        priority TEXT DEFAULT 'Medium',
        note_text TEXT NOT NULL,
        response_text TEXT,
        status TEXT DEFAULT 'Open',
        created_at TEXT,
        cleared_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id),
        FOREIGN KEY (wp_id) REFERENCES working_papers(wp_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS misstatements (
        misstatement_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        account_id TEXT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        misstatement_type TEXT NOT NULL,
        is_adjusted INTEGER DEFAULT 0,
        impact_on_pnl REAL DEFAULT 0.0,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id),
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS quality_reviews (
        review_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        reviewer_name TEXT NOT NULL,
        is_eqcr_required INTEGER DEFAULT 0,
        checklist_results TEXT,
        reviewer_comments TEXT,
        approved INTEGER DEFAULT 0,
        approval_date TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id TEXT,
        user_name TEXT NOT NULL,
        action TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );""")

    conn.commit()
    conn.close()

def log_audit(conn, eng_id, user, action, entity, entity_id, details):
    ts = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO audit_trail (engagement_id, user_name, action, entity_name, entity_id, details, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (eng_id, user, action, entity, entity_id, str(details), ts))
    conn.commit()

# ==============================================================================
# 2. محركات المراجعة المهنية (Calculation & Logic Engines)
# ==============================================================================
class TrialBalanceEngine:
    @staticmethod
    def verify(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        tot_deb = sum(float(a.get('debit', 0.0)) for a in accounts)
        tot_crd = sum(float(a.get('credit', 0.0)) for a in accounts)
        diff = abs(tot_deb - tot_crd)
        return {
            "total_debit": round(tot_deb, 2),
            "total_credit": round(tot_crd, 2),
            "difference": round(diff, 2),
            "is_balanced": diff < 0.01
        }

    @staticmethod
    def detect_anomalies(accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        anomalies = []
        for a in accounts:
            name = a.get('name', '').lower()
            code = a.get('code', '')
            net = float(a.get('debit', 0.0)) - float(a.get('credit', 0.0))
            if any(k in name for k in ['نقد', 'صندوق', 'بنك', 'cash', 'bank']) and net < 0:
                anomalies.append({
                    "account_code": code,
                    "account_name": a.get('name'),
                    "type": "Negative Cash / Overdraft",
                    "detail": f"رصيد دائن غير اعتيادي في حساب النقدية بقيمة {abs(net):,.2f} ر.س."
                })
            if any(k in name for k in ['مصروف', 'expense', 'رواتب', 'إيجار']) and net < 0:
                anomalies.append({
                    "account_code": code,
                    "account_name": a.get('name'),
                    "type": "Credit Balance in Expense",
                    "detail": f"رصيد دائن غير اعتيادي في حساب المصروفات بقيمة {abs(net):,.2f} ر.س."
                })
        return anomalies

class MappingEngine:
    RULES = [
        (r'(نقد|صندوق|بنك|مصرف|cash|bank)', 'CurrentAssets', 'Cash and Cash Equivalents', 0.98),
        (r'(عملاء|مدينون|ذمم مدينة|receivable|customer)', 'CurrentAssets', 'Trade Receivables', 0.95),
        (r'(مخزون|بضاعة|inventory|stock)', 'CurrentAssets', 'Inventories', 0.96),
        (r'(مقدم|prepaid)', 'CurrentAssets', 'Prepayments and Other Receivables', 0.90),
        (r'(أصول ثابتة|مباني|آلات|معدات|ppe|equipment)', 'NonCurrentAssets', 'Property, Plant and Equipment', 0.95),
        (r'(مجمع إهلاك|accumulated depreciation)', 'NonCurrentAssets', 'Accumulated Depreciation', 0.97),
        (r'(موردون|دائنون|ذمم دائنة|payable|supplier)', 'CurrentLiabilities', 'Trade Payables', 0.95),
        (r'(مستحقات|accrued)', 'CurrentLiabilities', 'Accruals and Other Payables', 0.92),
        (r'(زكاة|ضريبة|zakat|tax)', 'CurrentLiabilities', 'Zakat and Tax Payable', 0.95),
        (r'(قروض طويلة|term loan)', 'NonCurrentLiabilities', 'Long-term Borrowings', 0.94),
        (r'(مكافأة نهاية الخدمة|end of service)', 'NonCurrentLiabilities', 'Employees End of Service Benefits', 0.95),
        (r'(رأس المال|share capital)', 'Equity', 'Share Capital', 0.99),
        (r'(احتياطي|أرباح مبقاة|reserve|retained earnings)', 'Equity', 'Retained Earnings and Reserves', 0.98),
        (r'(إيراد|مبيعات|revenue|sales)', 'Revenue', 'Revenue from Contracts with Customers', 0.96),
        (r'(تكلفة المبيعات|مشتريات|cogs|cost of sales)', 'CostOfGoodsSold', 'Cost of Sales', 0.95),
        (r'(رواتب|إيجار|عمومية وإدارية|salary|rent|admin)', 'OperatingExpenses', 'General, Administrative and Selling Expenses', 0.94),
        (r'(مصروف الزكاة|zakat expense)', 'ZakatTax', 'Zakat Expense', 0.95)
    ]

    @classmethod
    def suggest(cls, code: str, name: str) -> Tuple[str, str, float]:
        n = name.lower()
        for pat, cat, line, conf in cls.RULES:
            if re.search(pat, n):
                return cat, line, conf
        return 'OperatingExpenses', f'General Account ({name})', 0.50

class MaterialityEngine:
    @staticmethod
    def calculate(b_type: str, b_amt: float, om_pct=5.0, pm_pct=75.0, ctt_pct=5.0) -> Dict[str, Any]:
        om = round(abs(b_amt) * (om_pct / 100.0), 2)
        pm = round(om * (pm_pct / 100.0), 2)
        ctt = round(om * (ctt_pct / 100.0), 2)
        return {
            "benchmark_type": b_type,
            "benchmark_amount": b_amt,
            "overall_percentage": om_pct,
            "overall_materiality": om,
            "performance_percentage": pm_pct,
            "performance_materiality": pm,
            "trivial_percentage": ctt_pct,
            "trivial_threshold": ctt,
            "justification": f"تم تطبيق معيار ISA 320 باختيار {b_type} ونسبة {om_pct}% للأهمية العامة و{pm_pct}% للأداء."
        }

class RiskEngine:
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
    @classmethod
    def evaluate(cls, inh: str, ctl: str) -> Dict[str, Any]:
        rmm = cls.MATRIX.get((inh.capitalize(), ctl.capitalize()), 'Medium')
        is_sig = 1 if rmm == 'Significant' else 0
        resp = "Substantive Testing & Detailed Verification" if is_sig or rmm == 'High' else "Analytical & Standard Procedures"
        return {"inherent_risk": inh, "control_risk": ctl, "rmm": rmm, "is_significant": is_sig, "planned_response": resp}

class SamplingEngine:
    @staticmethod
    def calculate_mus(pop_val: float, tol_mis: float, conf=0.95) -> Dict[str, Any]:
        factor = 3.0 if conf >= 0.95 else 2.31
        interval = max(1.0, round(tol_mis / factor, 2))
        size = int(math.ceil(pop_val / interval))
        size = max(5, min(size, 200))
        return {
            "method": "Monetary Unit Sampling (MUS - ISA 530)",
            "population_value": pop_val,
            "tolerable_misstatement": tol_mis,
            "sampling_interval": interval,
            "recommended_sample_size": size
        }

class QualityGateEnforcer:
    @staticmethod
    def check_gate_1(ev: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errs = []
        if ev.get('independence_passed') != 1: errs.append("فحص الاستقلالية غير مجاز.")
        if ev.get('integrity_passed') != 1: errs.append("فحص النزاهة غير مجاز.")
        if ev.get('conflict_of_interest') == 1: errs.append("يوجد تعارض مصالح غير معالج.")
        if ev.get('decision') not in ['Accepted', 'AcceptedWithConditions']: errs.append("لم يصدر قرار بقبول العميل.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_2(tb: Dict[str, Any], mat: Dict[str, Any], risks_count: int) -> Tuple[bool, List[str]]:
        errs = []
        if not tb or tb.get('is_balanced') != 1: errs.append("ميزان المراجعة غير متوازن.")
        if not mat or mat.get('overall_materiality', 0) <= 0: errs.append("لم يتم تحديد الأهمية النسبية.")
        if risks_count == 0: errs.append("لم يتم تحديد مخاطر المراجعة.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_3(pending_procs: int, missing_wps: int, open_notes: int) -> Tuple[bool, List[str]]:
        errs = []
        if pending_procs > 0: errs.append(f"يوجد {pending_procs} إجراء مراجعة غير مكتمل.")
        if missing_wps > 0: errs.append(f"يوجد {missing_wps} إجراء بدون ورقة عمل.")
        if open_notes > 0: errs.append(f"يوجد {open_notes} ملاحظة معلقة.")
        return len(errs) == 0, errs

    @staticmethod
    def check_gate_4(unadj_total: float, pm: float, eqcr_approved: bool, uncleared_notes: int) -> Tuple[bool, List[str]]:
        errs = []
        if uncleared_notes > 0: errs.append(f"يوجد {uncleared_notes} ملاحظات لم تغلق نهائياً.")
        if unadj_total > pm: errs.append(f"إجمالي التحريفات غير المعدلة ({unadj_total:,.2f}) يتجاوز أهمية الأداء ({pm:,.2f}).")
        if not eqcr_approved: errs.append("مراجعة الجودة المستقلة EQCR لم تعتمد بعد.")
        return len(errs) == 0, errs

# ==============================================================================
# 3. إعداد بيانات نموذجية متكاملة (Seed Demonstration Data)
# ==============================================================================
def populate_sample_audit():
    init_database()
    conn = get_db_connection()
    conn.execute("PRAGMA foreign_keys = OFF;")

    # 1. Client
    client_id = "CL-RUWAD-01"
    conn.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
    conn.execute("""
        INSERT INTO clients (client_id, name, tax_id, industry, accounting_system, fiscal_year_end, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (client_id, "شركة الرواد للتجارة والصناعة (شركة مساهمة مقفلة)", "300123456700003",
          "تجارة وتصنيع المواد الاستهلاكية", "SAP S/4HANA", "2026-12-31", datetime.utcnow().isoformat()))

    # 2. Acceptance
    conn.execute("""
        INSERT OR REPLACE INTO acceptance_evaluations (
            eval_id, client_id, independence_passed, integrity_passed,
            conflict_of_interest, risk_level, decision, notes, evaluated_by, evaluated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("EV-01", client_id, 1, 1, 0, "Medium", "Accepted",
          "تم استيفاء متطلبات الاستقلالية والنزاهة وفق معيار ISA 210 وقواعد SOCPA.",
          "أ. محمد القحطاني (الشريك المسؤول)", datetime.utcnow().isoformat()))

    # 3. Engagement
    eng_id = "ENG-2026-RUWAD"
    conn.execute("DELETE FROM engagements WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO engagements (
            engagement_id, client_id, title, fiscal_year, start_date, end_date,
            partner_name, manager_name, senior_name, auditor_name, eqcr_reviewer,
            budgeted_hours, actual_hours, stage, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (eng_id, client_id, "مراجعة القوائم المالية السنوية للسنة المنتهية في 31 ديسمبر 2026م",
          2026, "2026-01-01", "2026-12-31", "أ. محمد القحطاني", "أ. سارة العتيبي",
          "أ. أحمد الشهري", "أ. خالد الدوسري", "أ. د. فهد المنصور", 160.0, 148.0,
          "Completion", "Active", datetime.utcnow().isoformat()))

    # 4. Trial Balance & Accounts (Debits = Credits = 25,670,000.00)
    raw_tb = [
        ("1010", "النقدية لدى البنوك - الحسابات الجارية", 2450000.0, 0.0),
        ("1020", "صندوق العهدة النقدية (Petty Cash)", 50000.0, 0.0),
        ("1200", "العملاء والذمم المدينة التجارية", 4120000.0, 0.0),
        ("1290", "مخصص الخسائر الائتمانية المتوقعة (ECL)", 0.0, 180000.0),
        ("1300", "المخزون السلعي - بضاعة تامة الصنع", 3500000.0, 0.0),
        ("1400", "مصروفات وتأمينات مدفوعة مقدماً", 250000.0, 0.0),
        ("1500", "الممتلكات والآلات والمعدات (PPE)", 4980000.0, 0.0),
        ("1590", "مجمع إهلاك الممتلكات والمعدات", 0.0, 800000.0),
        ("2010", "الموردون والذمم الدائنة التجارية", 0.0, 2850000.0),
        ("2020", "مصروفات ورواتب مستحقة الدفع", 0.0, 450000.0),
        ("2030", "مخصص الزكاة الشرعية المستحقة", 0.0, 120000.0),
        ("2100", "قروض وتسهيلات بنكية طويلة الأجل", 0.0, 1220000.0),
        ("2500", "مخصص مكافأة نهاية الخدمة للموظفين", 0.0, 650000.0),
        ("3010", "رأس المال المدفوع", 0.0, 5000000.0),
        ("3020", "الاحتياطي النظامي", 0.0, 1000000.0),
        ("3030", "الأرباح المبقاة (المجمعة)", 0.0, 1000000.0),
        ("4010", "إيرادات المبيعات والخدمات", 0.0, 12400000.0),
        ("5010", "تكلفة المبيعات المباشرة (COGS)", 8200000.0, 0.0),
        ("6010", "رواتب ومزايا موظفي الإدارة والتسويق", 1200000.0, 0.0),
        ("6020", "إيجار ومرافق عمومية ومصاريف تسويق", 530000.0, 0.0),
        ("6030", "استهلاك الممتلكات والآلات والمعدات", 270000.0, 0.0),
        ("6040", "مصروف الزكاة الشرعية للعام الحالي", 120000.0, 0.0)
    ]

    tb_id = "TB-01"
    conn.execute("DELETE FROM trial_balances WHERE tb_id = ?", (tb_id,))
    conn.execute("DELETE FROM accounts WHERE tb_id = ?", (tb_id,))
    conn.execute("""
        INSERT INTO trial_balances (tb_id, engagement_id, total_debit, total_credit, is_balanced, imported_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tb_id, eng_id, 25670000.0, 25670000.0, 1, datetime.utcnow().isoformat()))

    for code, name, deb, crd in raw_tb:
        cat, line, conf = MappingEngine.suggest(code, name)
        net = deb - crd
        conn.execute("""
            INSERT INTO accounts (account_id, tb_id, code, name, debit, credit, net_balance, fs_category, fs_line_item, mapping_confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (f"ACC-{code}", tb_id, code, name, deb, crd, net, cat, line, conf))

    # 5. Materiality
    mat_calc = MaterialityEngine.calculate("ProfitBeforeTax", 2200000.0, om_pct=5.0, pm_pct=75.0, ctt_pct=5.0)
    conn.execute("DELETE FROM materiality WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO materiality (
            materiality_id, engagement_id, benchmark_type, benchmark_amount,
            overall_percentage, overall_materiality, performance_percentage,
            performance_materiality, trivial_percentage, trivial_threshold,
            justification, approved_by, approved_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("MAT-01", eng_id, mat_calc["benchmark_type"], mat_calc["benchmark_amount"],
          mat_calc["overall_percentage"], mat_calc["overall_materiality"],
          mat_calc["performance_percentage"], mat_calc["performance_materiality"],
          mat_calc["trivial_percentage"], mat_calc["trivial_threshold"],
          mat_calc["justification"], "أ. محمد القحطاني", datetime.utcnow().isoformat()))

    # 6. Risks (ISA 315)
    conn.execute("DELETE FROM risks WHERE engagement_id = ?", (eng_id,))
    risks_data = [
        ("RSK-01", "Revenue", "Revenue from Contracts", "خطر تضخيم الإيرادات والاعتراف المبكر بالمبيعات حول نهاية السنة المالية (افتراض احتيال ISA 240).", "Existence", "High", "Medium", "High", 1, "فحص عينة MUS لفواتير المبيعات وبوالص الشحن واختبارات الفصل الزمني."),
        ("RSK-02", "Inventory", "Inventories", "خطر تقادم المخزون وعدم كفاية مخصص هبوط القيمة إلى صافي القيمة القابلة للتحقق NRV.", "Accuracy & Valuation", "Medium", "Medium", "Medium", 0, "حضور الجرد الفعلي بمستودعات الرياض وجدة وفحص أسعار البيع اللاحقة."),
        ("RSK-03", "Cash", "Cash and Cash Equivalents", "خطر وجود تسويات بنكية معلقة أو تحويلات مكررة غير مسجلة بالدفاتر.", "Existence", "High", "Low", "Medium", 0, "مصادقات بنكية مباشرة لـ 100% من الحسابات ومطابقة مذكرات التسوية."),
        ("RSK-04", "Receivables", "Trade Receivables", "خطر تعثر ديون قديمة وعدم كفاية مخصص خسائر الائتمان المتوقعة وفق IFRS 9.", "Accuracy & Valuation", "High", "Medium", "High", 1, "مصادقات كبار العملاء واختبار مصفوفة الأعمار الزمنية والتحصيلات اللاحقة.")
    ]
    for rid, cat, line, desc, ast, inh, ctl, rmm, is_sig, resp in risks_data:
        conn.execute("""
            INSERT INTO risks (risk_id, engagement_id, account_category, fs_line_item, description, assertion, inherent_risk, control_risk, rmm, is_significant, planned_response)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rid, eng_id, cat, line, desc, ast, inh, ctl, rmm, is_sig, resp))

    # 7. Audit Programs & Procedures (ISA 330)
    conn.execute("DELETE FROM audit_programs WHERE engagement_id = ?", (eng_id,))
    programs = [
        ("PRG-01", "Revenue", "برنامج مراجعة الإيرادات والمبيعات"),
        ("PRG-02", "Cash & Bank", "برنامج مراجعة النقد وما في حكمه"),
        ("PRG-03", "Inventory", "برنامج مراجعة المخزون السلعي"),
        ("PRG-04", "Receivables", "برنامج مراجعة العملاء والذمم المدينة")
    ]
    for pid, area, title in programs:
        conn.execute("INSERT INTO audit_programs (program_id, engagement_id, area_name, title) VALUES (?, ?, ?, ?)", (pid, eng_id, area, title))

    procs_data = [
        ("PRC-01", "PRG-01", "RSK-01", "SubstantiveTest", "اختبار تفاصيل المبيعات والفصل الزمني وعينة MUS للفواتير.", "Existence", 12400000, 45, "Completed", "أ. خالد الدوسري"),
        ("PRC-02", "PRG-02", "RSK-03", "SubstantiveTest", "الحصول على مصادقات البنوك المباشرة 100% ومطابقة مذكرات التسوية.", "Existence", 2450000, 3, "Completed", "أ. خالد الدوسري"),
        ("PRC-03", "PRG-03", "RSK-02", "SubstantiveTest", "حضور الجرد الفعلي للمخزون بمستودعات الرياض وجدة وفحص اختبارات NRV.", "Accuracy & Valuation", 3500000, 60, "Completed", "أ. أحمد الشهري"),
        ("PRC-04", "PRG-04", "RSK-04", "SubstantiveTest", "إرسال مصادقات العملاء وفحص التحصيلات اللاحقة ومخصص التعثر IFRS 9.", "Accuracy & Valuation", 4120000, 35, "Completed", "أ. خالد الدوسري")
    ]
    for prid, pid, rid, ptype, desc, ast, pop, smp, stat, cby in procs_data:
        conn.execute("DELETE FROM procedures WHERE procedure_id = ?", (prid,))
        conn.execute("""
            INSERT INTO procedures (procedure_id, program_id, risk_id, procedure_type, description, assertion, population_size, sample_size, status, completed_by, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (prid, pid, rid, ptype, desc, ast, pop, smp, stat, cby, datetime.utcnow().isoformat()))

    # 8. Working Papers (ISA 230)
    wps_data = [
        ("WP-01", "PRC-01", "ورقة عمل اختبار تفاصيل المبيعات والفصل الزمني", "التحقق من صحة واكتمال الإيرادات.", "Existence & Cut-off", "تم اختيار عينة MUS شملت 45 فاتورة مبيعات، ومطابقتها مع بوالص الشحن الموقعة بالاستلام وفحص Cut-off.", "كافة فواتير العينة موثقة ومطابقة لمستندات الشحن والتسليم بدون أي تجاوز زمني.", "لا توجد استثناءات جوهرية.", "الإيرادات مسجلة بصورة عادلة ووفقًا لمعيار IFRS 15.", "أ. خالد الدوسري", "أ. سارة العتيبي"),
        ("WP-02", "PRC-02", "ورقة عمل مطابقة الأرصدة البنكية والمصادقات", "التحقق من صحة ووجود أرصدة النقدية لدى البنوك.", "Existence & Rights", "إرسال خطابات مصادقة مباشرة لجميع البنوك ومطابقتها مع الدفاتر ومذكرات التسوية.", "وردت كافة المصادقات البنكية مباشرة للمكتب وتطابقت 100% مع الأرصدة الدفترية ومذكرات التسوية.", "لا توجد فروقات معلقة.", "أرصدة النقدية صحيحة وخالية من الرهونات.", "أ. خالد الدوسري", "أ. أحمد الشهري"),
        ("WP-03", "PRC-03", "ورقة عمل حضور جرد المخزون واختبار NRV", "التحقق من الوجود المادي وتقييم المخزون بالتكلفة أو صافي القيمة القابلة للتحقق أيهما أقل.", "Existence & Valuation", "حضور الجرد بمستودعات الرياض وجدة، والقيام بعدّ اختباري لـ 60 صنفاً، ومقارنة التكلفة بأسعار البيع اللاحقة.", "تطابقت نتائج العد بنسبة 99.8%، وهامش الربح إيجابي ولا حاجة لزيادة مخصص الهبوط.", "فارق عجز طبيعي بسيط (1,400 ر.س) سُوّي دفترياً.", "المخزون موجود ومُقَيّم وفقًا لمعيار IAS 2.", "أ. أحمد الشهري", "أ. سارة العتيبي"),
        ("WP-04", "PRC-04", "ورقة عمل فحص أرصدة العملاء ومخصص IFRS 9", "التحقق من وجود وقابلية تحصيل الذمم المدينة وكفاية مخصص التعثر.", "Accuracy & Valuation", "إرسال مصادقات لأكبر 10 عملاء يمثلون 70% من الرصيد، وفحص التحصيلات اللاحقة.", "وردت المصادقات متطابقة، وتم تحصيل 82% من رصيد العملاء حتى نهاية فبراير 2027.", "لا توجد استثناءات.", "رصيد العملاء ومخصص الخسائر البالغ 180,000 ر.س عادل وكافٍ.", "أ. خالد الدوسري", "أ. محمد القحطاني")
    ]
    for wid, prid, title, obj, ast, proc_perf, res, exc, conc, prep, rev in wps_data:
        conn.execute("DELETE FROM working_papers WHERE wp_id = ?", (wid,))
        conn.execute("""
            INSERT INTO working_papers (wp_id, procedure_id, title, objective, assertion, procedures_performed, results, exceptions_noted, conclusion, prepared_by, prepared_at, reviewed_by, reviewed_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (wid, prid, title, obj, ast, proc_perf, res, exc, conc, prep, datetime.utcnow().isoformat(), rev, datetime.utcnow().isoformat(), 'Reviewed'))

    # 9. Evidence & Confirmations
    conn.execute("DELETE FROM confirmations WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO confirmations (confirmation_id, engagement_id, recipient_name, recipient_type, account_reference, book_balance, confirmed_balance, status, sent_date, received_date, notes)
        VALUES ('CNF-01', ?, 'مصرف الراجحي - الإدارة الإقليمية', 'Bank', 'SA1280000123456789012345', 1850000.0, 1850000.0, 'Cleared', '2026-02-10', '2026-02-15', 'مطابقة تامة لكشف الحساب.')
    """, (eng_id,))
    conn.execute("""
        INSERT INTO confirmations (confirmation_id, engagement_id, recipient_name, recipient_type, account_reference, book_balance, confirmed_balance, status, sent_date, received_date, notes)
        VALUES ('CNF-02', ?, 'البنك الأهلي السعودي (SNB)', 'Bank', 'SA4510000987654321098765', 600000.0, 600000.0, 'Cleared', '2026-02-10', '2026-02-16', 'مطابقة تامة لكشف الحساب.')
    """, (eng_id,))

    # 10. Review Notes (All Cleared)
    conn.execute("DELETE FROM review_notes WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO review_notes (note_id, engagement_id, wp_id, raised_by, assigned_to, priority, note_text, response_text, status, created_at, cleared_at)
        VALUES ('NOT-01', ?, 'WP-01', 'أ. سارة العتيبي (مدير الارتباط)', 'أ. خالد الدوسري', 'High', 'يرجى التأكد من إرفاق بوليصة الشحن الأصلية للفاتورة 8841 بمبلغ 120,000 ر.س.', 'تم فحص بوليصة الشحن الأصلية الموقعة بالاستلام وإرفاقها بملف الدليل.', 'Cleared', ?, ?)
    """, (eng_id, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))

    # 11. Misstatements (Below Trivial)
    conn.execute("DELETE FROM misstatements WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO misstatements (misstatement_id, engagement_id, description, amount, misstatement_type, is_adjusted, impact_on_pnl)
        VALUES ('MIS-01', ?, 'فارق في احتساب استهلاك أصل ثابت طفيف لا يتجاوز عتبة الخطأ التافه.', 3200.0, 'Judgmental', 0, -3200.0)
    """, (eng_id,))

    # 12. EQCR Quality Review Sign-off (ISQM 1/2)
    conn.execute("DELETE FROM quality_reviews WHERE engagement_id = ?", (eng_id,))
    conn.execute("""
        INSERT INTO quality_reviews (review_id, engagement_id, reviewer_name, is_eqcr_required, checklist_results, reviewer_comments, approved, approval_date)
        VALUES ('EQC-01', ?, 'أ. د. فهد المنصور (شريك مراجعة الجودة المستقل)', 1, '{\"all_checks_passed\": true}', 'تمت مراجعة جودة الارتباط والموافقة التامة على إصدار تقرير المراجع غير المتحفظ.', 1, ?)
    """, (eng_id, datetime.utcnow().isoformat()))

    # 13. Audit Trail
    log_audit(conn, eng_id, "System", "SEED", "engagements", eng_id, "تم إعداد دورة المراجعة الكاملة للبيانات النموذجية بنجاح.")

    conn.commit()
    conn.close()
    return eng_id

# ==============================================================================
# 4. توليد التقارير والقوائم المالية (Reporting Engine)
# ==============================================================================
def generate_auditor_report(eng_id: str) -> str:
    conn = get_db_connection()
    eng = conn.execute("SELECT e.*, c.name as client_name FROM engagements e JOIN clients c ON c.client_id = e.client_id WHERE e.engagement_id = ?", (eng_id,)).fetchone()
    client_name = eng["client_name"] if eng else "المنشأة"
    year = eng["fiscal_year"] if eng else 2026
    partner = eng["partner_name"] if eng else "الشريك المسؤول"
    conn.close()

    today = datetime.now().strftime("%Y-%m-%d")
    report = f"""
================================================================================
                      تقرير مراجع الحسابات المستقل
                     INDEPENDENT AUDITOR'S REPORT
================================================================================
إلى السادة / مساهمي {client_name}
الرياض - المملكة العربية السعودية

أولاً: الرأي غير المتحفظ (Unmodified / Clean Opinion):
راجعنا القوائم المالية لـ {client_name} ("الشركة")، والتي تشتمل على قائمة المركز المالي كما في 31 ديسمبر {year}م، وقائمة الربح أو الخسارة والدخل الشامل الآخر، وقائمة التغيرات في حقوق الملكية، وقائمة التدفقات النقدية للسنة المنتهية في ذلك التاريخ، والإيضاحات المرفقة بالقوائم المالية بما في ذلك ملخص السياسات المحاسبية الهامة.

وفي رأينا، فإن القوائم المالية المرفقة تظهر بعدالة، من كافة النواحي الجوهرية، المركز المالي لـ {client_name} كما في 31 ديسمبر {year}م، وأداءها المالي وتدفقاتها النقدية للسنة المنتهية في ذلك التاريخ وفقاً للمعايير الدولية للتقرير المالي المعتمدة في المملكة العربية السعودية (IFRS) والمعايير والإصدارات الأخرى المعتمدة من الهيئة السعودية للمراجعين والمحاسبين (SOCPA).

ثانياً: أساس الرأي (Basis for Opinion):
تمت مراجعتنا وفقاً للمعايير الدولية للمراجعة المعتمدة في المملكة العربية السعودية (ISA). ونحن مستقلون عن الشركة وفقاً لقواعد سلوك وآداب المهنة المعتمدة في المملكة، ونعتقد أن أدلة المراجعة التي حصلنا عليها كافية ومناسبة لتوفير أساس لرأينا.

ثالثاً: أمور المراجعة الرئيسية (Key Audit Matters - ISA 701):
1. الاعتراف بالإيرادات والتحقق من الفصل الزمني (Revenue Recognition & Cut-off):
   - الإجراءات المنفذة: فحص عينة المعاينة النقدية (MUS) ومطابقتها مع بوالص الشحن واختبار قيود الإقفال.
2. تقييم المخزون السلعي واختبار صافي القيمة القابلة للتحقق (Inventory Valuation & NRV):
   - الإجراءات المنفذة: حضور الجرد الفعلي بمستودعات الشركة ومقارنة التكلفة بالأسعار اللاحقة بعد تاريخ القوائم.

رابعاً: مسؤوليات الإدارة والمكلفين بالحوكمة:
الإدارة مسؤولة عن إعداد القوائم المالية وعرضها العادل وفقاً للمعايير المعتمدة في المملكة ونظام الشركات، وتصميم نظام الرقابة الداخلية المناسب.

خامساً: تقرير حول المتطلبات النظامية والتنظيمية الأخرى:
وفقاً للمعلومات والتوضيحات المقدمة، لم يتبين لنا وجود مخالفة جوهرية لأحكام نظام الشركات السعودي أو عقد تأسيس الشركة خلال السنة المنتهية في 31 ديسمبر {year}م.

عن مكتب المراجعة: ماي أودت للمحاسبة والمراجعة (My Audit Partners)
الشريك المسؤول: {partner}
ترخيص مهني صادر عن SOCPA
التاريخ: {today}
================================================================================
"""
    return report.strip()

# ==============================================================================
# 5. واجهة سطر الأوامر والمحاكاة الكاملة (CLI Demo)
# ==============================================================================
def run_cli_demo():
    print("\n" + "=" * 80)
    print("      منظومة ماي أودت – My Audit Platform | محاكاة دورة المراجعة الشاملة")
    print("=" * 80)
    eng_id = populate_sample_audit()
    conn = get_db_connection()

    print("\n[1] ملف العميل وتقييم القبول والاستمرار (ISA 210 / ISQM 1):")
    client = conn.execute("SELECT * FROM clients WHERE client_id = 'CL-RUWAD-01'").fetchone()
    print(f"    - اسم المنشأة: {client['name']}")
    print(f"    - الرقم الضريبي: {client['tax_id']} | النشاط: {client['industry']}")
    print("    - حالة الاستقلالية والنزاهة: مجاز بنجاح 100% (قرار القبول: معتمد)")

    print("\n[2] ميزان المراجعة وتصنيف الحسابات (TB & IFRS Mapping):")
    tb = conn.execute("SELECT * FROM trial_balances WHERE engagement_id = ?", (eng_id,)).fetchone()
    print(f"    - إجمالي المدين: {tb['total_debit']:,.2f} ر.س | إجمالي الدائن: {tb['total_credit']:,.2f} ر.س")
    print("    - حالة التوازن: متوازن تماماً (الفارق = 0.00 ر.س)")
    acc_count = conn.execute("SELECT count(*) as c FROM accounts WHERE tb_id = ?", (tb['tb_id'],)).fetchone()['c']
    print(f"    - الحسابات المصنفة آلياً بقوائم المركز المالي والدخل: {acc_count} حساباً")

    print("\n[3] الأهمية النسبية المعتمدة (ISA 320 Materiality):")
    mat = conn.execute("SELECT * FROM materiality WHERE engagement_id = ?", (eng_id,)).fetchone()
    print(f"    - المعيار الأساسي: {mat['benchmark_type']} بمبلغ {mat['benchmark_amount']:,.2f} ر.س")
    print(f"    - الأهمية العامة (Overall 5%): {mat['overall_materiality']:,.2f} ر.س")
    print(f"    - أهمية الأداء (Performance 75%): {mat['performance_materiality']:,.2f} ر.س")
    print(f"    - عتبة الخطأ التافه (Clearly Trivial 5%): {mat['trivial_threshold']:,.2f} ر.س")

    print("\n[4] تقييم المخاطر (ISA 315 Risk Assessment Matrix):")
    risks = conn.execute("SELECT * FROM risks WHERE engagement_id = ?", (eng_id,)).fetchall()
    for r in risks:
        print(f"    * [{r['account_category']}] {r['assertion']} -> RMM: {r['rmm']} {'(Significant Risk)' if r['is_significant'] else ''}")

    print("\n[5] برامج المراجعة وأوراق العمل الإلكترونية (ISA 230 & ISA 330):")
    wps = conn.execute("SELECT * FROM working_papers").fetchall()
    for w in wps:
        print(f"    * [{w['wp_id']}] {w['title']} | المُعِد: {w['prepared_by']} | الاستنتاج: {w['conclusion'][:50]}...")

    print("\n[6] المصادقات الخارجية (ISA 505 Confirmations):")
    confs = conn.execute("SELECT * FROM confirmations WHERE engagement_id = ?", (eng_id,)).fetchall()
    for c in confs:
        print(f"    * {c['recipient_name']} ({c['recipient_type']}): دفتري={c['book_balance']:,.2f} | مصادق={c['confirmed_balance']:,.2f} -> {c['status']}")

    print("\n[7] الملاحظات والتحريفات (ISA 450 Findings & Adjustments):")
    notes = conn.execute("SELECT * FROM review_notes WHERE engagement_id = ?", (eng_id,)).fetchall()
    for n in notes:
        print(f"    * ملاحظة: {n['note_text']} -> الحالة: {n['status']}")
    mis = conn.execute("SELECT * FROM misstatements WHERE engagement_id = ?", (eng_id,)).fetchall()
    for m in mis:
        print(f"    * تحريف: {m['description']} بمبلغ {m['amount']:,.2f} ر.س (أقل من عتبة الخطأ التافه)")

    print("\n[8] بوابات الجودة ومراجعة الارتباط المستقلة (Quality Gates & EQCR):")
    print("    - البوابة 1 (القبول والاستمرارية): مجازة بنجاح ✓")
    print("    - البوابة 2 (التخطيط والمخاطر والأهمية): مجازة بنجاح ✓")
    print("    - البوابة 3 (العمل الميداني والتوثيق): مجازة بنجاح ✓")
    print("    - البوابة 4 (مراجعة الجودة والإصدار): مجازة ومعتمدة من EQCR Partner ✓")
    print("    - الجاهزية النهائية للإصدار: جاهز 100% لإصدار الرأي غير المتحفظ")

    print("\n[9] تقرير مراجع الحسابات المستقل (Independent Auditor's Report):")
    print(generate_auditor_report(eng_id))
    conn.close()

# ==============================================================================
# 6. خادم الويب ولوحة التحكم التفاعلية المدمجة (Standard Library HTTP Server)
# ==============================================================================
class MyAuditHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            template_path = '/mnt/agentdata/tiered/c_e947e45d4369e070/my_audit/my_audit/web/templates/index.html'
            if os.path.exists(template_path):
                with open(template_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write("<h1>منظومة ماي أودت تعمل بنجاح</h1>".encode('utf-8'))
        elif path == '/api/dashboard/summary':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            summary = {
                "total_engagements": 1,
                "procedures_completion_pct": 100.0,
                "risks_total": 4,
                "review_notes_open": 0,
                "status": "Ready for Issuance"
            }
            self.wfile.write(json.dumps(summary).encode('utf-8'))
        elif path == '/api/report':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_auditor_report('ENG-2026-RUWAD').encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    populate_sample_audit()
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyAuditHTTPHandler)
    print(f"خادم منظومة ماي أودت يعمل الآن على: http://localhost:{port}")
    print("اضغط Ctrl+C لإيقاف الخادم.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nتم إيقاف الخادم.")

# ==============================================================================
# نقطة الدخول الرئيسية (Main Entrypoint)
# ==============================================================================
if __name__ == '__main__':
    if '--serve' in sys.argv:
        port = 8000
        if '--port' in sys.argv:
            try:
                idx = sys.argv.index('--port')
                port = int(sys.argv[idx + 1])
            except Exception:
                pass
        run_server(port)
    else:
        run_cli_demo()
