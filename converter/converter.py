from pptx import Presentation
from pptx.util import Inches, Pt, Cm


prs = Presentation()
prs.slide_height = Cm(29.7)
prs.slide_width = Cm(21)
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = Cm(0)
# card size
width = Cm(6.365) 
height = Cm(8.89)

txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame

tf.text = "This is text inside a textbox\vasasdas\vasdasdasdasd"
tf.fit_text()
prs.save('test.pptx')

class Converter:
    pass