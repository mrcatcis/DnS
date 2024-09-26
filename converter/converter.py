from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.enum.text import MSO_AUTO_SIZE

from converter.card import Card
from converter.spell import Spell

prs = Presentation()
prs.slide_height = Cm(29.7)
prs.slide_width = Cm(21)
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

with open('tests/spells/fireball.json', encoding='utf-8') as f:
    spell = Spell(f.read())

card = Card(Cm(1),Cm(2), spell)
card.add_to_slide(slide)

prs.save('test.pptx')

class Converter:
    pass