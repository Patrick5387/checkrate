
import requests
from bs4 import BeautifulSoup
import json

# 支援幣種
currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']
mock_rates = {}

# 1. 從 yoyorate.com 爬取 HKD 對其他幣種的匯率
url = "https://www.yoyorate.com/hkd"
resp = requests.get(url, timeout=10)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

rows = soup.select("table tr")[1:]
for row in rows:
    cols = row.text.strip().split()
    if len(cols) >= 3:
        code = cols[0]
        try:
            rate = float(cols[2])
            if code in currencies and code != "HKD":
                mock_rates[code] = rate
        except:
            continue

# 加入 HKD 自己
mock_rates["HKD"] = 1.0

# 2. 建立 7x7 匯率矩陣
matrix = {}
for base in currencies:
    matrix[base] = {}
    for target in currencies:
        if base == target:
            matrix[base][target] = 1.0
        else:
            try:
                rate = mock_rates[target] / mock_rates[base]
                matrix[base][target] = round(rate, 6)
            except:
                matrix[base][target] = 0.0

# 3. 寫入 public/rates.json
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, ensure_ascii=False, indent=2)
