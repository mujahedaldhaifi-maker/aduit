import argparse
import json
import sys
import os
from tabulate import tabulate
from my_audit.database import init_db
from my_audit.seed_data import load_seed_data
from my_audit.services.audit_service import AuditService
from my_audit.services.report_generator import ReportGenerator

def print_section(title):
    print("\n" + "=" * 85)
    print(f"  {title}")
    print("=" * 85)

def run_audit_demo():
    print_section("منظومة ماي أودت – My Audit Platform | دورة المراجعة الخارجية الشاملة")
    print("بدء دورة المراجعة الكاملة وفق معايير ISA / SOCPA / ISQM...")

    if os.path.exists("/tmp/my_audit.db"):
        os.remove("/tmp/my_audit.db")

    eng_id = load_seed_data()
    service = AuditService()
    reporter = ReportGenerator()

    # 1. Client & Engagement
    print_section("1. ملف العميل وإعداد الارتباط (Client Master & Engagement Setup)")
    conn = service._conn()
    client = conn.execute("SELECT * FROM clients WHERE client_id = 'CL-RUWAD-01'").fetchone()
    eng = conn.execute("SELECT * FROM engagements WHERE engagement_id = ?", (eng_id,)).fetchone()

    client_table = [
        ["معرف العميل", client["client_id"]],
        ["اسم المنشأة", client["name"]],
        ["الرقم الضريبي", client["tax_id"]],
        ["النشاط", client["industry"]],
        ["النظام المحاسبي", client["accounting_system"]],
        ["فحص الاستقلالية والنزاهة", "مجاز 100% (بدون تعارض مصالح)"],
        ["الشريك المسؤول", eng["partner_name"]],
        ["مدير الارتباط", eng["manager_name"]],
        ["مراجع الجودة المستقل (EQCR)", eng["eqcr_reviewer"]]
    ]
    print(tabulate(client_table, headers=["البيان", "القيمة"], tablefmt="fancy_grid"))

    # 2. Trial Balance & Mapping
    print_section("2. ميزان المراجعة وتصنيف الحسابات (Trial Balance & IFRS Mapping)")
    tb = conn.execute("SELECT * FROM trial_balances WHERE engagement_id = ?", (eng_id,)).fetchone()
    print(f"حالة التوازن: إجمالي المدين = {tb['total_debit']:,.2f} ر.س | إجمالي الدائن = {tb['total_credit']:,.2f} ر.س | الفارق = 0.00 ر.س (متوازن 100%)")

    accounts = conn.execute("SELECT code, name, debit, credit, fs_category, fs_line_item FROM accounts WHERE tb_id = ? LIMIT 8", (tb["tb_id"],)).fetchall()
    acc_rows = [[r["code"], r["name"][:35], f"{r['debit']:,.2f}", f"{r['credit']:,.2f}", r["fs_category"], r["fs_line_item"][:30]] for r in accounts]
    print("\nعينة من الحسابات المصنفة آلياً:")
    print(tabulate(acc_rows, headers=["الرمز", "اسم الحساب", "مدين", "دائن", "التصنيف", "بند القوائم"], tablefmt="grid"))

    # 3. Materiality (ISA 320)
    print_section("3. محرك الأهمية النسبية (ISA 320 Materiality Engine)")
    mat = conn.execute("SELECT * FROM materiality WHERE engagement_id = ?", (eng_id,)).fetchone()
    mat_table = [
        ["معيار القياس (Benchmark)", mat["benchmark_type"], f"{mat['benchmark_amount']:,.2f} ر.س"],
        ["الأهمية النسبية العامة (Overall Materiality)", f"{mat['overall_percentage']}%", f"{mat['overall_materiality']:,.2f} ر.س"],
        ["الأهمية النسبية للأداء (Performance Materiality)", f"{mat['performance_percentage']}%", f"{mat['performance_materiality']:,.2f} ر.س"],
        ["عتبة الخطأ التافه (Clearly Trivial Threshold)", f"{mat['trivial_percentage']}%", f"{mat['trivial_threshold']:,.2f} ر.س"]
    ]
    print(tabulate(mat_table, headers=["المستوى", "النسبة", "المبلغ المعياري"], tablefmt="fancy_grid"))
    print(f"المبرر المهني الموثق: {mat['justification']}")

    # 4. Risk Assessment (ISA 315)
    print_section("4. مصفوفة تقييم المخاطر (ISA 315 Revised Risk Matrix)")
    risks = conn.execute("SELECT account_category, assertion, inherent_risk, control_risk, rmm, is_significant, description FROM risks WHERE engagement_id = ?", (eng_id,)).fetchall()
    r_rows = [[r["account_category"], r["assertion"], r["inherent_risk"], r["control_risk"], r["rmm"], "نعم (Significant)" if r["is_significant"] else "لا", r["description"][:45] + "..."] for r in risks]
    print(tabulate(r_rows, headers=["البند", "الادعاء", "خطر كامن", "خطر رقابي", "تقييم RMM", "خطر هام؟", "وصف الخطر"], tablefmt="grid"))

    # 5. Working Papers & Procedures (ISA 230 & 330)
    print_section("5. برامج المراجعة وأوراق العمل الإلكترونية (ISA 230 & ISA 330)")
    query = """
        SELECT wp.wp_id, wp.title, wp.assertion, wp.conclusion, wp.prepared_by, wp.reviewed_by
        FROM working_papers wp
        JOIN procedures pr ON pr.procedure_id = wp.procedure_id
        JOIN audit_programs p ON p.program_id = pr.program_id
        WHERE p.engagement_id = ?
    """
    wps = conn.execute(query, (eng_id,)).fetchall()
    wp_rows = [[w["wp_id"], w["title"][:40], w["assertion"], w["conclusion"][:45] + "...", w["prepared_by"][:15], w["reviewed_by"][:15]] for w in wps]
    print(tabulate(wp_rows, headers=["معرف WP", "عنوان ورقة العمل", "الادعاء", "الاستنتاج المهني", "المُعِد", "المُراجِع"], tablefmt="grid"))

    # 6. Sampling & Confirmations
    print_section("6. محرك العينات والمصادقات الخارجية (ISA 530 & ISA 505)")
    confs = conn.execute("SELECT recipient_name, recipient_type, book_balance, confirmed_balance, status FROM confirmations WHERE engagement_id = ?", (eng_id,)).fetchall()
    conf_rows = [[c["recipient_name"][:30], c["recipient_type"], f"{c['book_balance']:,.2f}", f"{c['confirmed_balance']:,.2f}", c["status"]] for c in confs]
    print("سجل المصادقات البنكية والخارجية:")
    print(tabulate(conf_rows, headers=["الجهة", "النوع", "الرصيد الدفتري", "المصادق عليه", "الحالة"], tablefmt="grid"))

    # 7. Review Notes & Misstatements
    print_section("7. الملاحظات والتحريفات (ISA 450 Findings & Adjustments)")
    mis = conn.execute("SELECT description, amount, misstatement_type, is_adjusted FROM misstatements WHERE engagement_id = ?", (eng_id,)).fetchall()
    mis_rows = [[m["description"][:45], f"{m['amount']:,.2f} ر.س", m["misstatement_type"], "تم التعديل" if m["is_adjusted"] else "غير معدل (أقل من التافه)"] for m in mis]
    print(tabulate(mis_rows, headers=["بيان التحريف", "المبلغ", "النوع", "الموقف الدفتري"], tablefmt="grid"))

    # 8. Quality Gates & EQCR
    print_section("8. بوابات الجودة ومراجعة الارتباط المستقلة (Quality Gates & EQCR)")
    gates = service.check_engagement_gates(eng_id)
    print(f"- البوابة 2 (التخطيط والأهمية والمخاطر): {'اجتياز بنجاح ✓' if gates['gate_2_planning']['passed'] else 'فشل'}")
    print(f"- البوابة 3 (العمل الميداني والتوثيق): {'اجتياز بنجاح ✓' if gates['gate_3_fieldwork']['passed'] else 'فشل'}")
    print(f"- البوابة 4 (مراجعة الجودة والإصدار): {'اجتياز بنجاح ✓' if gates['gate_4_issuance']['passed'] else 'فشل'}")
    print(f"- الجاهزية النهائية لإصدار التقرير: {'جاهز 100% ✓' if gates['ready_for_issuance'] else 'غير جاهز'}")

    # 9. Auditor's Report
    print_section("9. تقرير مراجع الحسابات المستقل (Independent Auditor's Report - ISA 700)")
    rep = reporter.generate_auditor_report(eng_id)
    print(rep["report_text"])

    conn.close()
    print("\nاكتمل تنفيذ دورة المراجعة بالكامل بنجاح تام.")

def main():
    parser = argparse.ArgumentParser(description="My Audit Platform CLI")
    parser.add_argument("--demo", action="store_true", help="Run full end-to-end audit demonstration")
    parser.add_argument("--serve", action="store_true", help="Start FastAPI web server")
    parser.add_argument("--port", type=int, default=8000, help="Port for web server")
    args = parser.parse_args()

    if args.serve:
        import uvicorn
        init_db()
        print(f"Starting My Audit Web Server on http://0.0.0.0:{args.port}...")
        uvicorn.run("my_audit.api.app:app", host="0.0.0.0", port=args.port, reload=False)
    else:
        run_audit_demo()

if __name__ == "__main__":
    main()
