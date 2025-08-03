import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict

BASE = "https://www.b2b-center.ru/market/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_one_page(page: int) -> List[Dict]:
    """Вернуть список словарей с одной страницы."""
    params = {"page": page}
    r = requests.get(BASE, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr")
    tenders = []

    for tr in rows:
        cells = tr.find_all("td")
        if len(cells) < 4:
            continue
        link_tag = cells[0].find("a", href=True)
        tenders.append(
            {
                "number": link_tag.text.strip() if link_tag else None,
                "url": "https://www.b2b-center.ru" + link_tag["href"]
                if link_tag
                else None,
                "customer": cells[1].get_text(strip=True),
                "published": cells[2].get_text(strip=True),
                "deadline": cells[3].get_text(strip=True),
            }
        )
    return tenders

def fetch_tenders(limit: int = 100) -> pd.DataFrame:
    """Собрать до `limit` тендеров."""
    result = []
    page = 1
    while len(result) < limit:
        print(f"Загружаю страницу {page}...")
        batch = parse_one_page(page)
        if not batch:
            break
        result.extend(batch)
        page += 1
    return pd.DataFrame(result[:limit])

def save(df, path: str, fmt: str = "csv"):
    """
    Сохраняем DataFrame в CSV или SQLite.
    fmt = 'csv' | 'sqlite'
    """
    if fmt.lower() == "csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"💾 Сохранено в CSV: {path}")
    elif fmt.lower() == "sqlite":
        import sqlite3
        with sqlite3.connect(path) as conn:
            df.to_sql("tenders", conn, if_exists="replace", index=False)
        print(f"💾 Сохранено в SQLite: {path}")
    else:
        raise ValueError("fmt должен быть 'csv' или 'sqlite'")