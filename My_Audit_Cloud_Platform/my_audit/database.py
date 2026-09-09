import sqlite3
import os
import json
from datetime import datetime

DEFAULT_DB_PATH = os.environ.get('MY_AUDIT_DB', '/tmp/my_audit.db')

def get_connection(db_path=None):
    path = db_path or DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path=None):
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Clients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        tax_id TEXT,
        industry TEXT,
        accounting_system TEXT,
        fiscal_year_end TEXT,
        created_at TEXT
    );
    """)

    # 2. Client Acceptance & Continuance
    cursor.execute("""
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
    );
    """)

    # 3. Engagements
    cursor.execute("""
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
    );
    """)

    # 4. Trial Balances
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trial_balances (
        tb_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        total_debit REAL NOT NULL,
        total_credit REAL NOT NULL,
        is_balanced INTEGER NOT NULL,
        imported_at TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );
    """)

    # 5. Accounts
    cursor.execute("""
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
    );
    """)

    # 6. Materiality (ISA 320)
    cursor.execute("""
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
    );
    """)

    # 7. Risk Assessments (ISA 315)
    cursor.execute("""
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
    );
    """)

    # 8. Audit Programs & Procedures (ISA 330)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_programs (
        program_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        area_name TEXT NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );
    """)

    cursor.execute("""
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
    );
    """)

    # 9. Working Papers (ISA 230)
    cursor.execute("""
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
    );
    """)

    # 10. Evidence Management
    cursor.execute("""
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
    );
    """)

    # 11. Samples (ISA 530)
    cursor.execute("""
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
    );
    """)

    # 12. Confirmations (ISA 505)
    cursor.execute("""
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
    );
    """)

    # 13. Findings & Review Notes
    cursor.execute("""
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
    );
    """)

    # 14. Misstatements & Adjustments (ISA 450)
    cursor.execute("""
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
    );
    """)

    # 15. PBC Requests (Client Portal)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pbc_requests (
        request_id TEXT PRIMARY KEY,
        engagement_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Requested',
        uploaded_file TEXT,
        FOREIGN KEY (engagement_id) REFERENCES engagements(engagement_id)
    );
    """)

    # 16. Quality Reviews (EQCR, ISQM 1 & 2, ISA 220)
    cursor.execute("""
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
    );
    """)

    # 17. Immutable Audit Trail
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        engagement_id TEXT,
        user_name TEXT NOT NULL,
        action TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def log_audit_trail(conn, engagement_id, user_name, action, entity_name, entity_id, details):
    ts = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO audit_trail (engagement_id, user_name, action, entity_name, entity_id, details, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (engagement_id, user_name, action, entity_name, entity_id, str(details), ts))
    conn.commit()
