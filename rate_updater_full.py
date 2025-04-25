import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']

# 根據 yoyorate 或其他來源模擬的部分匯率（以 HKD 為 base）
mock_rates = {
    "HKD": {
        "CNY": 0.92,
        "USD": 0.13,
        "TWD": 4.2,
        "JPY": 19.3,
        "KRW": 170.8,
        "EUR": 0.12
    }
}

# 自己兌自己 = 1.0
for c in currencies:
    if c not in mock_rates:
        mock_rates[c] = {}
    mock_rates[c][c] = 1.0

# 補完 HKD 雙向兌換率
for target, rate in mock_rates["HKD"].items():
    if target not in mock_rates:
        mock_rates[target] = {}
    mock_rates[target]["HKD"] = round(1 / rate, 6)

# 推算其他幣種之間的兌換率 A→B = A→HKD × HKD→B
for base in currencies:
    for target in currencies:
        if base == target:
            continue
        if (
            base in mock_rates and
            "HKD" in mock_rates[base] and
            target in mock_rates["HKD"]
        ):
            try:
                rate = mock_rates[base]["HKD"] * mock_rates["HKD"][target]
                mock_rates[base][target] = round(rate, 6)
            except:
                pass

# 寫入 JSON
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(mock_rates, f, ensure_ascii=False, indent=2)