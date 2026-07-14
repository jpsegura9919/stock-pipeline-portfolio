# 📈 Stock Market ETL Pipeline

Pipeline automatizada de datos financieros internacionales construida con Python, PostgreSQL y Power BI.

## 🎯 Objetivo

Demostrar un flujo completo de ingeniería de datos: desde la extracción de datos en tiempo real hasta la visualización interactiva, con automatización en producción.

## 🏗️ Arquitectura

```
Yahoo Finance (yfinance)
        ↓
Python ETL (extract → transform → load)
        ↓
PostgreSQL (Neon Cloud)
        ↓
GitHub Actions (ejecución diaria automatizada)
        ↓
Power BI Service (dashboard con refresco automático)
```

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Extracción | Python · yfinance |
| Transformación | pandas · numpy |
| Almacenamiento | PostgreSQL · Neon |
| Orquestación | GitHub Actions |
| Visualización | Power BI Service |

## 📊 Métricas calculadas

- **Variación diaria %** — rendimiento respecto al cierre anterior
- **Media móvil 7 días** — tendencia a corto plazo
- **Media móvil 30 días** — tendencia a medio plazo
- **Volatilidad anualizada** — desviación estándar de retornos en 30 días
- **RSI 14** — índice de fuerza relativa (señal de sobrecompra/venta)

## 🌍 Cobertura

~100 tickers internacionales organizados por región:

- 🇺🇸 **USA** — Big Tech, Finanzas, Consumo (AAPL, MSFT, NVDA, JPM, V...)
- 🇪🇺 **Europa** — ASML, SAP, Inditex, BBVA, Airbus, LVMH...
- 🇯🇵🇰🇷🇨🇳 **Asia** — Toyota, Sony, TSMC, Alibaba, Samsung...
- 🌍 **Otros** — Mercadolibre, Infosys, Vale, Shopify...

## 📁 Estructura del proyecto

```
📁 stock-pipeline-portfolio/
├── 📁 etl/
│   ├── extract.py      # Descarga precios desde Yahoo Finance
│   ├── transform.py    # Calcula métricas financieras
│   └── load.py         # Carga con upsert en PostgreSQL
├── 📁 .github/
│   └── 📁 workflows/
│       └── pipeline.yml  # GitHub Action — ejecución diaria
├── main.py             # Orquestador del ETL completo
└── requirements.txt
```

## ⚙️ Pipeline automatizada

El workflow de GitHub Actions se ejecuta automáticamente cada día laborable a las 10:00h (España) y actualiza los datos en PostgreSQL. Power BI Service refresca el dataset diariamente de forma sincronizada.

```yaml
on:
  schedule:
    - cron: "0 8 * * 1-5"  # Lunes a viernes, 8:00 UTC
```

## 🚀 Ejecutar en local

```bash
# 1. Clonar el repositorio
git clone https://github.com/jpsegura9919/stock-pipeline-portfolio.git
cd stock-pipeline-portfolio

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu DATABASE_URL de PostgreSQL

# 4. Ejecutar la pipeline
python main.py
```

## 📊 Dashboard

[🔗 Ver dashboard en Power BI →] https://app.powerbi.com/view?r=eyJrIjoiMWI1ODJhMDgtODVjOC00YTM0LTkxNTItOWU2Y2VkNDViODdlIiwidCI6IjQ3ZTNjY2NhLTFkZTgtNDJlNi1hOTI3LTU5N2UyNTI0YThmZSJ9
---

*Proyecto desarrollado como parte de un portfolio de Data Analytics & Engineering.*
