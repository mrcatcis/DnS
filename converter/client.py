import requests
import json

from typing import Any
from pathlib import Path

class TTGCachedClient:
    def __init__(self) -> None:
        self.cache_dir = Path('./.cache/spells/ttg_api/')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

    def get_spell(self, name: str) -> dict[str, Any]:
        name = name.lower()
        spell_path = self.cache_dir / f'{name}.json'
        if not spell_path.exists():
            spell = self.download_spell(name)
            with open(spell_path, 'w', encoding='utf-8') as f:
                f.write(spell)
        else:
            with open(spell_path, 'r', encoding='utf-8') as f:
                spell = f.read()

        return json.loads(spell)
    
    def download_spell(self, name: str) -> str:
        r = self.session.post(f'https://ttg.club/api/v1/spells/{name}')
        r.raise_for_status()
        return r.text
    
ttg_client = TTGCachedClient()