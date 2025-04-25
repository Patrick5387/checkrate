import json\nfrom datetime import datetime\n\n# 以下內容為模擬真實爬蟲輸出（正式版本可加入 requests + BeautifulSoup）\noutput = {
  "update_time": "2025-04-25 06:39:16",
  "rates": {
    "HKD": {
      "USD": 0.128,
      "JPY": 19.3,
      "CNY": 0.91,
      "KRW": 167.5,
      "EUR": 0.116,
      "TWD": 4.1
    },
    "USD": {
      "HKD": 7.82,
      "JPY": 151.8,
      "EUR": 0.92,
      "CNY": 7.2
    },
    "CNY": {
      "HKD": 1.09,
      "USD": 0.139
    },
    "JPY": {
      "HKD": 0.0518
    },
    "KRW": {
      "HKD": 0.0059
    },
    "EUR": {
      "HKD": 8.58
    },
    "TWD": {
      "HKD": 0.243
    }
  },
  "hk_shops": [
    {
      "name": "永昌找換（旺角）",
      "rates": {
        "USD": 0.127,
        "JPY": 19.2,
        "EUR": 0.115,
        "KRW": 166,
        "TWD": 4.0
      }
    },
    {
      "name": "金龍找換（尖沙咀）",
      "rates": {
        "USD": 0.128,
        "JPY": 19.3,
        "EUR": 0.116,
        "KRW": 167,
        "TWD": 4.1
      }
    }
  ],
  "cards": [
    {
      "name": "Visa（渣打）",
      "rates": {
        "USD": 0.126,
        "JPY": 19.0,
        "EUR": 0.114
      }
    },
    {
      "name": "Mastercard（匯豐）",
      "rates": {
        "USD": 0.127,
        "JPY": 19.1,
        "EUR": 0.115
      }
    }
  ],
  "airports": [
    {
      "name": "東京成田機場",
      "rates": {
        "HKD": 14.5,
        "USD": 0.125,
        "JPY": 18.9
      }
    },
    {
      "name": "首爾仁川機場",
      "rates": {
        "HKD": 14.8,
        "USD": 0.126,
        "KRW": 158
      }
    }
  ]
}\nwith open('public/rates.json', 'w', encoding='utf-8') as f:\n    json.dump(output, f, ensure_ascii=False, indent=2)\nprint('✅ 匯率已更新並寫入 public/rates.json')