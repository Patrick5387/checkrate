import { useState, useEffect } from "react";

export default function App() {
  const currencies = {
    HKD: "港幣 HKD",
    CNY: "人民幣 CNY",
    USD: "美元 USD",
    TWD: "台幣 TWD",
    JPY: "日圓 JPY",
    KRW: "韓圓 KRW",
    EUR: "歐元 EUR"
  };

  const [amount, setAmount] = useState(1000);
  const [fromCurrency, setFromCurrency] = useState("HKD");
  const [toCurrency, setToCurrency] = useState("JPY");
  const [rate, setRate] = useState(0);

  useEffect(() => {
    if (fromCurrency === toCurrency) {
      setRate(1);
    } else {
      fetch(`/api/rate?base=${fromCurrency}&target=${toCurrency}`)
        .then((res) => res.json())
        .then((data) => {
          const r = data.rate ?? 0;
          setRate(r);
        });
    }
  }, [fromCurrency, toCurrency]);

  const converted = amount * rate;

  return (
    <div className="p-4 max-w-xl mx-auto text-center space-y-5">
      <h1 className="text-3xl font-bold text-blue-700">CheckRate - 點兌匯率工具</h1>
      <p className="text-sm text-gray-500">查實時匯率、找換店、機場與信用卡兌換比較</p>

      <div className="grid grid-cols-1 gap-3 text-left">
        <label>
          輸入金額 / Amount:
          <input
            type="number"
            className="w-full border rounded px-3 py-2 mt-1"
            value={amount}
            onChange={(e) => setAmount(parseFloat(e.target.value))}
          />
        </label>

        <label>
          輸入幣種 / From:
          <select
            className="w-full border rounded px-3 py-2 mt-1"
            value={fromCurrency}
            onChange={(e) => setFromCurrency(e.target.value)}
          >
            {Object.keys(currencies).map((code) => (
              <option key={code} value={code}>
                {currencies[code]}
              </option>
            ))}
          </select>
        </label>

        <label>
          兌換至 / To:
          <select
            className="w-full border rounded px-3 py-2 mt-1"
            value={toCurrency}
            onChange={(e) => setToCurrency(e.target.value)}
          >
            {Object.keys(currencies).map((code) => (
              <option key={code} value={code}>
                {currencies[code]}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="text-xl font-medium bg-yellow-100 p-3 rounded shadow">
        ≈ {converted.toLocaleString(undefined, { maximumFractionDigits: 2 })} {toCurrency}
      </div>

      <div className="bg-gray-100 p-3 mt-6 rounded text-sm text-center text-gray-400">
        ⓘ 匯率透過 Vercel proxy API 串接 exchangerate.host<br />
        📢 廣告位 / Ad Placeholder
      </div>
    </div>
  );
}