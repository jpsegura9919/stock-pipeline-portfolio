"""
main.py
Orquesta el pipeline ETL completo: Extract → Transform → Load.
Puede ejecutarse manualmente o desde GitHub Actions.
"""

import sys
import traceback
from datetime import datetime

from etl.extract import extract_prices
from etl.transform import calculate_metrics
from etl.load import get_engine, create_tables, load_prices, load_metrics


def run_pipeline():
    start_time = datetime.now()
    print(f"\n{'='*50}")
    print(f"🚀 Pipeline iniciada: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    try:
        # 1. EXTRACT
        print("📥 [1/3] Extrayendo datos de Yahoo Finance...")
        prices_df = extract_prices()

        # 2. TRANSFORM
        print("\n⚙️  [2/3] Calculando métricas financieras...")
        metrics_df = calculate_metrics(prices_df)

        # 3. LOAD
        print("\n💾 [3/3] Cargando datos en PostgreSQL...")
        engine = get_engine()
        create_tables(engine)
        load_prices(prices_df, engine)
        load_metrics(metrics_df, engine)

    except Exception as e:
        print(f"\n❌ Error en la pipeline: {e}")
        traceback.print_exc()
        sys.exit(1)

    elapsed = (datetime.now() - start_time).seconds
    print(f"\n{'='*50}")
    print(f"✅ Pipeline completada en {elapsed}s")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    run_pipeline()
