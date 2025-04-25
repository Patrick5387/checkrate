
import json
from datetime import datetime
start_time = datetime.now()
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
    rows = table.find_all("tr") if table else[]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            currency = cols[0].text.strip().replace("→", "").replace("HKD", "").strip().upper()
            if currency == "":
                continue
            if currency == "RMB":
                currency = "CNY"
            elif currency == "NTD":
                currency = "TWD"
            try:
                rate_text = cols[2].text.strip()
                rate = float(rate_text.replace(",",""))
                if currency in currencies:
                    mock_rates_from_hkd[currency] = rate
            except Exception as e:
                print(f"❌ 匯率轉換失敗: {e}")
                continue

    # HKD 對 HKD 是 1
    mock_rates_from_hkd["HKD"] = 1.0
    assert mock_rates_from_hkd["HKD"] == 1.0, "HKD 匯率異常，應為 1.0"

except Exception as e:
    print("❌ 爬蟲失敗，使用 fallback：", e)
    # fallback
    print("📦 抓到的 HKD 匯率對：", mock_rates_from_hkd)
    mock_rates_from_hkd = {
        "HKD": 1.0,
        "CNY": 0.92,
        "USD": 0.13,
        "TWD": 4.2,
        "JPY": 19.3,
        "KRW": 170.8,
        "EUR": 0.12
    }
    if len(mock_rates_from_hkd) < 7:
            print("⚠️ 未抓到齊 7 個貨幣，實際抓到：", list(mock_rates_from_hkd.keys()))

            # ⬇️ 可選：發 Telegram / Slack 警告
            # send_warning("抓匯率未齊 7 個貨幣，實際抓到：" + ", ".join(mock_rates_from_hkd.keys()))

            import sys
            sys.exit(1)
    # ⚠️ 未抓到齊 7 個貨幣，實際抓到： ['HKD', 'USD', 'JPY', 'KRW']

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
print("⏱️ 用時：", datetime.now() - start_time)  # 放在 print 完成之後