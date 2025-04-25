
import json
import requests
from bs4 import BeautifulSoup

currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']
mock_rates_from_hkd = {}

# Step 1: 爬蟲抓取 yoyorate.com 的 HKD 匯率資料
try:
    url = "https://www.yoyorate.com/hk"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 2: 擷取牌價表格中 HKD 匯率對其他貨幣（預期格式：HKD→xxx）
    table = soup.find("table", class_="ratetable")
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            currency = cols[0].text.strip().replace("→", "").replace("HKD", "").strip()
            if currency == "":
                continue
            if currency == "RMB":
                currency = "CNY"
            elif currency == "NTD":
                currency = "TWD"
            rate_text = cols[2].text.strip().replace(",", "")
            try:
                rate = float(rate_text)
                if currency in currencies:
                    mock_rates_from_hkd[currency] = rate
            except:
                pass

    # HKD 對 HKD 是 1
    mock_rates_from_hkd["HKD"] = 1.0

except Exception as e:
    print("❌ 爬蟲失敗:", e)
    # fallback
    mock_rates_from_hkd = {
        "HKD": 1.0,
        "CNY": 0.92,
        "USD": 0.13,
        "TWD": 4.2,
        "JPY": 19.3,
        "KRW": 170.8,
        "EUR": 0.12
    }

# Step 3: 建立 7x7 匯率矩陣
rates = {}
for base in currencies:
    rates[base] = {}
    for target in currencies:
        if base == target:
            rates[base][target] = 1.0
        else:
            try:
                rate = mock_rates_from_hkd[target] / mock_rates_from_hkd[base]
                rates[base][target] = round(rate, 6)
            except:
                rates[base][target] = 0.0

# Step 4: 輸出到 public/rates.json
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(rates, f, ensure_ascii=False, indent=2)

print("✅ 匯率更新完成")
