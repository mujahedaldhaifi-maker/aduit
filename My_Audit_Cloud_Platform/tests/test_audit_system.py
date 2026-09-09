import unittest
import os
from my_audit.database import init_db
from my_audit.engines.trial_balance_engine import TrialBalanceEngine
from my_audit.engines.mapping_engine import MappingEngine
from my_audit.engines.materiality_engine import MaterialityEngine
from my_audit.engines.risk_engine import RiskEngine
from my_audit.engines.sampling_engine import SamplingEngine
from my_audit.engines.quality_gates import QualityGateEnforcer
from my_audit.services.audit_service import AuditService
from my_audit.services.report_generator import ReportGenerator

class TestMyAuditPlatform(unittest.TestCase):
    def setUp(self):
        self.test_db = "/tmp/test_my_audit.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        init_db(self.test_db)
        self.service = AuditService(self.test_db)
        self.reporter = ReportGenerator(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_trial_balance_verification_and_anomalies(self):
        accounts = [
            {"code": "1010", "name": "البنك التجاري", "debit": 1000.0, "credit": 0.0},
            {"code": "2010", "name": "الموردين", "debit": 0.0, "credit": 1000.0}
        ]
        res = TrialBalanceEngine.verify_balance(accounts)
        self.assertTrue(res["is_balanced"])
        self.assertEqual(res["total_debit"], 1000.0)

        # Anomaly test: negative cash
        anomaly_accs = [
            {"code": "1010", "name": "حساب الصندوق", "debit": 0.0, "credit": 500.0}
        ]
        anomalies = TrialBalanceEngine.detect_anomalies(anomaly_accs)
        self.assertTrue(any(a["type"] == "Negative Cash / Overdraft" for a in anomalies))

    def test_mapping_engine(self):
        cat, item, conf = MappingEngine.suggest_mapping("1010", "النقدية بالصندوق والبنوك")
        self.assertEqual(cat, "CurrentAssets")
        self.assertEqual(item, "Cash and Cash Equivalents")
        self.assertGreater(conf, 0.9)

        cat2, item2, conf2 = MappingEngine.suggest_mapping("4010", "إيرادات عقود المبيعات")
        self.assertEqual(cat2, "Revenue")

    def test_materiality_engine(self):
        pbt = 1000000.0
        mat = MaterialityEngine.calculate(
            benchmark_type="ProfitBeforeTax",
            benchmark_amount=pbt,
            overall_percentage=5.0,
            performance_percentage=75.0,
            trivial_percentage=5.0
        )
        self.assertEqual(mat["overall_materiality"], 50000.0)
        self.assertEqual(mat["performance_materiality"], 37500.0)
        self.assertEqual(mat["trivial_threshold"], 2500.0)

    def test_risk_engine(self):
        rmm = RiskEngine.evaluate_rmm("High", "High")
        self.assertEqual(rmm["rmm"], "Significant")
        self.assertEqual(rmm["is_significant"], 1)

        rmm2 = RiskEngine.evaluate_rmm("Low", "Low")
        self.assertEqual(rmm2["rmm"], "Low")

    def test_sampling_engine(self):
        sampling = SamplingEngine.calculate_mus_sample_size(
            population_value=1000000.0,
            tolerable_misstatement=50000.0,
            confidence_level=0.95
        )
        self.assertGreater(sampling["recommended_sample_size"], 10)
        self.assertEqual(sampling["method"], "Monetary Unit Sampling (MUS)")

    def test_quality_gates(self):
        # Gate 1
        eval_pass = {
            "independence_passed": 1,
            "integrity_passed": 1,
            "conflict_of_interest": 0,
            "decision": "Accepted"
        }
        self.assertTrue(QualityGateEnforcer.evaluate_gate_1_acceptance_to_planning(eval_pass)["passed"])

        eval_fail = {
            "independence_passed": 0,
            "integrity_passed": 1,
            "conflict_of_interest": 1,
            "decision": "Rejected"
        }
        self.assertFalse(QualityGateEnforcer.evaluate_gate_1_acceptance_to_planning(eval_fail)["passed"])

    def test_end_to_end_audit_service_lifecycle(self):
        # 1. Create client & evaluate acceptance
        cl = self.service.create_client({"name": "شركة الاختبار"})
        self.service.evaluate_acceptance({
            "client_id": cl["client_id"],
            "independence_passed": True,
            "integrity_passed": True,
            "conflict_of_interest": False,
            "decision": "Accepted"
        })

        # 2. Create engagement
        eng = self.service.create_engagement({
            "client_id": cl["client_id"],
            "title": "مراجعة سنة 2026",
            "fiscal_year": 2026,
            "partner_name": "الشريك الأول",
            "manager_name": "المدير الأول"
        })
        eng_id = eng["engagement_id"]

        # 3. Import TB
        tb_data = [
            {"code": "1010", "name": "نقد وبنوك", "debit": 500000.0, "credit": 0.0},
            {"code": "2010", "name": "دائنون تجاريون", "debit": 0.0, "credit": 200000.0},
            {"code": "3010", "name": "رأس مال", "debit": 0.0, "credit": 300000.0}
        ]
        self.service.import_trial_balance(eng_id, tb_data)

        # 4. Materiality
        mat = self.service.calculate_and_set_materiality(eng_id, "TotalAssets", 500000.0, overall_percentage=1.0)
        self.assertEqual(mat["overall_materiality"], 5000.0)

        # 5. Risks & Procedures
        r = self.service.add_risk({
            "engagement_id": eng_id,
            "account_category": "Cash",
            "description": "خطر مطابقة النقدية",
            "assertion": "Existence",
            "inherent_risk": "Medium",
            "control_risk": "Low"
        })
        prg = self.service.create_program(eng_id, "Cash", "برنامج النقد")
        prc = self.service.add_procedure({
            "program_id": prg["program_id"],
            "risk_id": r["risk_id"],
            "description": "مصادقة بنكية",
            "assertion": "Existence"
        })

        # 6. WP & Confirmations
        wp = self.service.document_working_paper({
            "procedure_id": prc["procedure_id"],
            "title": "ورقة النقد",
            "objective": "التأكد من رصيد البنك",
            "assertion": "Existence",
            "procedures_performed": "تمت المصادقة",
            "results": "مطابق 100%",
            "conclusion": "سليم",
            "prepared_by": "المدقق"
        })

        # 7. Quality Gates check
        gates = self.service.check_engagement_gates(eng_id)
        self.assertTrue(gates["gate_2_planning"]["passed"])
        self.assertTrue(gates["gate_3_fieldwork"]["passed"])

        # 8. Auditor's report
        rep = self.reporter.generate_auditor_report(eng_id)
        self.assertIn("تقرير مراجع الحسابات المستقل", rep["report_text"])
        self.assertIn("Unmodified / Clean Opinion", rep["opinion_type"])

if __name__ == "__main__":
    unittest.main()
