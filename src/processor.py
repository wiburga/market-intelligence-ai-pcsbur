"""
processor.py
============
Transforma las respuestas de la IA (texto/JSON) en estructuras
tabulares y las exporta a CSV y Excel usando Pandas.
"""

import re
import json
import logging
import pandas as pd
from datetime import date
from pathlib import Path
from typing import Any

from config import OUTPUT_DIR

logger = logging.getLogger(__name__)

# OUTPUT_DIR se maneja desde config.py


class DataProcessor:
    """Convierte respuestas de Blackbox AI en datasets estructurados."""

    def __init__(self):
        self.records: list[dict] = []

    # ── Parsing ───────────────────────────────────────────────────────────────
    def parse_response(self, ai_result: dict) -> list[dict]:
        """
        Parsea la respuesta cruda del cliente de IA.

        Estrategia:
          1. Intenta extraer JSON directamente.
          2. Busca bloques ```json ... ``` con regex.
          3. Si falla, guarda la respuesta como texto plano.

        Returns:
            Lista de registros listos para DataFrame.
        """
        service      = ai_result.get("service", "desconocido")
        raw_response = ai_result.get("raw_response", "")
        status       = ai_result.get("status", "error")

        if status == "error" or not raw_response:
            logger.warning(f"[Processor] Sin respuesta válida para '{service}'.")
            return [self._fallback_record(service, raw_response)]

        # Intento 1: JSON directo
        try:
            parsed = json.loads(raw_response)
            return self._normalize(parsed, service)
        except json.JSONDecodeError:
            pass

        # Intento 2: extraer bloque ```json ... ```
        match = re.search(r"```json\s*(.*?)\s*```", raw_response, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                return self._normalize(parsed, service)
            except json.JSONDecodeError:
                pass

        # Intento 3: buscar cualquier objeto JSON en el texto
        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
                return self._normalize(parsed, service)
            except json.JSONDecodeError:
                pass

        # Fallback: texto plano
        logger.warning(f"[Processor] No se pudo parsear JSON para '{service}'. Guardando como texto.")
        return [self._fallback_record(service, raw_response)]

    # ── Normalización ─────────────────────────────────────────────────────────
    def _normalize(self, data: dict, service: str) -> list[dict]:
        """Aplana el JSON de la IA a filas planas."""
        rows = []
        resultados = data.get("resultados", [])

        if not resultados:
            return [self._fallback_record(service, json.dumps(data, ensure_ascii=False))]

        for item in resultados:
            rows.append({
                "servicio":        data.get("servicio", service),
                "ubicacion":       data.get("ubicacion", "Calderón, Quito, Ecuador"),
                "moneda":          data.get("moneda", "USD"),
                "proveedor":       item.get("proveedor", "N/A"),
                "precio_min_usd":  self._to_float(item.get("precio_min", 0)),
                "precio_max_usd":  self._to_float(item.get("precio_max", 0)),
                "precio_prom_usd": self._to_float(item.get("precio_promedio", 0)),
                "descripcion":     item.get("descripcion", ""),
                "fuente":          item.get("fuente", ""),
                "resumen_mercado": data.get("resumen_mercado", ""),
                "fecha_consulta":  data.get("fecha_consulta", str(date.today())),
            })
        return rows

    def _fallback_record(self, service: str, raw: str) -> dict:
        return {
            "servicio":        service,
            "ubicacion":       "Calderón, Quito, Ecuador",
            "moneda":          "USD",
            "proveedor":       "Sin datos estructurados",
            "precio_min_usd":  0.0,
            "precio_max_usd":  0.0,
            "precio_prom_usd": 0.0,
            "descripcion":     raw[:500],
            "fuente":          "",
            "resumen_mercado": "",
            "fecha_consulta":  str(date.today()),
        }

    @staticmethod
    def _to_float(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    # ── Acumulación ───────────────────────────────────────────────────────────
    def add_results(self, records: list[dict]) -> None:
        self.records.extend(records)

    # ── Exportación ───────────────────────────────────────────────────────────
    def export(self, filename_base: str = "market_research") -> dict[str, Path]:
        """
        Exporta los registros acumulados a CSV y Excel.

        Args:
            filename_base: Prefijo del nombre del archivo de salida.

        Returns:
            Dict con rutas de los archivos generados.
        """
        if not self.records:
            logger.warning("[Processor] No hay datos para exportar.")
            return {}

        df = pd.DataFrame(self.records)
        df = df.sort_values(["servicio", "precio_prom_usd"]).reset_index(drop=True)

        today      = date.today().isoformat()
        csv_path   = OUTPUT_DIR / f"{filename_base}_{today}.csv"
        excel_path = OUTPUT_DIR / f"{filename_base}_{today}.xlsx"

        # CSV
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info(f"[Processor] CSV exportado: {csv_path}")

        # Excel con formato
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Precios_Mercado", index=False)
            self._format_excel(writer, df)
        logger.info(f"[Processor] Excel exportado: {excel_path}")

        return {"csv": csv_path, "excel": excel_path}

    @staticmethod
    def _format_excel(writer: pd.ExcelWriter, df: pd.DataFrame) -> None:
        """Aplica formato básico de ancho de columnas al Excel."""
        worksheet = writer.sheets["Precios_Mercado"]
        for col_idx, col_name in enumerate(df.columns, start=1):
            max_len = max(df[col_name].astype(str).map(len).max(), len(col_name)) + 4
            col_letter = worksheet.cell(row=1, column=col_idx).column_letter
            worksheet.column_dimensions[col_letter].width = min(max_len, 60)
