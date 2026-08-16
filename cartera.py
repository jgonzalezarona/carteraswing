# -*- coding: utf-8 -*-
"""
cartera_update.py — Genera el JSON de actualización semanal para Cartera Swing
"""

import json
import os
import requests
import yfinance as yf

UPDATER_FILE = "cartera_update.json"

def main():
    swing_data = {}
    if os.path.exists("swing_data.json"):
        with open("swing_data.json", "r", encoding="utf-8") as f:
            swing_data = json.load(f)
    
    stocks = swing_data.get("stocks", [])
    universe_size = swing_data.get("universe_size", 578)
    pasan = sum(1 for s in stocks if s.get("trend_template"))
    
    stock_map = {s["ticker"]: s for s in stocks}
    
    # Obtención del tipo de cambio EUR/USD
    eurusd = 1.09
    try:
        fx = yf.Ticker("EURUSD=X").history(period="1d")
        if not fx.empty:
            eurusd = float(fx["Close"].iloc[-1])
    except Exception:
        pass

    active_tickers = ["VLO", "NTAP", "PANW", "CRL", "DELL", "APH", "CNC", "DXCM", "CRWD", "FCX", "IDR.MC", "GRMN"]
    
    valores = {}
    for tk in active_tickers:
        if tk in stock_map:
            item = stock_map[tk]
            c = item.get("close", 0)
            ema21 = item.get("ema21", 0)
            tt = item.get("trend_template", False)
            rs = item.get("rs", 0)
            earn = item.get("days_to_earnings")

            valores[tk] = {
                "ema21_ok": c >= ema21,
                "trend_template": tt,
                "rs_ok": rs >= 60,
                "earnings_dias": earn,
                "cierre": c,
                "divisa": "EUR" if tk.endswith(".MC") else "USD"
            }

    out_data = {
        "generado": swing_data.get("generated"),
        "eurusd": round(eurusd, 4),
        "amplitud": {
            "pasan": pasan,
            "total": universe_size
        },
        "valores": valores
    }

    with open(UPDATER_FILE, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Archivo {UPDATER_FILE} generado correctamente.")

if __name__ == "__main__":
    main()
