"""
extract.py
Descarga precios históricos diarios desde Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"]


def extract_prices(tickers: list[str] = TICKERS, days: int = 90) -> pd.DataFrame:
    """
    Descarga los precios de cierre de los últimos `days` días para cada ticker.
    Devuelve un DataFrame con columnas: date, ticker, open, high, low, close, volume.
    """
    end = datetime.today()
    start = end - timedelta(days=days)

    frames = []
    for ticker in tickers:
        print(f"  → Descargando {ticker}...")
        raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

        if raw.empty:
            print(f"  ⚠️  Sin datos para {ticker}, se omite.")
            continue

        # Aplanar columnas multi-nivel si existen
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)

        raw = raw.reset_index()
        raw.columns = [c.lower() for c in raw.columns]
        raw["ticker"] = ticker
        raw = raw.rename(columns={"index": "date"})

        # Seleccionar y ordenar columnas
        raw = raw[["date", "ticker", "open", "high", "low", "close", "volume"]]
        raw["date"] = pd.to_datetime(raw["date"]).dt.date

        frames.append(raw)

    if not frames:
        raise ValueError("No se pudo descargar ningún ticker.")

    df = pd.concat(frames, ignore_index=True)
    print(f"  ✅ Extracción completada: {len(df)} filas, {df['ticker'].nunique()} tickers.")
    return df
