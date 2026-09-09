from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ClientCreate(BaseModel):
    client_id: str
    name: str
    tax_id: Optional[str] = None
    industry: Optional[str] = "تجارة عامة وخدمات"
    accounting_system: Optional[str] = "ERP / Cloud Accounting"
    fiscal_year_end: Optional[str] = "2026-12-31"

class AcceptanceCreate(BaseModel):
    client_id: str
    independence_passed: bool = True
    integrity_passed: bool = True
    conflict_of_interest: bool = False
    risk_level: str = "Medium"
    decision: str = "Accepted"
    notes: Optional[str] = "تم استيفاء معايير الاستقلالية والنزاهة وفقًا لـ ISA 210."
    evaluated_by: str = "Partner / Engagement Manager"

class EngagementCreate(BaseModel):
    engagement_id: str
    client_id: str
    title: str
    fiscal_year: int = 2026
    start_date: str = "2026-01-01"
    end_date: str = "2026-12-31"
    partner_name: str
    manager_name: str
    senior_name: Optional[str] = "Senior Auditor"
    auditor_name: Optional[str] = "Staff Auditor"
    eqcr_reviewer: Optional[str] = "Independent Quality Reviewer"
    budgeted_hours: float = 120.0

class TrialBalanceAccountItem(BaseModel):
    code: str
    name: str
    debit: float = 0.0
    credit: float = 0.0

class TrialBalanceImportRequest(BaseModel):
    engagement_id: str
    accounts: List[TrialBalanceAccountItem]

class AccountMappingUpdateRequest(BaseModel):
    account_id: str
    fs_category: str
    fs_line_item: str
    mapping_status: str = "Approved"

class MaterialityRequest(BaseModel):
    engagement_id: str
    benchmark_type: str = "ProfitBeforeTax"
    benchmark_amount: float
    overall_percentage: Optional[float] = None
    performance_percentage: Optional[float] = 75.0
    trivial_percentage: Optional[float] = 5.0
    approved_by: str = "Engagement Partner"

class RiskCreate(BaseModel):
    engagement_id: str
    account_category: str
    fs_line_item: Optional[str] = None
    description: str
    assertion: str
    inherent_risk: str
    control_risk: str
    planned_response: Optional[str] = None

class ProcedureCreate(BaseModel):
    program_id: str
    risk_id: Optional[str] = None
    procedure_type: str = "SubstantiveTest"
    description: str
    assertion: str
    population_size: Optional[int] = 0
    sample_size: Optional[int] = 0

class WorkingPaperCreate(BaseModel):
    procedure_id: str
    title: str
    objective: str
    assertion: str
    procedures_performed: str
    results: str
    exceptions_noted: Optional[str] = "لا توجد استثناءات أو أخطاء جوهرية."
    conclusion: str = "الرصيد يظهر بعدالة ومطابق لمتطلبات المعايير الدولية."
    prepared_by: str
    reviewed_by: Optional[str] = "Audit Senior"

class EvidenceCreate(BaseModel):
    procedure_id: str
    wp_id: Optional[str] = None
    file_name: str
    file_type: str = "PDF"
    file_size: int = 1024
    description: str
    source: str = "ClientPBC"

class SampleCalculateRequest(BaseModel):
    procedure_id: str
    population_value: float
    tolerable_misstatement: float
    expected_misstatement: float = 0.0
    confidence_level: float = 0.95

class ConfirmationCreate(BaseModel):
    engagement_id: str
    recipient_name: str
    recipient_type: str
    account_reference: str
    book_balance: float
    confirmed_balance: Optional[float] = None
    notes: Optional[str] = None

class ReviewNoteCreate(BaseModel):
    engagement_id: str
    wp_id: Optional[str] = None
    raised_by: str
    assigned_to: str
    priority: str = "Medium"
    note_text: str

class ReviewNoteResolve(BaseModel):
    note_id: str
    response_text: str
    status: str = "Cleared"

class MisstatementCreate(BaseModel):
    engagement_id: str
    account_id: Optional[str] = None
    description: str
    amount: float
    misstatement_type: str = "Factual"
    is_adjusted: bool = False
    impact_on_pnl: float = 0.0

class EQCRReviewCreate(BaseModel):
    engagement_id: str
    reviewer_name: str
    is_eqcr_required: bool = True
    checklist_results: Dict[str, Any]
    reviewer_comments: str
    approved: bool = True
