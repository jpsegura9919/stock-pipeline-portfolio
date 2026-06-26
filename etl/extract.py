"""
extract.py
Descarga precios históricos diarios desde Yahoo Finance.
Mix internacional de ~100 tickers.
"""

import time
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

TICKERS = [
    # USA — Big Tech
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO",
    "ORCL", "ADBE", "CRM", "AMD", "INTC", "QCOM", "TXN", "IBM",
    "CSCO", "NFLX", "UBER", "PYPL",

    # USA — Finanzas y consumo
    "JPM", "BAC", "GS", "MS", "V", "MA", "BRK-B", "WMT",
    "COST", "HD", "MCD", "KO", "PEP", "JNJ", "PFE", "UNH",
    "XOM", "CVX", "BA", "CAT",

    # Europa
    "ASML", "SAP", "MC.PA", "ITX.MC", "SIE.DE", "BBVA.MC", "SAN.MC",
    "TTE.PA", "AIR.PA", "NESN.SW", "ROG.SW", "NVS", "VOW3.DE", "BMW.DE",
    "RMS.PA", "OR.PA", "ULVR.L", "AZN", "HSBC", "SHEL",

    # Asia
    "TM", "SONY", "TSM", "BABA", "TCEHY", "BIDU", "NTDOY",
    "HMC", "SFTBY", "HYMTF", "NTTYY", "MSBHF",

    # Otros mercados
    "INFY", "VALE", "PBR", "SHOP", "MELI", "BHP", "RIO",
]


def extract_prices(tickers: list[str] = TICKERS, days: int = 90) -> pd.DataFrame:
    """
    Descarga los precios de cierre de los últimos `days` días para cada ticker.
    Incluye pausas para evitar rate limiting con listas grandes.
    Devuelve un DataFrame con columnas: date, ticker, open, high, low, close, volume.
    """
    end = datetime.today()
    start = end - timedelta(days=days)

    frames = []
    errors = []

    for i, ticker in enumerate(tickers):
        print(f"  → [{i+1}/{len(tickers)}] Descargando {ticker}...")

        try:
            info = yf.Ticker(ticker).fast_info
            currency = getattr(info, "currency", "N/A") or "N/A"

            raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

            if raw.empty:
                print(f"  ⚠️  Sin datos para {ticker}, se omite.")
                errors.append(ticker)
                continue

            # Aplanar columnas multi-nivel si existen
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = raw.columns.get_level_values(0)

            raw = raw.reset_index()
            raw.columns = [c.lower() for c in raw.columns]
            raw["ticker"] = ticker
            raw["currency"] = currency
            raw = raw.rename(columns={"index": "date"})
            raw = raw[["date", "ticker", "currency", "open", "high", "low", "close", "volume"]]
            raw["date"] = pd.to_datetime(raw["date"]).dt.date

            print(f"     Divisa: {currency}")
            frames.append(raw)

        except Exception as e:
            print(f"  ❌ Error en {ticker}: {e}")
            errors.append(ticker)

        # Pausa cada 10 tickers para evitar rate limiting
        if (i + 1) % 10 == 0:
            print(f"  ⏳ Pausa breve para evitar rate limiting...")
            time.sleep(2)

    if not frames:
        raise ValueError("No se pudo descargar ningún ticker.")

    if errors:
        print(f"\n  ⚠️  Tickers sin datos ({len(errors)}): {', '.join(errors)}")

    df = pd.concat(frames, ignore_index=True)
    print(f"\n  ✅ Extracción completada: {len(df)} filas, {df['ticker'].nunique()} tickers.")
    return df
