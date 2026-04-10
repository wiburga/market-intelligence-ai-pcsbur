"""
config.py
=========
Configuración centralizada del proyecto.
Carga variables de entorno y define rutas globales.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# ── Carga de Variables de Entorno ─────────────────────────────────────────────
# Busca .env en la raíz (un nivel arriba de /src)
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# ── API de Blackbox AI ────────────────────────────────────────────────────────
# Se espera que la clave venga sin el prefijo 'sk-' (se agrega si falta)
RAW_API_KEY = os.getenv("BLACKBOX_API_KEY", "")
BLACKBOX_API_KEY = f"sk-{RAW_API_KEY}" if RAW_API_KEY and not RAW_API_KEY.startswith("sk-") else RAW_API_KEY

BLACKBOX_MODEL = os.getenv("BLACKBOX_MODEL", "blackboxai/blackbox-pro")
BLACKBOX_API_URL = "https://api.blackbox.ai/chat/completions"

# ── Rutas de Datos ────────────────────────────────────────────────────────────
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"

# Asegurar que los directorios existan
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logging():
    """Configuración global del logger."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

# ── Validación de Configuración ───────────────────────────────────────────────
def validate_config():
    """Verifica que las variables críticas existan."""
    if not BLACKBOX_API_KEY:
        raise ValueError(
            "ERROR: BLACKBOX_API_KEY no encontrada. "
            "Asegúrate de tener un archivo .env configurado."
        )
