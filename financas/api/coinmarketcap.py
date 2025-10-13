# financas/api/coinmarketcap.py
from typing import Dict, Iterable
from django.conf import settings
import requests


class CoinMarketCapError(RuntimeError):
    pass


def fetch_quotes(
    symbols: Iterable[str] = ("BTC", "ETH"), convert: str = "USD"
) -> Dict[str, dict]:
    api_key = getattr(settings, "COINMARKETCAP_API_KEY", "") or ""
    if not api_key:
        raise CoinMarketCapError(
            "Chave da API (COINMARKETCAP_API_KEY) não configurada."
        )

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": api_key}
    symbols_str = ",".join(s.strip().upper() for s in symbols if s)
    params = {"symbol": symbols_str, "convert": convert.upper()}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException as ex:
        raise CoinMarketCapError(f"Falha de rede ao consultar CMC: {ex}") from ex

    if resp.status_code != 200:
        try:
            j = resp.json()
            msg = j.get("status", {}).get("error_message") or j
        except Exception:
            msg = resp.text
        raise CoinMarketCapError(f"Erro HTTP {resp.status_code} da CMC: {msg}")

    data = resp.json()
    status = data.get("status", {})
    if status.get("error_code"):
        raise CoinMarketCapError(f"CMC retornou erro: {status.get('error_message')}")

    out: Dict[str, dict] = {}
    for sym, payload in (data.get("data") or {}).items():
        name = payload.get("name") or sym
        quote = (payload.get("quote") or {}).get(convert.upper()) or {}
        price = quote.get("price")
        pct24 = quote.get("percent_change_24h")
        if price is None:
            continue
        out[sym.upper()] = {
            "name": name,
            "price": float(price),
            "percent_change_24h": float(pct24) if pct24 is not None else 0.0,
        }
    if not out:
        raise CoinMarketCapError(
            "Nenhuma cotação retornada pela API (verifique símbolos/convert)."
        )
    return out
