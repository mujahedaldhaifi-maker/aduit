import base64
import json
import time
from typing import Dict, Any, Optional

class CloudSecurityContext:
    """
    إدارة الهوية والوصول السحابي (Cloud Identity & Multi-Tenancy Context)
    تدعم عزل مكاتب المراجعة (Tenant Isolation) وتحديد أدوار الفريق (RBAC).
    """
    ROLES = {
        "PARTNER": "شريك مراجعة (اعتماد نهائي وإصدار التقرير)",
        "MANAGER": "مدير ارتباط (إشراف واعتماد أوراق العمل)",
        "SENIOR": "كبير مراجعين (تنفيذ التخطيط وتقييم المخاطر)",
        "AUDITOR": "مدقق ميداني (تنفيذ الإجراءات وتوثيق الأدلة)",
        "EQCR": "شريك مراجعة الجودة المستقل (اعتماد الجودة قبل الإصدار)",
        "CLIENT": "عميل المنشأة (رفع مستندات PBC فقط)"
    }

    @staticmethod
    def create_token(user_id: str, user_name: str, tenant_id: str, role: str) -> str:
        payload = {
            "sub": user_id,
            "name": user_name,
            "tenant_id": tenant_id, # معرف مكتب المراجعة
            "role": role,
            "iat": int(time.time()),
            "exp": int(time.time()) + (3600 * 24)
        }
        token_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        return f"myaudit_jwt_{token_str}"

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            if not token.startswith("myaudit_jwt_"):
                return None
            raw = token.replace("myaudit_jwt_", "")
            padded = raw + "=" * (-len(raw) % 4)
            payload = json.loads(base64.urlsafe_b64decode(padded).decode())
            if payload.get("exp", 0) < time.time():
                return None
            return payload
        except Exception:
            return None
