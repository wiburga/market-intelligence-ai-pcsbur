"""
ai_client.py
============
Cliente HTTP para la API de Blackbox AI.
Gestiona autenticación, construcción de prompts y reintentos.
"""

import os
import time
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────
BLACKBOX_API_URL = "https://api.blackbox.ai/chat/completions"
DEFAULT_MODEL    = "blackboxai/blackbox-pro"
MAX_RETRIES      = 3
RETRY_DELAY_S    = 2


class BlackboxClient:
    """Wrapper sobre la API REST de Blackbox AI."""

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.getenv("BLACKBOX_API_KEY", "")
        # Asegurar prefijo sk- si se usa el endpoint api.blackbox.ai
        if self.api_key and not self.api_key.startswith("sk-"):
            self.api_key = f"sk-{self.api_key}"
            
        self.model   = model
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        })

    # ── Prompt Engineering ────────────────────────────────────────────────────
    def build_market_research_prompt(self, service: str) -> str:
        """
        Construye un prompt altamente específico para investigación de precios
        en el sector de Calderón, Quito, Ecuador (moneda USD).
        """
        return (
            f"Eres un investigador de mercado especializado en servicios técnicos de "
            f"computadoras en Calderón, Quito, Ecuador.\n\n"
            f"Busca y analiza los PRECIOS ACTUALES (en dólares americanos USD $) del "
            f"siguiente servicio técnico ofrecido por negocios locales en el sector "
            f"de Calderón, Quito, Ecuador:\n\n"
            f"  SERVICIO: {service}\n\n"
            f"Instrucciones de respuesta:\n"
            f"1. Busca precios reales publicados en internet (redes sociales, páginas web, "
            f"   grupos de Facebook, OLX Ecuador, Marketplace de Ecuador).\n"
            f"2. Devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:\n"
            f"{{\n"
            f"  \"servicio\": \"{service}\",\n"
            f"  \"ubicacion\": \"Calderón, Quito, Ecuador\",\n"
            f"  \"moneda\": \"USD\",\n"
            f"  \"resultados\": [\n"
            f"    {{\n"
            f"      \"proveedor\": \"Nombre del negocio o referencia\",\n"
            f"      \"precio_min\": 0.00,\n"
            f"      \"precio_max\": 0.00,\n"
            f"      \"precio_promedio\": 0.00,\n"
            f"      \"descripcion\": \"Detalle del servicio incluido\",\n"
            f"      \"fuente\": \"URL o red social donde se encontró\"\n"
            f"    }}\n"
            f"  ],\n"
            f"  \"resumen_mercado\": \"Análisis breve del rango de precios del mercado local\",\n"
            f"  \"fecha_consulta\": \"YYYY-MM-DD\"\n"
            f"}}\n\n"
            f"3. Si no encuentras información específica de Calderón, amplía a Quito Norte.\n"
            f"4. NO inventes precios. Si no hay datos reales, indica precio_min y precio_max en 0.\n"
            f"5. Responde SOLO con el JSON, sin texto adicional."
        )

    # ── Llamada a la API ──────────────────────────────────────────────────────
    def query(self, service: str) -> dict:
        """
        Envía el prompt a Blackbox AI y retorna la respuesta parseada.

        Args:
            service: Nombre del servicio técnico a investigar.

        Returns:
            dict con la respuesta de la IA (ya sea JSON estructurado o texto plano).
        """
        prompt = self.build_market_research_prompt(service)
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": self.model,
            "stream": False,
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"[Blackbox] Consultando servicio: '{service}' (intento {attempt}/{MAX_RETRIES})")
                response = self.session.post(BLACKBOX_API_URL, json=payload, timeout=60)
                response.raise_for_status()

                data = response.json()
                content = self._extract_content(data)
                logger.info(f"[Blackbox] Respuesta recibida para '{service}'.")
                return {"service": service, "raw_response": content, "status": "ok"}

            except requests.exceptions.HTTPError as e:
                logger.error(f"[Blackbox] HTTP {response.status_code}: {e}")
                if response.status_code in (401, 403):
                    raise PermissionError("API Key inválida o sin permisos. Revisa BLACKBOX_API_KEY en tu .env") from e
                if attempt == MAX_RETRIES:
                    raise
            except requests.exceptions.RequestException as e:
                logger.warning(f"[Blackbox] Error de conexión (intento {attempt}): {e}")
                if attempt == MAX_RETRIES:
                    raise
            time.sleep(RETRY_DELAY_S * attempt)

        return {"service": service, "raw_response": "", "status": "error"}

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _extract_content(response_data: dict) -> str:
        """Extrae el texto del mensaje de la respuesta de Blackbox."""
        try:
            # Estructura típica OpenAI-compatible
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            pass
        # Fallback: campo 'response' directo
        return response_data.get("response", str(response_data))
