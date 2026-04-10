"""
main.py
=======
Punto de entrada del proyecto market-intelligence-ai-pcsbur.

Flujo:
  1. Carga configuración desde .env
  2. Lee la lista de servicios a investigar
  3. Consulta Blackbox AI para cada servicio
  4. Procesa y exporta los resultados a CSV y Excel
"""

import os
import sys
import logging
from pathlib import Path

from dotenv import load_dotenv

# ── Carga de variables de entorno ─────────────────────────────────────────────
# Busca .env en la raíz del proyecto (un nivel arriba de /src)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/output/run.log", encoding="utf-8", mode="a"),
    ],
)
logger = logging.getLogger("market_intelligence")

# ── Importaciones internas ────────────────────────────────────────────────────
from ai_client import BlackboxClient   # noqa: E402 (después de dotenv)
from processor import DataProcessor    # noqa: E402

# ── Servicios a investigar ────────────────────────────────────────────────────
# Puedes ampliar esta lista sin tocar otra parte del código.
SERVICES = [
    "mantenimiento preventivo de laptop o computadora de escritorio",
    "formateo e instalación de Windows 10 / Windows 11",
    "cambio e instalación de disco duro SSD en laptop",
    "reparación de pantalla de laptop",
    "instalación de programas y antivirus",
]


def main() -> int:
    """Función principal del pipeline de inteligencia de mercado."""
    api_key = os.getenv("BLACKBOX_API_KEY")
    if not api_key:
        logger.error(
            "No se encontró BLACKBOX_API_KEY. "
            "Crea un archivo .env con tu API Key o define la variable de entorno."
        )
        return 1

    logger.info("=" * 60)
    logger.info(" INICIO: Market Intelligence AI — pcsbur")
    logger.info(f" Sector objetivo: Calderón, Quito, Ecuador")
    logger.info(f" Servicios a investigar: {len(SERVICES)}")
    logger.info("=" * 60)

    client    = BlackboxClient(api_key=api_key)
    processor = DataProcessor()

    # ── Bucle principal ────────────────────────────────────────────────────────
    errors = 0
    for i, service in enumerate(SERVICES, start=1):
        logger.info(f"\n[{i}/{len(SERVICES)}] Investigando: '{service}'")
        try:
            ai_result = client.query(service)
            records   = processor.parse_response(ai_result)
            processor.add_results(records)
            logger.info(f"  → {len(records)} registro(s) obtenido(s).")
        except PermissionError as e:
            logger.critical(str(e))
            return 1
        except Exception as e:
            logger.error(f"  → Error inesperado para '{service}': {e}")
            errors += 1

    # ── Exportación ───────────────────────────────────────────────────────────
    logger.info("\n" + "=" * 60)
    logger.info(" EXPORTANDO RESULTADOS…")
    exported = processor.export(filename_base="precios_calderon_quito")

    if exported:
        for fmt, path in exported.items():
            logger.info(f"  ✓ {fmt.upper()}: {path}")
    else:
        logger.warning("  ✗ No se generaron archivos de salida.")

    logger.info("=" * 60)
    logger.info(f" FIN. Errores: {errors}/{len(SERVICES)}")
    logger.info("=" * 60)

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
