import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# 7 種主要貨幣
currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']

# 模擬從 yoyorate 或其他來源獲得部分匯率（例：HKD 為 base）
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

# 自己兌自己設為 1
for c in currencies:
    if c not in mock_rates:
        mock_rates[c] = {}
    mock_rates[c][c] = 1.0

# 利用 HKD 為中介推導其餘幣種之間的兌換率
for base in currencies:
    for target in currencies:
        if base == target:
            continue
        if base in mock_rates and target in mock_rates["HKD"] and base in mock_rates["HKD"]:
            try:
                # A→C = (A→HKD) * (HKD→C)
                rate = mock_rates["HKD"][target] / mock_rates["HKD"][base]
                mock_rates[base][target] = round(rate, 4)
            except:
                pass

# 輸出 JSON
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(mock_rates, f, ensure_ascii=False, indent=2)
