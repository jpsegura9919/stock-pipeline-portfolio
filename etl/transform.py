"""
transform.py
Calcula métricas financieras a partir de los precios crudos.
"""

import pandas as pd
import numpy as np


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe el DataFrame de precios crudos y devuelve un DataFrame
    con las métricas calculadas por ticker y fecha.

    Métricas:
        - daily_change_pct : variación % respecto al cierre anterior
        - ma_7             : media móvil de 7 días
        - ma_30            : media móvil de 30 días
        - volatility_30    : volatilidad (desv. estándar de retornos en 30 días)
        - rsi_14           : RSI de 14 días
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["ticker", "date"])

    results = []

    for ticker, group in df.groupby("ticker"):
        group = group.copy().reset_index(drop=True)

        # Variación diaria %
        group["daily_change_pct"] = group["close"].pct_change() * 100

        # Medias móviles
        group["ma_7"] = group["close"].rolling(window=7).mean()
        group["ma_30"] = group["close"].rolling(window=30).mean()

        # Volatilidad: desv. estándar de retornos diarios en ventana de 30 días
        daily_returns = group["close"].pct_change()
        group["volatility_30"] = daily_returns.rolling(window=30).std() * np.sqrt(252) * 100

        # RSI 14
        group["rsi_14"] = _calculate_rsi(group["close"], window=14)

        results.append(group)

    metrics_df = pd.concat(results, ignore_index=True)

    # Seleccionar columnas finales y redondear
    metrics_df = metrics_df[[
        "date", "ticker", "close",
        "daily_change_pct", "ma_7", "ma_30",
        "volatility_30", "rsi_14"
    ]]

    numeric_cols = ["close", "daily_change_pct", "ma_7", "ma_30", "volatility_30", "rsi_14"]
    metrics_df[numeric_cols] = metrics_df[numeric_cols].round(4)
    metrics_df["date"] = metrics_df["date"].dt.date

    print(f"  ✅ Transformación completada: {len(metrics_df)} filas con métricas.")
    return metrics_df


def _calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Calcula el RSI (Relative Strength Index) para una serie de precios."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.round(2)
