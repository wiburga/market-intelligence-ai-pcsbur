# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile — market-intelligence-ai-pcsbur
# Base image: Python 3.12 slim para imagen mínima y segura
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS base

# Metadatos de la imagen
LABEL maintainer="pcsbur"
LABEL description="Market Intelligence AI — Investigación de precios en Calderón, Quito"
LABEL version="1.0.0"

# Variables de entorno para Python (sin buffers, sin .pyc)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── Directorio de trabajo ─────────────────────────────────────────────────────
WORKDIR /app

# ── Instalación de dependencias ───────────────────────────────────────────────
# Copiamos requirements primero para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ── Código fuente ─────────────────────────────────────────────────────────────
COPY src/ ./src/

# ── Directorio de salida (datos generados se montan como volumen) ──────────────
RUN mkdir -p data/output

# ── Usuario no-root por seguridad ─────────────────────────────────────────────
RUN useradd --no-create-home --shell /bin/false appuser && \
    chown -R appuser:appuser /app
USER appuser

# ── Exponer puerto de Streamlit ───────────────────────────────────────────────
EXPOSE 8501

# ── Salud del contenedor ──────────────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ── Comando por defecto ───────────────────────────────────────────────────────
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
