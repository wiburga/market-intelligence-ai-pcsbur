"""
ai_engine.py
============
Motor de inteligencia basado en Blackbox AI.
"""

import os
import json
import logging
import requests
from typing import Optional, List, Dict

from config import BLACKBOX_API_URL, BLACKBOX_API_KEY, BLACKBOX_MODEL

logger = logging.getLogger(__name__)

# Configuración centralizada en config.py

class AIEngine:
    """Cliente especializado en inteligencia de mercado técnico."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or BLACKBOX_API_KEY
        self.model = model or BLACKBOX_MODEL
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })

    def get_market_data(self, service: str) -> Dict:
        """
        Consulta a Blackbox AI y fuerza respuesta JSON estructurada.
        """
        prompt = (
            f"Actúa como un experto consultor de mercado en Quito, Ecuador.\n"
            f"Investiga el precio actual del servicio técnico: '{service}' "
            f"específicamente en el sector de CALDERÓN y norte de Quito.\n\n"
            f"Busca en Marketplace, OLX y sitios locales los precios actuales de 2025/2026.\n\n"
            f"Devuelve estrictamente un JSON con esta estructura:\n"
            f"{{\n"
            f"  \"servicio\": \"{service}\",\n"
            f"  \"ubicacion\": \"Calderón, Quito\",\n"
            f"  \"resultados\": [\n"
            f"    {{\"proveedor\": \"nombre\", \"precio_min\": 0.0, \"precio_max\": 0.0, \"precio_promedio\": 0.0, \"descripcion\": \"...\", \"fuente\": \"...\"}}\n"
            f"  ],\n"
            f"  \"resumen_mercado\": \"análisis breve\",\n"
            f"  \"fecha_consulta\": \"2026-04-09\"\n"
            f"}}\n"
            f"Responde SOLO el JSON."
        )

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
            "stream": False
        }

        try:
            logger.info(f"Consultando IA para: {service}")
            response = self.session.post(BLACKBOX_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            return {
                "service": service,
                "raw_response": content,
                "status": "ok"
            }
        except Exception as e:
            logger.error(f"Error en AI Engine: {e}")
            return {
                "service": service,
                "raw_response": "",
                "status": "error",
                "message": str(e)
            }
