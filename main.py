from converter.spell import Spell

from converter.converter import Converter

with open('tests/spells/eldrich_blast.json') as f:
    spell = Spell(f.read())

from pprint import pprint
pprint(spell.__dict__)