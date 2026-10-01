"""Read verified iPhone inputs from preserved Apple and SBP evidence, offline.

The notebook computes every floor and comparison. This module only extracts
inputs and checks their source identity, dates and checksums.
"""
import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd


def load_iphone_inputs(root: Path) -> pd.DataFrame:
    manifest = json.loads((root / 'data/v2/iphone_sources.json').read_text())
    for rec in manifest['files']:
        content = (root / rec['file']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == rec['sha256'], rec['file']
    rows = []
    for rec in manifest['models']:
        text = BeautifulSoup((root / rec['apple_file']).read_text(), 'html.parser').get_text(' ', strip=True)
        pricing = text[text.rfind('Pricing and Availability'):]
        price = int(re.search(rec['price_pattern'], pricing).group(1).replace(',', ''))
        assert rec['storage_evidence'] in pricing
        assert rec['availability_evidence'] in pricing
        capture = json.loads((root / rec['fx_file']).read_text())['response']
        if rec['year'] == 2026:
            header = re.search(r'View\s*\|\s*Series Name[^\n]+', capture).group(0)
            dates = re.findall(r'\d{2}-Sep-2026', header)
            rates = re.search(r'M2M Exchange Rate of PKR per USD in Ready\s*\|\s*([\d.,]+)', capture).group(1).split(',')
            rate = float(rates[dates.index('18-Sep-2026')])
        else:
            assert rec['fx_date_evidence'] in capture
            rate = float(re.search(r'\bUSD\s+([\d.]+)', capture).group(1))
        assert rec['availability_date'] == rec['fx_date']
        rows.append({k: rec[k] for k in ['year', 'model', 'storage_gb', 'availability_date', 'fx_date', 'apple_url', 'fx_url']} | {'usd': price, 'pkr_per_usd': rate})
    frame = pd.DataFrame(rows)
    assert frame.year.tolist() == [2019, 2021, 2023, 2026]
    assert frame.model.is_unique and frame[['usd', 'pkr_per_usd']].gt(0).all().all()
    return frame
