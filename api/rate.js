export default async function handler(req, res) {
  const { base, target } = req.query;

  if (!base || !target) {
    return res.status(400).json({ error: "Missing base or target parameter" });
  }

  try {
    const apiRes = await fetch(`https://api.exchangerate.host/latest?base=${base}&symbols=${target}`);
    const data = await apiRes.json();
    const rate = data.rates?.[target] ?? 0;
    res.status(200).json({ rate });
  } catch (err) {
    res.status(500).json({ error: "API error" });
  }
}
