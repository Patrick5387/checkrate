import json
from datetime import datetime

currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']

# 模擬以 HKD 為 base 的實際找換店匯率
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

# 初始化所有幣種為空 dict，並設自己兌自己為 1.0
for base in currencies:
    if base not in mock_rates:
        mock_rates[base] = {}
    mock_rates[base][base] = 1.0

# 建立 HKD 雙向反推（補完其他→HKD）
for to_currency, rate in mock_rates["HKD"].items():
    if to_currency not in mock_rates:
        mock_rates[to_currency] = {}
    mock_rates[to_currency]["HKD"] = round(1 / rate, 6)

# 用 HKD 為中介推導所有 A→B 匯率
for base in currencies:
    for target in currencies:
        if base == target:
            continue
        try:
            # 若 base→HKD 與 HKD→target 都有數值，就計出 base→target
            if (
                "HKD" in mock_rates[base] and
                target in mock_rates["HKD"]
            ):
                mock_rates[base][target] = round(
                    mock_rates[base]["HKD"] * mock_rates["HKD"][target], 6
                )
        except Exception as e:
            pass

# 寫入 JSON 檔案
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(mock_rates, f, ensure_ascii=False, indent=2)
