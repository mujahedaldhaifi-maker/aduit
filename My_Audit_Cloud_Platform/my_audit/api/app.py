from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any

from my_audit.database import init_db, get_connection
from my_audit.models import (
    ClientCreate, AcceptanceCreate, EngagementCreate,
    TrialBalanceImportRequest, AccountMappingUpdateRequest,
    MaterialityRequest, RiskCreate, ProcedureCreate,
    WorkingPaperCreate, EvidenceCreate, SampleCalculateRequest,
    ConfirmationCreate, ReviewNoteCreate, ReviewNoteResolve,
    MisstatementCreate, EQCRReviewCreate
)
from my_audit.services.audit_service import AuditService
from my_audit.services.report_generator import ReportGenerator

app = FastAPI(
    title="My Audit Platform API (منظومة ماي أودت للمراجعة الخارجية)",
    description="منصة سحابية متكاملة لإدارة دورة المراجعة الخارجية وفق المعايير الدولية ISA وSOCPA وISQM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = AuditService()
reporter = ReportGenerator()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "system": "My Audit API", "standards": ["ISA", "SOCPA", "ISQM"]}

# Dashboard
@app.get("/api/dashboard/summary")
def get_dashboard(engagement_id: Optional[str] = None):
    return service.get_dashboard_summary(engagement_id)

# Clients
@app.post("/api/clients")
def create_client(client: ClientCreate):
    return service.create_client(client.dict())

