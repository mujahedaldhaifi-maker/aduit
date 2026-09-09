from typing import Dict, Any, List

class QualityGateEnforcer:
    """
    Quality Gates & Workflow Rules Engine:
    Enforces compliance with ISA 220 (Revised), ISA 230, and ISQM 1/2.
    Ensures stage transitions only occur when all prerequisites are verified.
    """

    @staticmethod
    def evaluate_gate_1_acceptance_to_planning(eval_data: Dict[str, Any]) -> Dict[str, Any]:
        passed = (
            eval_data.get('independence_passed') == 1 and
            eval_data.get('integrity_passed') == 1 and
            eval_data.get('conflict_of_interest') == 0 and
            eval_data.get('decision') in ['Accepted', 'AcceptedWithConditions']
        )
        failures = []
        if eval_data.get('independence_passed') != 1:
            failures.append("فشل التحقق من استقلالية فريق المراجعة (ISA 210/ISQM 1).")
        if eval_data.get('integrity_passed') != 1:
            failures.append("فشل تقييم نزاهة إدارة العميل.")
        if eval_data.get('conflict_of_interest') == 1:
            failures.append("يوجد تعارض مصالح غير معالج مع العميل.")
        if eval_data.get('decision') not in ['Accepted', 'AcceptedWithConditions']:
            failures.append("لم يصدر قرار رسمي بقبول الارتباط.")

        return {
            "gate_name": "Gate 1: Client Acceptance & Continuance",
            "passed": passed,
            "errors": failures
        }

    @staticmethod
    def evaluate_gate_2_planning_to_fieldwork(tb_data: Dict[str, Any], materiality_data: Dict[str, Any], risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        failures = []
        if not tb_data or tb_data.get('is_balanced') != 1:
            failures.append("ميزان المراجعة غير متوازن (إجمالي المدين لا يساوي الدائن).")

        if not materiality_data or materiality_data.get('overall_materiality', 0) <= 0:
            failures.append("لم يتم تحديد واعتماد الأهمية النسبية (ISA 320).")

        if not risks or len(risks) == 0:
            failures.append("لم يتم إجراء تقييم المخاطر أو تحديد مخاطر التحريف الجوهري (ISA 315).")

        return {
            "gate_name": "Gate 2: Audit Planning & Risk Setup",
            "passed": len(failures) == 0,
            "errors": failures
        }

    @staticmethod
    def evaluate_gate_3_fieldwork_completion(procedures: List[Dict[str, Any]], working_papers: List[Dict[str, Any]], review_notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        failures = []

        # All procedures must be completed
        pending_procs = [p for p in procedures if p.get('status') != 'Completed']
        if pending_procs:
            failures.append(f"يوجد {len(pending_procs)} إجراء مراجعة لم يكتمل بعد.")

        # Every procedure should have a corresponding working paper
        proc_ids_with_wp = {wp.get('procedure_id') for wp in working_papers}
        missing_wp = [p for p in procedures if p.get('procedure_id') not in proc_ids_with_wp]
        if missing_wp:
            failures.append(f"يوجد {len(missing_wp)} إجراء مراجعة لا يحتوي على ورقة عمل موثقة (ISA 230).")

        # Open review notes
        open_notes = [n for n in review_notes if n.get('status') == 'Open']
        if open_notes:
            failures.append(f"يوجد {len(open_notes)} ملاحظة مراجعة معلقة لم يتم الرد عليها.")

        return {
            "gate_name": "Gate 3: Fieldwork Execution & Documentation",
            "passed": len(failures) == 0,
            "errors": failures
        }

    @staticmethod
    def evaluate_gate_4_issuance(
        unadjusted_misstatements_total: float,
        performance_materiality: float,
        eqcr_review: Dict[str, Any],
        review_notes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        failures = []

        # Review notes must be completely cleared
        uncleared = [n for n in review_notes if n.get('status') != 'Cleared']
        if uncleared:
            failures.append(f"يوجد {len(uncleared)} ملاحظات مراجعة لم يتم إغلاقها واعتمادها نهائيًا.")

        # Unadjusted misstatements <= Performance Materiality (ISA 450)
        if unadjusted_misstatements_total > performance_materiality:
            failures.append(
                f"إجمالي التحريفات غير المعدلة ({unadjusted_misstatements_total:,.2f} ر.س) يتجاوز الأهمية النسبية للأداء "
                f"({performance_materiality:,.2f} ر.س). يتطلب ذلك تعديل القوائم أو تعديل رأي المراجع (ISA 450)."
            )

        # EQCR sign-off if required
        if eqcr_review and eqcr_review.get('is_eqcr_required') == 1:
            if eqcr_review.get('approved') != 1:
                failures.append("مراجعة جودة الارتباط (EQCR) لم تُعتمد بعد من قبل مراجع الجودة المستقل (ISA 220/ISQM 2).")

        return {
            "gate_name": "Gate 4: Final Quality Gate & Report Issuance",
            "passed": len(failures) == 0,
            "errors": failures
        }
