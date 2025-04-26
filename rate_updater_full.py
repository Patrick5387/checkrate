import json
import requests
from datetime import datetime

currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']

# Step 1: 去 exchangerate.host 取實時匯率
url = "https://api.exchangerate.host/latest"
params = {
    "base": "HKD",
    "symbols": ",".join(currencies)
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    rates_from_hkd = data.get("rates", {})

    if not rates_from_hkd:
        raise ValueError("API回傳資料異常")
except Exception as e:
    print("❌ 爬蟲失敗，錯誤：", e)
    rates_from_hkd = {
        "HKD": 1.0,
        "CNY": 0.92,
        "USD": 0.13,
        "TWD": 4.2,
        "JPY": 19.3,
        "KRW": 170.8,
        "EUR": 0.12
    }

# Step 2: 建立 7x7 匯率矩陣
rates = {}
for base in currencies:
    rates[base] = {}
    for target in currencies:
        if base == target:
            rates[base][target] = 1.0
        else:
            try:
                rate = rates_from_hkd[target] / rates_from_hkd[base]
                rates[base][target] = round(rate, 6)
            except:
                rates[base][target] = 0.0

# Step 3: 寫入 public/rates.json
output = {
    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "rates": rates
}

with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 匯率更新完成")