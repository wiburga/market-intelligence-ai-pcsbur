"""
scraper.py
==========
Módulo de scraping / investigación de mercado.
Actúa como façade de ai_client.py para múltiples consultas batch.
"""

import logging
from typing import Iterator
from ai_client import BlackboxClient

logger = logging.getLogger(__name__)


class MarketScraper:
    """
    Orquesta múltiples consultas a Blackbox AI para un conjunto
    de servicios técnicos, con soporte para ejecución por lotes
    y opcionalmente con pausa entre peticiones.
    """

    def __init__(self, client: BlackboxClient, delay_seconds: float = 2.0):
        """
        Args:
            client: Instancia autenticada de BlackboxClient.
            delay_seconds: Pausa entre peticiones para respetar rate-limits.
        """
        self.client = client
        self.delay  = delay_seconds

    def scrape_services(self, services: list[str]) -> Iterator[dict]:
        """
        Genera resultados uno a uno para cada servicio.
        Usar como generador permite procesar resultados en streaming.

        Args:
            services: Lista de nombres de servicios a investigar.

        Yields:
            dict con la respuesta de Blackbox AI para cada servicio.
        """
        import time
        total = len(services)
        for i, service in enumerate(services, start=1):
            logger.info(f"[Scraper] ({i}/{total}) → {service}")
            try:
                result = self.client.query(service)
                yield result
            except Exception as e:
                logger.error(f"[Scraper] Error en '{service}': {e}")
                yield {"service": service, "raw_response": "", "status": "error"}
            finally:
                if i < total:
                    time.sleep(self.delay)

    def scrape_all(self, services: list[str]) -> list[dict]:
        """Versión que retorna todos los resultados de una vez."""
        return list(self.scrape_services(services))
