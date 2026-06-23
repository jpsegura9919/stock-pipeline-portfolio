"""
load.py
Carga los DataFrames en PostgreSQL (Neon o cualquier instancia compatible).
Usa upsert para evitar duplicados en ejecuciones repetidas.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    """Crea el engine de SQLAlchemy usando la variable de entorno DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise EnvironmentError("❌ Variable DATABASE_URL no encontrada en .env")
    return create_engine(db_url)


def create_tables(engine):
    """Crea las tablas si no existen."""
    ddl = """
    CREATE TABLE IF NOT EXISTS stock_prices (
        id          SERIAL PRIMARY KEY,
        date        DATE          NOT NULL,
        ticker      VARCHAR(10)   NOT NULL,
        open        NUMERIC(12,4),
        high        NUMERIC(12,4),
        low         NUMERIC(12,4),
        close       NUMERIC(12,4),
        volume      BIGINT,
        UNIQUE (date, ticker)
    );

    CREATE TABLE IF NOT EXISTS stock_metrics (
        id                  SERIAL PRIMARY KEY,
        date                DATE          NOT NULL,
        ticker              VARCHAR(10)   NOT NULL,
        close               NUMERIC(12,4),
        daily_change_pct    NUMERIC(10,4),
        ma_7                NUMERIC(12,4),
        ma_30               NUMERIC(12,4),
        volatility_30       NUMERIC(10,4),
        rsi_14              NUMERIC(8,2),
        UNIQUE (date, ticker)
    );
    """
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()
    print("  ✅ Tablas verificadas / creadas.")


def load_prices(df: pd.DataFrame, engine):
    """
    Upsert de precios crudos en stock_prices.
    Si ya existe el par (date, ticker), actualiza los valores.
    """
    records = df.to_dict(orient="records")
    upsert_sql = text("""
        INSERT INTO stock_prices (date, ticker, open, high, low, close, volume)
        VALUES (:date, :ticker, :open, :high, :low, :close, :volume)
        ON CONFLICT (date, ticker) DO UPDATE SET
            open   = EXCLUDED.open,
            high   = EXCLUDED.high,
            low    = EXCLUDED.low,
            close  = EXCLUDED.close,
            volume = EXCLUDED.volume
    """)
    with engine.connect() as conn:
        conn.execute(upsert_sql, records)
        conn.commit()
    print(f"  ✅ stock_prices: {len(records)} filas cargadas (upsert).")


def load_metrics(df: pd.DataFrame, engine):
    """
    Upsert de métricas en stock_metrics.
    """
    records = df.to_dict(orient="records")
    upsert_sql = text("""
        INSERT INTO stock_metrics (date, ticker, close, daily_change_pct, ma_7, ma_30, volatility_30, rsi_14)
        VALUES (:date, :ticker, :close, :daily_change_pct, :ma_7, :ma_30, :volatility_30, :rsi_14)
        ON CONFLICT (date, ticker) DO UPDATE SET
            close            = EXCLUDED.close,
            daily_change_pct = EXCLUDED.daily_change_pct,
            ma_7             = EXCLUDED.ma_7,
            ma_30            = EXCLUDED.ma_30,
            volatility_30    = EXCLUDED.volatility_30,
            rsi_14           = EXCLUDED.rsi_14
    """)
    with engine.connect() as conn:
        conn.execute(upsert_sql, records)
        conn.commit()
    print(f"  ✅ stock_metrics: {len(records)} filas cargadas (upsert).")
