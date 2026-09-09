# ==============================================================================
# My Audit Cloud-Native Dockerfile (Production Multi-Stage Build)
# ==============================================================================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Stage
FROM python:3.11-slim

WORKDIR /app

# إنشاء مستخدم آمن غير جذري (Non-root user) للامتثال الأمني
RUN groupadd -r myaudit && useradd -r -g myaudit myaudit \
    && mkdir -p /app/data /app/storage \
    && chown -R myaudit:myaudit /app

COPY --from=builder /root/.local /home/myaudit/.local
ENV PATH=/home/myaudit/.local/bin:$PATH

COPY . .
RUN chown -R myaudit:myaudit /app

USER myaudit

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    MY_AUDIT_DB=/app/data/my_audit_cloud.db

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "my_audit.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
