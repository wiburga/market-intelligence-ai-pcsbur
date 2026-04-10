# ─────────────────────────────────────────────────────────────────────────────
# setup.ps1 — Instalador de Prerrequisitos para Windows
# market-intelligence-ai-pcsbur
# ─────────────────────────────────────────────────────────────────────────────
# Ejecutar con: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Market Intelligence AI — pcsbur : Setup de prerrequisitos" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ── Verificar si winget está disponible ───────────────────────────────────────
function Test-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

# ── Instalar Python ───────────────────────────────────────────────────────────
Write-Host "[1/2] Verificando Python..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pyVer = python --version 2>&1
    Write-Host "  ✓ Python ya instalado: $pyVer" -ForegroundColor Green
} else {
    Write-Host "  → Instalando Python 3.12 via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    # Actualizar PATH sin reiniciar terminal
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "  ✓ Python instalado. Reinicia PowerShell si 'python' no se reconoce." -ForegroundColor Green
}

# ── Instalar Docker Desktop ───────────────────────────────────────────────────
Write-Host ""
Write-Host "[2/2] Verificando Docker Desktop..." -ForegroundColor Yellow
if (Test-Command "docker") {
    $dockerVer = docker --version 2>&1
    Write-Host "  ✓ Docker ya instalado: $dockerVer" -ForegroundColor Green
} else {
    Write-Host "  → Instalando Docker Desktop via winget..." -ForegroundColor Yellow
    winget install --id Docker.DockerDesktop --silent --accept-source-agreements --accept-package-agreements
    Write-Host "  ✓ Docker Desktop instalado." -ForegroundColor Green
    Write-Host "  ⚠ IMPORTANTE: Inicia Docker Desktop manualmente antes de ejecutar docker compose up" -ForegroundColor Yellow
}

# ── Instrucciones finales ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup completo. Próximos pasos:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Copia el archivo de ejemplo de variables de entorno:" -ForegroundColor White
Write-Host "     Copy-Item .env.example .env" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Edita .env y agrega tu BLACKBOX_API_KEY:" -ForegroundColor White
Write-Host "     notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Ejecuta con Docker:" -ForegroundColor White
Write-Host "     docker compose up --build" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. O ejecuta localmente (después de instalar Python):" -ForegroundColor White
Write-Host "     python -m venv .venv" -ForegroundColor Gray
Write-Host "     .venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "     python -m pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "     cd src && python main.py" -ForegroundColor Gray
Write-Host ""
