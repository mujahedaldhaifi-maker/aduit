import os
from typing import List

class CloudSettings:
    """إعدادات البيئة السحابية لمنظومة ماي أودت"""
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # توطين البيانات والامتثال السعودي (Saudi PDPL & CST Compliance)
    DATA_RESIDENCY_REGION: str = os.getenv("DATA_RESIDENCY_REGION", "sa-central-1") # Dammam / Riyadh
    DATA_ENCRYPTION_STANDARD: str = "AES-256"

    # قاعدة البيانات السحابية (PostgreSQL Managed / Cloud SQL / RDS)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:////tmp/my_audit_cloud.db")

    # التخزين السحابي للمستندات والأدلة (S3 / MinIO / GCS / R2)
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local") # "s3" or "local"
    S3_ENDPOINT_URL: str = os.getenv("S3_ENDPOINT_URL", "http://minio:9000")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "minioadmin123")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "my-audit-evidence")
    S3_REGION: str = os.getenv("S3_REGION", "me-central2")

    # التخزين المؤقت والمهام الخلفية (Redis Cache & Queue)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    # الأمان السحابي والتوثيق (JWT & OAuth2)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my-audit-enterprise-super-secret-key-2026-sa")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12 # 12 hours

    # نطاقات CORS المصرح بها
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")

settings = CloudSettings()
