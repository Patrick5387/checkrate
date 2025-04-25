import { useState, useEffect } from "react";

export default function App() {
  const [amountHKD, setAmountHKD] = useState(1000);
  const [selectedCurrency, setSelectedCurrency] = useState("JPY");
  const [exchangeRate, setExchangeRate] = useState(null);

  const fakeRates = {
    JPY: 19.3,
    USD: 0.127,
    TWD: 4.1,
    KRW: 172,
    EUR: 0.116
  };

  useEffect(() => {
    setExchangeRate(fakeRates[selectedCurrency]);
  }, [selectedCurrency]);

  const converted = amountHKD * (exchangeRate || 0);

  return (
    <div className="p-4 max-w-md mx-auto text-center space-y-4">
      <h1 className="text-3xl font-bold text-blue-700">CheckRate - 點兌滙率工具</h1>
      <p className="text-sm text-gray-500">查實時匯率、找換店、機場與信用卡兌換比較</p>

      <div className="space-y-2 text-left">
        <label>輸入港幣金額：</label>
        <input
          type="number"
          className="w-full border rounded px-3 py-2"
          value={amountHKD}
          onChange={(e) => setAmountHKD(parseFloat(e.target.value))}
        />

        <label>兌換目標貨幣：</label>
        <select
          className="w-full border rounded px-3 py-2"
          value={selectedCurrency}
          onChange={(e) => setSelectedCurrency(e.target.value)}
        >
          <option value="JPY">日圓（JPY）</option>
          <option value="USD">美元（USD）</option>
          <option value="TWD">台幣（TWD）</option>
          <option value="KRW">韓圓（KRW）</option>
          <option value="EUR">歐元（EUR）</option>
        </select>
      </div>

      <div className="text-xl font-medium bg-yellow-100 p-3 rounded shadow">
        ≈ {converted.toLocaleString()} {selectedCurrency}
      </div>

      <div className="mt-6 text-left space-y-6">
        <div>
          <h2 className="text-lg font-semibold mb-2 text-blue-600">📍 香港找換店推介：</h2>
          <ul className="space-y-1 text-sm">
            <li>金英找換（中環） - {fakeRates[selectedCurrency] - 0.1} {selectedCurrency}</li>
            <li>銀通找換（旺角） - {fakeRates[selectedCurrency] - 0.2} {selectedCurrency}</li>
            <li>易兌換（上水） - {fakeRates[selectedCurrency] - 0.15} {selectedCurrency}</li>
          </ul>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2 text-blue-600">✈️ 機場找換匯率：</h2>
          <ul className="space-y-1 text-sm">
            <li>香港國際機場：{fakeRates[selectedCurrency] - 0.3} {selectedCurrency}</li>
            <li>成田機場（日本）：{fakeRates[selectedCurrency] - 0.4} {selectedCurrency}</li>
          </ul>
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2 text-blue-600">💳 信用卡兌換率比較：</h2>
          <ul className="space-y-1 text-sm">
            <li>Visa（渣打）：{fakeRates[selectedCurrency] + 0.05} {selectedCurrency}（+1.95% 手續費）</li>
            <li>Master（匯豐）：{fakeRates[selectedCurrency] + 0.04} {selectedCurrency}（+2.0% 手續費）</li>
            <li>AE（Amex Blue）：{fakeRates[selectedCurrency] + 0.07} {selectedCurrency}（+2.5% 手續費）</li>
          </ul>
        </div>
      </div>
    </div>
  );
}