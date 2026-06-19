import asyncio
from urllib.parse import quote
import httpx

from .common import CommonTranslator

class GoogleTranslator(CommonTranslator):
    _LANGUAGE_CODE_MAP = {
        'CHS': 'zh-CN',
        'CHT': 'zh-TW',
        'JPN': 'ja',
        'ENG': 'en',
        'KOR': 'ko',
        'VIN': 'vi',
        'CSY': 'cs',
        'NLD': 'nl',
        'FRA': 'fr',
        'DEU': 'de',
        'HUN': 'hu',
        'ITA': 'it',
        'POL': 'pl',
        'PTB': 'pt',
        'ROM': 'ro',
        'RUS': 'ru',
        'ESP': 'es',
        'TRK': 'tr',
        'UKR': 'uk',
        'ARA': 'ar',
    }

    def __init__(self):
        super().__init__()

    async def translate_single(self, client, from_lang, to_lang, query):
        if not query or not query.strip():
            return query
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={from_lang}&tl={to_lang}&dt=t&q={quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            resp = await client.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            translated = "".join([x[0] for x in data[0] if x[0]])
            return translated
        except Exception as e:
            self.logger.error(f"Google translate error for query '{query}': {e}")
            return query

    async def _translate(self, from_lang, to_lang, queries):
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        async with httpx.AsyncClient(limits=limits) as client:
            tasks = [self.translate_single(client, from_lang, to_lang, q) for q in queries]
            return await asyncio.gather(*tasks)
