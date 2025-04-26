
import { useEffect, useState } from "react";

export default function App() {
  const [amount, setAmount] = useState(1000);
  const [from, setFrom] = useState("HKD");
  const [to, setTo] = useState("JPY");
  const [rate, setRate] = useState(0);
  const [ratesData, setRatesData] = useState({});
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    fetch("/rates.json")
      .then((res) => res.json())
      .then((data) => {
        setRatesData(data);
        setLoaded(true);
        const r = data.rates?.[from]?.[to] ?? 0;
        setRate(r);
      });
  }, [from, to]);

  const converted = amount * rate;

  return (
    <div className="p-4 max-w-2xl mx-auto text-center space-y-6">
      <h1 className="text-3xl font-bold text-blue-700">CheckRate - 點兌匯率工具</h1>
      <p className="text-sm text-gray-500">
        查實時匯率・找換店・機場與信用卡兌換比較
      </p>

      <div className="grid gap-3 text-left">
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
          <select className="w-full border rounded px-3 py-2 mt-1" value={from} onChange={(e) => setFrom(e.target.value)}>
            {["HKD", "CNY", "USD", "JPY", "KRW", "EUR", "TWD"].map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>

        <label>
          兌換至 / To:
          <select className="w-full border rounded px-3 py-2 mt-1" value={to} onChange={(e) => setTo(e.target.value)}>
            {["HKD", "CNY", "USD", "JPY", "KRW", "EUR", "TWD"].map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="text-xl font-medium bg-yellow-100 p-3 rounded shadow">
        ≈ {converted.toLocaleString(undefined, { maximumFractionDigits: 2 })} {to}
      </div>

      {loaded && (
        <div className="space-y-8 text-left text-sm bg-gray-50 p-4 rounded">
          <div>
            <h2 className="font-bold text-lg mb-2 text-blue-700">🏦 香港找換店報價</h2>
            {ratesData.hk_shops?.map((shop, idx) => (
              <div key={idx} className="mb-1">📍 {shop.name}：{shop.rates[to] ?? '-'} {to}</div>
            ))}
          </div>

          <div>
            <h2 className="font-bold text-lg mb-2 text-green-700">💳 信用卡兌換率比較</h2>
            {ratesData.cards?.map((c, idx) => (
              <div key={idx}>💳 {c.name}：{c.rates[to] ?? '-'} {to}</div>
            ))}
          </div>

          <div>
            <h2 className="font-bold text-lg mb-2 text-purple-700">🛫 機場找換店（日本 / 韓國）</h2>
            {ratesData.airports?.map((s, idx) => (
              <div key={idx}>🛬 {s.name}：{s.rates[to] ?? '-'} {to}</div>
            ))}
          </div>
        </div>
      )}

      <div className="text-xs text-gray-400 mt-6">
        ⓘ 匯率資料每 15 分鐘更新．僅供參考．Copyright by checkrate
      </div>
    </div>
  );
}
