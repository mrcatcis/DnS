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

left = top = Cm(0)
# card size
width = Cm(6.365) 
height = Cm(8.89)

# txBox = slide.shapes.add_textbox(left, top, width, height)
# tf = txBox.text_frame

# tf.text = "This is text inside a textbox\vasasdas\vasdasdasdasd"
# tf.auto_size=MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
# tf.word_wrap=True


with open('tests/spells/eldrich_blast.json') as f:
    spell = Spell(f.read())

card = Card(Cm(1),Cm(2), spell)
card.add_to_slide(slide)

prs.save('/home/mrcatcis/shared/test.pptx')

class Converter:
    pass