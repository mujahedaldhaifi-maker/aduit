import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from my_audit.database import get_connection, log_audit_trail
from my_audit.engines.trial_balance_engine import TrialBalanceEngine
from my_audit.engines.mapping_engine import MappingEngine
from my_audit.engines.materiality_engine import MaterialityEngine
from my_audit.engines.risk_engine import RiskEngine
from my_audit.engines.sampling_engine import SamplingEngine
from my_audit.engines.quality_gates import QualityGateEnforcer

class AuditService:
    def __init__(self, db_path=None):
        self.db_path = db_path

    def _conn(self):
        return get_connection(self.db_path)

    # 1. Client Master & Acceptance
    def create_client(self, client_data: Dict[str, Any], user_name="Admin") -> Dict[str, Any]:
        conn = self._conn()
        client_id = client_data.get('client_id') or f"CL-{uuid.uuid4().hex[:6].upper()}"
        created_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO clients (client_id, name, tax_id, industry, accounting_system, fiscal_year_end, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            client_id,
            client_data['name'],
            client_data.get('tax_id'),
            client_data.get('industry'),
            client_data.get('accounting_system'),
            client_data.get('fiscal_year_end'),
            created_at
        ))
        log_audit_trail(conn, None, user_name, "CREATE", "clients", client_id, f"Created client {client_data['name']}")
        conn.close()
        return {"client_id": client_id, **client_data, "created_at": created_at}

    def evaluate_acceptance(self, eval_data: Dict[str, Any], user_name="Partner") -> Dict[str, Any]:
        conn = self._conn()
        eval_id = f"EV-{uuid.uuid4().hex[:6].upper()}"
        evaluated_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO acceptance_evaluations (
                eval_id, client_id, independence_passed, integrity_passed,
                conflict_of_interest, risk_level, decision, notes, evaluated_by, evaluated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            eval_id,
            eval_data['client_id'],
            1 if eval_data.get('independence_passed', True) else 0,
            1 if eval_data.get('integrity_passed', True) else 0,
            1 if eval_data.get('conflict_of_interest', False) else 0,
            eval_data.get('risk_level', 'Medium'),
            eval_data.get('decision', 'Accepted'),
            eval_data.get('notes', ''),
            eval_data.get('evaluated_by', user_name),
            evaluated_at
        ))
        log_audit_trail(conn, None, user_name, "CREATE", "acceptance_evaluations", eval_id, f"Client {eval_data['client_id']} acceptance decision: {eval_data.get('decision')}")
        conn.close()
        return {"eval_id": eval_id, **eval_data, "evaluated_at": evaluated_at}

    # 2. Engagement Setup
    def create_engagement(self, eng_data: Dict[str, Any], user_name="Manager") -> Dict[str, Any]:
        conn = self._conn()
        eng_id = eng_data.get('engagement_id') or f"ENG-{datetime.now().year}-{uuid.uuid4().hex[:4].upper()}"
        created_at = datetime.utcnow().isoformat()

        # Check acceptance gate
        eval_row = conn.execute("SELECT * FROM acceptance_evaluations WHERE client_id = ? ORDER BY evaluated_at DESC LIMIT 1", (eng_data['client_id'],)).fetchone()
        if eval_row:
            gate_check = QualityGateEnforcer.evaluate_gate_1_acceptance_to_planning(dict(eval_row))
            if not gate_check['passed']:
                conn.close()
                raise ValueError(f"Gate 1 Failed: {', '.join(gate_check['errors'])}")

        conn.execute("""
            INSERT INTO engagements (
                engagement_id, client_id, title, fiscal_year, start_date, end_date,
                partner_name, manager_name, senior_name, auditor_name, eqcr_reviewer,
                budgeted_hours, actual_hours, stage, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            eng_id,
            eng_data['client_id'],
            eng_data['title'],
            eng_data.get('fiscal_year', datetime.now().year),
            eng_data.get('start_date'),
            eng_data.get('end_date'),
            eng_data['partner_name'],
            eng_data['manager_name'],
            eng_data.get('senior_name'),
            eng_data.get('auditor_name'),
            eng_data.get('eqcr_reviewer'),
            eng_data.get('budgeted_hours', 100.0),
            0.0,
            'Planning',
            'Active',
            created_at
        ))
        log_audit_trail(conn, eng_id, user_name, "CREATE", "engagements", eng_id, f"Engagement created for client {eng_data['client_id']}")
        conn.close()
        return {"engagement_id": eng_id, **eng_data, "stage": "Planning", "status": "Active", "created_at": created_at}

    # 3. Trial Balance Import & Auto-Mapping
    def import_trial_balance(self, engagement_id: str, raw_accounts: List[Dict[str, Any]], user_name="Auditor") -> Dict[str, Any]:
        balance_check = TrialBalanceEngine.verify_balance(raw_accounts)
        if not balance_check['is_balanced']:
            raise ValueError(f"Trial Balance is not in balance! Total Debit={balance_check['total_debit']}, Total Credit={balance_check['total_credit']}, Diff={balance_check['difference']}")

        anomalies = TrialBalanceEngine.detect_anomalies(raw_accounts)

        conn = self._conn()
        tb_id = f"TB-{uuid.uuid4().hex[:6].upper()}"
        imported_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO trial_balances (tb_id, engagement_id, total_debit, total_credit, is_balanced, imported_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tb_id,
            engagement_id,
            balance_check['total_debit'],
            balance_check['total_credit'],
            1 if balance_check['is_balanced'] else 0,
            imported_at
        ))

        mapped_accounts = []
        for acc in raw_accounts:
            acc_id = f"ACC-{uuid.uuid4().hex[:6].upper()}"
            code = acc['code']
            name = acc['name']
            debit = float(acc.get('debit', 0.0))
            credit = float(acc.get('credit', 0.0))
            net = debit - credit

            # Auto suggest mapping
            fs_category, fs_line_item, confidence = MappingEngine.suggest_mapping(code, name)

            conn.execute("""
                INSERT INTO accounts (
                    account_id, tb_id, code, name, debit, credit, net_balance,
                    fs_category, fs_line_item, mapping_confidence, mapping_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                acc_id, tb_id, code, name, debit, credit, net,
                fs_category, fs_line_item, confidence, 'Suggested'
            ))
            mapped_accounts.append({
                "account_id": acc_id,
                "code": code,
                "name": name,
                "debit": debit,
                "credit": credit,
                "net_balance": net,
                "fs_category": fs_category,
                "fs_line_item": fs_line_item,
                "mapping_confidence": confidence
            })

        metrics = TrialBalanceEngine.calculate_financial_metrics(mapped_accounts)

        log_audit_trail(conn, engagement_id, user_name, "IMPORT", "trial_balances", tb_id, f"Imported {len(raw_accounts)} accounts. Debit/Credit={balance_check['total_debit']}")
        conn.close()

        return {
            "tb_id": tb_id,
            "engagement_id": engagement_id,
            "balance_check": balance_check,
            "anomalies": anomalies,
            "financial_metrics": metrics,
            "accounts_count": len(mapped_accounts)
        }

    # 4. Materiality Engine (ISA 320)
    def calculate_and_set_materiality(
        self,
        engagement_id: str,
        benchmark_type: str,
        benchmark_amount: float,
        overall_percentage: Optional[float] = None,
        performance_percentage: Optional[float] = 75.0,
        trivial_percentage: Optional[float] = 5.0,
        user_name: str = "Partner"
    ) -> Dict[str, Any]:
        calc = MaterialityEngine.calculate(
            benchmark_type=benchmark_type,
            benchmark_amount=benchmark_amount,
            overall_percentage=overall_percentage,
            performance_percentage=performance_percentage,
            trivial_percentage=trivial_percentage
        )

        conn = self._conn()
        mat_id = f"MAT-{uuid.uuid4().hex[:6].upper()}"
        approved_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO materiality (
                materiality_id, engagement_id, benchmark_type, benchmark_amount,
                overall_percentage, overall_materiality, performance_percentage,
                performance_materiality, trivial_percentage, trivial_threshold,
                justification, approved_by, approved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mat_id,
            engagement_id,
            benchmark_type,
            benchmark_amount,
            calc['overall_percentage'],
            calc['overall_materiality'],
            calc['performance_percentage'],
            calc['performance_materiality'],
            calc['trivial_percentage'],
            calc['trivial_threshold'],
            calc['justification'],
            user_name,
            approved_at
        ))
        log_audit_trail(conn, engagement_id, user_name, "CREATE", "materiality", mat_id, f"Materiality OM={calc['overall_materiality']}, PM={calc['performance_materiality']}")
        conn.close()

        return {"materiality_id": mat_id, **calc, "approved_by": user_name, "approved_at": approved_at}

    # 5. Risk Assessment (ISA 315)
    def add_risk(self, risk_data: Dict[str, Any], user_name="Senior") -> Dict[str, Any]:
        rmm_info = RiskEngine.evaluate_rmm(risk_data['inherent_risk'], risk_data['control_risk'])
        planned_response = risk_data.get('planned_response') or rmm_info['planned_response']

        conn = self._conn()
        risk_id = f"RSK-{uuid.uuid4().hex[:6].upper()}"
        conn.execute("""
            INSERT INTO risks (
                risk_id, engagement_id, account_category, fs_line_item, description,
                assertion, inherent_risk, control_risk, rmm, is_significant, planned_response, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            risk_id,
            risk_data['engagement_id'],
            risk_data['account_category'],
            risk_data.get('fs_line_item'),
            risk_data['description'],
            risk_data['assertion'],
            rmm_info['inherent_risk'],
            rmm_info['control_risk'],
            rmm_info['rmm'],
            rmm_info['is_significant'],
            planned_response,
            'Identified'
        ))
        log_audit_trail(conn, risk_data['engagement_id'], user_name, "CREATE", "risks", risk_id, f"Risk {risk_id}: {risk_data['description'][:50]} (RMM: {rmm_info['rmm']})")
        conn.close()

        return {
            "risk_id": risk_id,
            **risk_data,
            "rmm": rmm_info['rmm'],
            "is_significant": rmm_info['is_significant'],
            "planned_response": planned_response
        }

    # 6. Audit Programs & Procedures (ISA 330)
    def create_program(self, engagement_id: str, area_name: str, title: str, user_name="Manager") -> Dict[str, Any]:
        conn = self._conn()
        prog_id = f"PRG-{uuid.uuid4().hex[:6].upper()}"
        conn.execute("""
            INSERT INTO audit_programs (program_id, engagement_id, area_name, title)
            VALUES (?, ?, ?, ?)
        """, (prog_id, engagement_id, area_name, title))
        log_audit_trail(conn, engagement_id, user_name, "CREATE", "audit_programs", prog_id, f"Program: {title}")
        conn.close()
        return {"program_id": prog_id, "engagement_id": engagement_id, "area_name": area_name, "title": title}

    def add_procedure(self, proc_data: Dict[str, Any], user_name="Senior") -> Dict[str, Any]:
        conn = self._conn()
        proc_id = f"PRC-{uuid.uuid4().hex[:6].upper()}"
        conn.execute("""
            INSERT INTO procedures (
                procedure_id, program_id, risk_id, procedure_type, description,
                assertion, population_size, sample_size, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proc_id,
            proc_data['program_id'],
            proc_data.get('risk_id'),
            proc_data.get('procedure_type', 'SubstantiveTest'),
            proc_data['description'],
            proc_data['assertion'],
            proc_data.get('population_size', 0),
            proc_data.get('sample_size', 0),
            'Pending'
        ))
        # update engagement stage to Fieldwork
        prg = conn.execute("SELECT engagement_id FROM audit_programs WHERE program_id = ?", (proc_data['program_id'],)).fetchone()
        if prg:
            conn.execute("UPDATE engagements SET stage = 'Fieldwork' WHERE engagement_id = ?", (prg['engagement_id'],))

        log_audit_trail(conn, prg['engagement_id'] if prg else None, user_name, "CREATE", "procedures", proc_id, f"Procedure: {proc_data['description'][:50]}")
        conn.close()
        return {"procedure_id": proc_id, **proc_data, "status": "Pending"}

    # 7. Electronic Working Papers (ISA 230)
    def document_working_paper(self, wp_data: Dict[str, Any], user_name="Auditor") -> Dict[str, Any]:
        conn = self._conn()
        wp_id = f"WP-{uuid.uuid4().hex[:6].upper()}"
        now_ts = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO working_papers (
                wp_id, procedure_id, title, objective, assertion,
                procedures_performed, results, exceptions_noted, conclusion,
                prepared_by, prepared_at, reviewed_by, reviewed_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            wp_id,
            wp_data['procedure_id'],
            wp_data['title'],
            wp_data['objective'],
            wp_data['assertion'],
            wp_data['procedures_performed'],
            wp_data['results'],
            wp_data.get('exceptions_noted', 'لا توجد استثناءات.'),
            wp_data['conclusion'],
            user_name,
            now_ts,
            wp_data.get('reviewed_by', 'Senior Auditor'),
            now_ts,
            'Reviewed'
        ))

        # Mark procedure completed
        conn.execute("UPDATE procedures SET status = 'Completed', completed_by = ?, completed_at = ? WHERE procedure_id = ?", (user_name, now_ts, wp_data['procedure_id']))

        # Find engagement
        prg = conn.execute("""
            SELECT p.engagement_id FROM audit_programs p
            JOIN procedures pr ON pr.program_id = p.program_id
            WHERE pr.procedure_id = ?
        """, (wp_data['procedure_id'],)).fetchone()

        eng_id = prg['engagement_id'] if prg else None
        log_audit_trail(conn, eng_id, user_name, "CREATE", "working_papers", wp_id, f"Documented WP: {wp_data['title']}")
        conn.close()
        return {"wp_id": wp_id, **wp_data, "prepared_by": user_name, "prepared_at": now_ts, "status": "Reviewed"}

    # 8. Evidence Management
    def attach_evidence(self, ev_data: Dict[str, Any], user_name="Auditor") -> Dict[str, Any]:
        conn = self._conn()
        ev_id = f"EVD-{uuid.uuid4().hex[:6].upper()}"
        uploaded_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO evidence (
                evidence_id, procedure_id, wp_id, file_name, file_type, file_size, description, source, uploaded_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ev_id,
            ev_data['procedure_id'],
            ev_data.get('wp_id'),
            ev_data['file_name'],
            ev_data.get('file_type', 'PDF'),
            ev_data.get('file_size', 1024),
            ev_data.get('description', ''),
            ev_data.get('source', 'ClientPBC'),
            uploaded_at
        ))
        log_audit_trail(conn, None, user_name, "ATTACH", "evidence", ev_id, f"Attached evidence {ev_data['file_name']}")
        conn.close()
        return {"evidence_id": ev_id, **ev_data, "uploaded_at": uploaded_at}

    # 9. Sampling Execution (ISA 530)
    def calculate_sampling(self, sample_req: Dict[str, Any], user_name="Auditor") -> Dict[str, Any]:
        result = SamplingEngine.calculate_mus_sample_size(
            population_value=sample_req['population_value'],
            tolerable_misstatement=sample_req['tolerable_misstatement'],
            expected_misstatement=sample_req.get('expected_misstatement', 0.0),
            confidence_level=sample_req.get('confidence_level', 0.95)
        )

        conn = self._conn()
        sample_id = f"SMP-{uuid.uuid4().hex[:6].upper()}"
        conn.execute("""
            INSERT INTO samples (
                sample_id, procedure_id, method, population_amount, tolerable_misstatement,
                expected_misstatement, confidence_level, sample_size, items_selected
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sample_id,
            sample_req['procedure_id'],
            result['method'],
            sample_req['population_value'],
            sample_req['tolerable_misstatement'],
            sample_req.get('expected_misstatement', 0.0),
            sample_req.get('confidence_level', 0.95),
            result['recommended_sample_size'],
            json.dumps({"description": "Systematic sample selection based on MUS interval"})
        ))

        # Update procedure sample size
        conn.execute("UPDATE procedures SET sample_size = ?, population_size = ? WHERE procedure_id = ?",
                     (result['recommended_sample_size'], int(sample_req['population_value']), sample_req['procedure_id']))

        log_audit_trail(conn, None, user_name, "CALCULATE", "samples", sample_id, f"Sample size {result['recommended_sample_size']} for procedure {sample_req['procedure_id']}")
        conn.close()
        return {"sample_id": sample_id, **result}

    # 10. Confirmations (ISA 505)
    def create_confirmation(self, conf_data: Dict[str, Any], user_name="Auditor") -> Dict[str, Any]:
        conn = self._conn()
        conf_id = f"CNF-{uuid.uuid4().hex[:6].upper()}"
        sent_date = datetime.utcnow().strftime("%Y-%m-%d")

        conn.execute("""
            INSERT INTO confirmations (
                confirmation_id, engagement_id, recipient_name, recipient_type,
                account_reference, book_balance, confirmed_balance, status, sent_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conf_id,
            conf_data['engagement_id'],
            conf_data['recipient_name'],
            conf_data['recipient_type'],
            conf_data.get('account_reference'),
            conf_data['book_balance'],
            conf_data.get('confirmed_balance'),
            'Sent',
            sent_date,
            conf_data.get('notes', '')
        ))
        log_audit_trail(conn, conf_data['engagement_id'], user_name, "CREATE", "confirmations", conf_id, f"Sent confirmation to {conf_data['recipient_name']}")
        conn.close()
        return {"confirmation_id": conf_id, **conf_data, "status": "Sent", "sent_date": sent_date}

    def reconcile_confirmation(self, conf_id: str, confirmed_balance: float, notes: str = "", user_name="Auditor") -> Dict[str, Any]:
        conn = self._conn()
        row = conn.execute("SELECT book_balance, engagement_id FROM confirmations WHERE confirmation_id = ?", (conf_id,)).fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Confirmation {conf_id} not found")

        diff = abs(row['book_balance'] - confirmed_balance)
        status = 'Cleared' if diff < 1.0 else 'DiscrepancyNoted'
        received_date = datetime.utcnow().strftime("%Y-%m-%d")

        conn.execute("""
            UPDATE confirmations
            SET confirmed_balance = ?, status = ?, received_date = ?, notes = ?
            WHERE confirmation_id = ?
        """, (confirmed_balance, status, received_date, notes, conf_id))

        log_audit_trail(conn, row['engagement_id'], user_name, "UPDATE", "confirmations", conf_id, f"Reconciled confirmation. Status: {status}, Diff: {diff}")
        conn.close()
        return {"confirmation_id": conf_id, "status": status, "diff": diff, "received_date": received_date}

    # 11. Review Notes / Findings
    def raise_review_note(self, note_data: Dict[str, Any], user_name="Manager") -> Dict[str, Any]:
        conn = self._conn()
        note_id = f"NOT-{uuid.uuid4().hex[:6].upper()}"
        created_at = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO review_notes (
                note_id, engagement_id, wp_id, raised_by, assigned_to, priority, note_text, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            note_id,
            note_data['engagement_id'],
            note_data.get('wp_id'),
            user_name,
            note_data['assigned_to'],
            note_data.get('priority', 'Medium'),
            note_data['note_text'],
            'Open',
            created_at
        ))
        log_audit_trail(conn, note_data['engagement_id'], user_name, "CREATE", "review_notes", note_id, f"Review Note: {note_data['note_text'][:50]}")
        conn.close()
        return {"note_id": note_id, **note_data, "raised_by": user_name, "status": "Open", "created_at": created_at}

    def clear_review_note(self, note_id: str, response_text: str, user_name="Manager") -> Dict[str, Any]:
        conn = self._conn()
        now_ts = datetime.utcnow().isoformat()
        row = conn.execute("SELECT engagement_id FROM review_notes WHERE note_id = ?", (note_id,)).fetchone()
        conn.execute("""
            UPDATE review_notes
            SET response_text = ?, status = 'Cleared', cleared_at = ?
            WHERE note_id = ?
        """, (response_text, now_ts, note_id))

        log_audit_trail(conn, row['engagement_id'] if row else None, user_name, "CLEAR", "review_notes", note_id, f"Cleared note {note_id}")
        conn.close()
        return {"note_id": note_id, "status": "Cleared", "response_text": response_text, "cleared_at": now_ts}

    # 12. Misstatements & Adjustments (ISA 450)
    def record_misstatement(self, mis_data: Dict[str, Any], user_name="Senior") -> Dict[str, Any]:
        conn = self._conn()
        mis_id = f"MIS-{uuid.uuid4().hex[:6].upper()}"

        conn.execute("""
            INSERT INTO misstatements (
                misstatement_id, engagement_id, account_id, description, amount,
                misstatement_type, is_adjusted, impact_on_pnl
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mis_id,
            mis_data['engagement_id'],
            mis_data.get('account_id'),
            mis_data['description'],
            mis_data['amount'],
            mis_data.get('misstatement_type', 'Factual'),
            1 if mis_data.get('is_adjusted', False) else 0,
            mis_data.get('impact_on_pnl', 0.0)
        ))
        log_audit_trail(conn, mis_data['engagement_id'], user_name, "CREATE", "misstatements", mis_id, f"Misstatement {mis_id}: {mis_data['amount']} SAR")
        conn.close()
        return {"misstatement_id": mis_id, **mis_data}

    # 13. Quality Review & EQCR (ISQM 1/2 & ISA 220)
    def submit_eqcr_review(self, eqcr_data: Dict[str, Any], user_name="EQCR Partner") -> Dict[str, Any]:
        conn = self._conn()
        rev_id = f"EQC-{uuid.uuid4().hex[:6].upper()}"
        appr_date = datetime.utcnow().isoformat()

        conn.execute("""
            INSERT INTO quality_reviews (
                review_id, engagement_id, reviewer_name, is_eqcr_required,
                checklist_results, reviewer_comments, approved, approval_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rev_id,
            eqcr_data['engagement_id'],
            eqcr_data.get('reviewer_name', user_name),
            1 if eqcr_data.get('is_eqcr_required', True) else 0,
            json.dumps(eqcr_data.get('checklist_results', {})),
            eqcr_data.get('reviewer_comments', 'تمت مراجعة جودة الارتباط والموافقة على إصدار التقرير.'),
            1 if eqcr_data.get('approved', True) else 0,
            appr_date
        ))
        conn.execute("UPDATE engagements SET stage = 'EQCR' WHERE engagement_id = ?", (eqcr_data['engagement_id'],))
        log_audit_trail(conn, eqcr_data['engagement_id'], user_name, "APPROVE", "quality_reviews", rev_id, f"EQCR Approval: {eqcr_data.get('approved')}")
        conn.close()
        return {"review_id": rev_id, **eqcr_data, "approval_date": appr_date}

    # 14. Gate Check Evaluation
    def check_engagement_gates(self, engagement_id: str) -> Dict[str, Any]:
        conn = self._conn()
        eng = conn.execute("SELECT * FROM engagements WHERE engagement_id = ?", (engagement_id,)).fetchone()
        if not eng:
            conn.close()
            raise ValueError(f"Engagement {engagement_id} not found")

        tb = conn.execute("SELECT * FROM trial_balances WHERE engagement_id = ? ORDER BY imported_at DESC LIMIT 1", (engagement_id,)).fetchone()
        mat = conn.execute("SELECT * FROM materiality WHERE engagement_id = ? ORDER BY approved_at DESC LIMIT 1", (engagement_id,)).fetchone()
        risks = [dict(r) for r in conn.execute("SELECT * FROM risks WHERE engagement_id = ?", (engagement_id,)).fetchall()]

        procs = [dict(r) for r in conn.execute("""
            SELECT pr.* FROM procedures pr
            JOIN audit_programs p ON p.program_id = pr.program_id
            WHERE p.engagement_id = ?
        """, (engagement_id,)).fetchall()]

        proc_ids = [p['procedure_id'] for p in procs]
        wps = []
        if proc_ids:
            placeholders = ','.join(['?'] * len(proc_ids))
            wps = [dict(r) for r in conn.execute(f"SELECT * FROM working_papers WHERE procedure_id IN ({placeholders})", proc_ids).fetchall()]

        notes = [dict(r) for r in conn.execute("SELECT * FROM review_notes WHERE engagement_id = ?", (engagement_id,)).fetchall()]
        misstatements = [dict(r) for r in conn.execute("SELECT * FROM misstatements WHERE engagement_id = ?", (engagement_id,)).fetchall()]
        eqcr = conn.execute("SELECT * FROM quality_reviews WHERE engagement_id = ? ORDER BY approval_date DESC LIMIT 1", (engagement_id,)).fetchone()

        unadjusted_total = sum(m['amount'] for m in misstatements if m['is_adjusted'] == 0)
        pm = mat['performance_materiality'] if mat else 0.0

        g2 = QualityGateEnforcer.evaluate_gate_2_planning_to_fieldwork(dict(tb) if tb else {}, dict(mat) if mat else {}, risks)
        g3 = QualityGateEnforcer.evaluate_gate_3_fieldwork_completion(procs, wps, notes)
        g4 = QualityGateEnforcer.evaluate_gate_4_issuance(unadjusted_total, pm, dict(eqcr) if eqcr else None, notes)

        ready_for_issuance = g2['passed'] and g3['passed'] and g4['passed']

        conn.close()
        return {
            "engagement_id": engagement_id,
            "gate_2_planning": g2,
            "gate_3_fieldwork": g3,
            "gate_4_issuance": g4,
            "ready_for_issuance": ready_for_issuance,
            "unadjusted_misstatements_total": unadjusted_total,
            "performance_materiality": pm
        }

    # 15. Dashboard KPIs & Metrics
    def get_dashboard_summary(self, engagement_id: Optional[str] = None) -> Dict[str, Any]:
        conn = self._conn()
        eng_filter = "WHERE engagement_id = ?" if engagement_id else ""
        eng_params = (engagement_id,) if engagement_id else ()

        total_engagements = conn.execute("SELECT count(*) as c FROM engagements").fetchone()['c']
        active_engagements = conn.execute("SELECT count(*) as c FROM engagements WHERE status = 'Active'").fetchone()['c']

        procs_total = conn.execute(f"SELECT count(*) as c FROM procedures pr JOIN audit_programs p ON p.program_id = pr.program_id {eng_filter}", eng_params).fetchone()['c']
        procs_completed = conn.execute(f"SELECT count(*) as c FROM procedures pr JOIN audit_programs p ON p.program_id = pr.program_id {eng_filter} {'AND' if engagement_id else 'WHERE'} pr.status = 'Completed'", eng_params).fetchone()['c']

        completion_pct = round((procs_completed / procs_total) * 100, 1) if procs_total > 0 else 0.0

        notes_total = conn.execute(f"SELECT count(*) as c FROM review_notes {eng_filter}", eng_params).fetchone()['c']
        notes_open = conn.execute(f"SELECT count(*) as c FROM review_notes {eng_filter} {'AND' if engagement_id else 'WHERE'} status = 'Open'", eng_params).fetchone()['c']
        notes_cleared = conn.execute(f"SELECT count(*) as c FROM review_notes {eng_filter} {'AND' if engagement_id else 'WHERE'} status = 'Cleared'", eng_params).fetchone()['c']

        risks_count = conn.execute(f"SELECT count(*) as c FROM risks {eng_filter}", eng_params).fetchone()['c']
        significant_risks = conn.execute(f"SELECT count(*) as c FROM risks {eng_filter} {'AND' if engagement_id else 'WHERE'} is_significant = 1", eng_params).fetchone()['c']

        wps_count = conn.execute("SELECT count(*) as c FROM working_papers").fetchone()['c']
        evidence_count = conn.execute("SELECT count(*) as c FROM evidence").fetchone()['c']

        conn.close()
        return {
            "total_engagements": total_engagements,
            "active_engagements": active_engagements,
            "procedures_total": procs_total,
            "procedures_completed": procs_completed,
            "procedures_completion_pct": completion_pct,
            "review_notes_total": notes_total,
            "review_notes_open": notes_open,
            "review_notes_cleared": notes_cleared,
            "risks_total": risks_count,
            "significant_risks": significant_risks,
            "working_papers_total": wps_count,
            "evidence_files_total": evidence_count
        }
