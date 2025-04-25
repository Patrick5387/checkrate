
import requests
from bs4 import BeautifulSoup
import json

currencies = ['HKD', 'CNY', 'USD', 'TWD', 'JPY', 'KRW', 'EUR']
mock_rates_from_hkd = {}

# 從 yoyorate.com 爬出 HKD 兌換其他幣種的匯率
url = 'https://www.yoyorate.com/hkd'
res = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

table = soup.find('table', class_='table table-sm table-hover')
rows = table.find_all('tr')[1:]  # Skip header

for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 2:
        code = cols[0].text.strip()
        try:
            rate = float(cols[1].text.strip())
        except:
            continue
        if code in currencies and code != 'HKD':
            mock_rates_from_hkd[code] = rate

# 人民幣等於自己
mock_rates_from_hkd['HKD'] = 1.0

# 建立完整 7x7 匯率矩陣
rates = {}
for base in currencies:
    rates[base] = {}
    for target in currencies:
        if base == target:
            rates[base][target] = 1.0
        else:
            try:
                # A-B = A-HKD x HKD-B
                rate = (1 / mock_rates_from_hkd[base]) * mock_rates_from_hkd[target]
                rates[base][target] = round(rate, 6)
            except:
                rates[base][target] = 0.0

# 寫入 public/rates.json
with open("public/rates.json", "w", encoding="utf-8") as f:
    json.dump(rates, f, ensure_ascii=False, indent=2)
