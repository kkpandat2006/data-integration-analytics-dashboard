import httpx

COUNTRIES_API = "https://restcountries.com/v3.1/all"

MOCK_RATES = {
    "USD": 1.0, "INR": 83.50, "EUR": 0.92, "GBP": 0.79,
    "JPY": 149.50, "AUD": 1.53, "CAD": 1.36,
}

_cached_currencies = None


async def fetch_currency_metadata() -> dict:
    global _cached_currencies
    if _cached_currencies is not None:
        return _cached_currencies
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(COUNTRIES_API, timeout=10.0)
            resp.raise_for_status()
            countries = resp.json()
        currencies = {}
        for country in countries:
            for code, info in country.get("currencies", {}).items():
                if code not in currencies:
                    currencies[code] = {"code": code, "name": info.get("name", ""), "symbol": info.get("symbol", "")}
        _cached_currencies = currencies
    except Exception:
        _cached_currencies = {}
    return _cached_currencies


def convert_amount(amount: float, from_currency: str = "USD", to_currency: str = "USD") -> float:
    if from_currency == to_currency:
        return amount
    if from_currency not in MOCK_RATES or to_currency not in MOCK_RATES:
        return amount
    return round((amount / MOCK_RATES[from_currency]) * MOCK_RATES[to_currency], 2)