@app.get("/api/clients")
def list_clients():
    conn = service._conn()
    rows = conn.execute("SELECT * FROM clients ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Acceptance
@app.post("/api/acceptance/evaluate")
def evaluate_acceptance(acceptance: AcceptanceCreate):
    return service.evaluate_acceptance(acceptance.dict())

# Engagements
@app.post("/api/engagements")
def create_engagement(eng: EngagementCreate):
    try:
        return service.create_engagement(eng.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/engagements")
def list_engagements():
    conn = service._conn()
    rows = conn.execute("""
        SELECT e.*, c.name as client_name, c.tax_id
        FROM engagements e
        JOIN clients c ON c.client_id = e.client_id
        ORDER BY e.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/engagements/{engagement_id}")
def get_engagement(engagement_id: str):
    conn = service._conn()
    eng = conn.execute("SELECT * FROM engagements WHERE engagement_id = ?", (engagement_id,)).fetchone()
    conn.close()
    if not eng:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return dict(eng)

# Trial Balance & Mapping
@app.post("/api/tb/import")
def import_trial_balance(payload: TrialBalanceImportRequest):
    try:
        raw_list = [acc.dict() for acc in payload.accounts]
        return service.import_trial_balance(payload.engagement_id, raw_list)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tb/accounts/{engagement_id}")
def get_tb_accounts(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("""
        SELECT a.* FROM accounts a
        JOIN trial_balances tb ON tb.tb_id = a.tb_id
        WHERE tb.engagement_id = ?
        ORDER BY a.code
    """, (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Materiality
@app.post("/api/materiality/calculate")
def calculate_materiality(payload: MaterialityRequest):
    return service.calculate_and_set_materiality(
        engagement_id=payload.engagement_id,
        benchmark_type=payload.benchmark_type,
        benchmark_amount=payload.benchmark_amount,
        overall_percentage=payload.overall_percentage,
        performance_percentage=payload.performance_percentage,
        trivial_percentage=payload.trivial_percentage,
        user_name=payload.approved_by
    )

@app.get("/api/materiality/{engagement_id}")
def get_materiality(engagement_id: str):
    conn = service._conn()
    row = conn.execute("SELECT * FROM materiality WHERE engagement_id = ? ORDER BY approved_at DESC LIMIT 1", (engagement_id,)).fetchone()
    conn.close()
    if not row:
        return {}
    return dict(row)

# Risks
@app.post("/api/risks")
def add_risk(payload: RiskCreate):
    return service.add_risk(payload.dict())

@app.get("/api/risks/{engagement_id}")
def get_risks(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("SELECT * FROM risks WHERE engagement_id = ?", (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Audit Programs & Procedures
@app.post("/api/programs")
def create_program(engagement_id: str, area_name: str, title: str):
    return service.create_program(engagement_id, area_name, title)

@app.post("/api/procedures")
def add_procedure(payload: ProcedureCreate):
    return service.add_procedure(payload.dict())

@app.get("/api/procedures/{engagement_id}")
def list_procedures(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("""
        SELECT pr.*, p.title as program_title, p.area_name
        FROM procedures pr
        JOIN audit_programs p ON p.program_id = pr.program_id
        WHERE p.engagement_id = ?
    """, (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Working Papers
@app.post("/api/working-papers")
def document_working_paper(payload: WorkingPaperCreate):
    return service.document_working_paper(payload.dict(), user_name=payload.prepared_by)

@app.get("/api/working-papers/{engagement_id}")
def list_working_papers(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("""
        SELECT wp.*, pr.description as procedure_desc, p.area_name
        FROM working_papers wp
        JOIN procedures pr ON pr.procedure_id = wp.procedure_id
        JOIN audit_programs p ON p.program_id = pr.program_id
        WHERE p.engagement_id = ?
    """, (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Evidence
@app.post("/api/evidence")
def attach_evidence(payload: EvidenceCreate):
    return service.attach_evidence(payload.dict())

# Sampling
@app.post("/api/sampling/calculate")
def calculate_sampling(payload: SampleCalculateRequest):
    return service.calculate_sampling(payload.dict())

# Confirmations
@app.post("/api/confirmations")
def create_confirmation(payload: ConfirmationCreate):
    return service.create_confirmation(payload.dict())

@app.put("/api/confirmations/{conf_id}/reconcile")
def reconcile_confirmation(conf_id: str, confirmed_balance: float, notes: Optional[str] = ""):
    return service.reconcile_confirmation(conf_id, confirmed_balance, notes)

@app.get("/api/confirmations/{engagement_id}")
def list_confirmations(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("SELECT * FROM confirmations WHERE engagement_id = ?", (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Review Notes
@app.post("/api/review-notes")
def raise_review_note(payload: ReviewNoteCreate):
    return service.raise_review_note(payload.dict(), user_name=payload.raised_by)

@app.put("/api/review-notes/resolve")
def resolve_review_note(payload: ReviewNoteResolve):
    return service.clear_review_note(payload.note_id, payload.response_text)

@app.get("/api/review-notes/{engagement_id}")
def list_review_notes(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("SELECT * FROM review_notes WHERE engagement_id = ?", (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Misstatements
@app.post("/api/misstatements")
def record_misstatement(payload: MisstatementCreate):
    return service.record_misstatement(payload.dict())

@app.get("/api/misstatements/{engagement_id}")
def list_misstatements(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("SELECT * FROM misstatements WHERE engagement_id = ?", (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Quality Gates & EQCR
@app.get("/api/gates/check/{engagement_id}")
def check_gates(engagement_id: str):
    return service.check_engagement_gates(engagement_id)

@app.post("/api/eqcr/review")
def submit_eqcr(payload: EQCRReviewCreate):
    return service.submit_eqcr_review(payload.dict(), user_name=payload.reviewer_name)

# Reports
@app.get("/api/reports/lead-schedules/{engagement_id}")
def get_lead_schedules(engagement_id: str):
    return reporter.generate_lead_schedules(engagement_id)

@app.get("/api/reports/financial-statements/{engagement_id}")
def get_financial_statements(engagement_id: str):
    return reporter.generate_draft_financial_statements(engagement_id)

@app.get("/api/reports/auditor-report/{engagement_id}")
def get_auditor_report(engagement_id: str):
    return reporter.generate_auditor_report(engagement_id)

# Audit Trail
@app.get("/api/audit-trail/{engagement_id}")
def get_audit_trail(engagement_id: str):
    conn = service._conn()
    rows = conn.execute("SELECT * FROM audit_trail WHERE engagement_id = ? ORDER BY timestamp DESC", (engagement_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Interactive Web UI
@app.get("/", response_class=HTMLResponse)
def index_page():
    with open("/working_dir/c_e947e45d4369e070/my_audit/my_audit/web/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
