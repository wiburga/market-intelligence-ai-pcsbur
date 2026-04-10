# 🧠 PCSBUR Market Intelligence Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Blackbox AI](https://img.shields.io/badge/Blackbox-API-000000?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 🇪🇸 Versión en Español

### 🎯 Impacto de Negocio en Calderón
Este proyecto nace para fortalecer la competitividad de **pcsbur** en el sector de Calderón, Quito. Al automatizar la vigilancia de precios técnicos (mantenimientos, formateos, repuestos), el dueño del negocio puede:
- **Ajustar precios** basándose en datos reales de la competencia local.
- **Identificar tendencias** de mercado antes que los demás locales.
- **Optimizar recursos** al dejar que la IA investigue en Marketplace y sitios locales en segundos.

### 🚀 Características
- **IA de Vanguardia**: Utiliza el modelo `blackbox-search` para navegación web en tiempo real.
- **Dashboard Profesional**: Interfaz interactiva para comparar precios mínimos y máximos.
- **Reportes Detallados**: Listas de proveedores encontrados con sus respectivas fuentes.

### ⚙️ Instalación en Windows
1. **Clonar y entrar**:
   ```powershell
   git clone https://github.com/pcsbur/market-intelligence-ai-pcsbur.git
   cd market-intelligence-ai-pcsbur
   ```
2. **Entorno Virtual**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Configurar .env**:
   Copia `.env.example` a `.env` y coloca tu `BLACKBOX_API_KEY`.
5. **Ejecutar**:
   ```powershell
   streamlit run src/app.py
   ```

---

## 🇺🇸 English Version

### 🎯 Business Impact for pcsbur
This tool provides a strategic edge for **pcsbur** in the Calderón area (Quito, Ecuador). By automating technical service price intelligence, the business can:
- **Refine pricing strategies** using local competitor data.
- **Identify gaps** in service offerings within the community.
- **Save hours** of manual research on social media and local marketplaces.

### 🚀 Key Features
- **Real-time Engine**: Powered by Blackbox AI's `blackbox-search` for live web data extraction.
- **Visual Analytics**: Interactive Plotly charts for price range analysis.
- **Actionable Data**: Dynamic table featuring local providers and verifiable source links.

### ⚙️ Quick Installation (Windows/Docker)
1. **Clone & Setup**:
   ```bash
   git clone https://github.com/pcsbur/market-intelligence-ai-pcsbur.git
   cd market-intelligence-ai-pcsbur
   ```
2. **Docker Deployment**:
   ```bash
   docker compose up --build
   ```
   Access at: [http://localhost:8501](http://localhost:8501)

3. **Manual Python Install**:
   Follow the steps in the Spanish section above using `python -m venv` and `pip install`.

---

## 🛠️ Tecnologías / Tech Stack
- **AI Engine**: Blackbox AI REST API
- **Web Interface**: Streamlit
- **Visualization**: Plotly Express
- **Data Engine**: Pandas & OpenPyXL

## 📄 Licencia / License
MIT © 2025 [pcsbur](https://github.com/pcsbur)
