import os
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.enum.text import MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.slide import Slide
from pptx.shapes.shapetree import Shape
from pptx.dml.color import RGBColor
from converter.spell import Spell
from io import BytesIO
from functools import cached_property


class Card:
    WIDTH = Cm(6.365) 
    HEIGHT = Cm(8.89)
    BORDER_1_SIZE = Cm(0.3)
    
    TITLE_GAP_LEFT = Cm(0.2)
    TITLE_GAP_TOP = Cm(0.3)
    TITLE_GAP_BOTTOM = Cm(0.1)

    BODY_SIZE_LEFT = Cm(0.4)
    BODY_SIZE_TOP = Cm(1)
    

    def __init__(self, left: Cm, top: Cm, spell: Spell):
        self.left = left
        self.top = top
        self.spell = spell
    

    @cached_property
    def font(self) -> str:
        return os.path.join(os.getcwd(), 'fonts/OpenSans-Regular.ttf')

    
    def add_to_slide(self, slide: Slide) -> None:
        self.add_border(slide)
        self.add_title(slide)
        self.add_body(slide)
    
    def add_border(self, slide: Slide) -> Shape:
        border: Shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            self.left,
            self.top,
            self.WIDTH,
            self.HEIGHT,
        )
        border.fill.background()
        border.line.color.rgb = RGBColor(0, 0, 0)
        border.line.width = self.BORDER_1_SIZE
        return border
    
    def add_title(self, slide: Slide) -> Shape:
        title: Shape = slide.shapes.add_textbox(
            self.left + self.TITLE_GAP_LEFT,
            self.top + self.TITLE_GAP_BOTTOM,
            self.WIDTH - 2 * self.TITLE_GAP_LEFT,
            self.BODY_SIZE_TOP - 2 * self.TITLE_GAP_BOTTOM,
        )
        title.fill.background()
        title.line.color.rgb = RGBColor(0, 0, 0)
        title.line.width = Cm(0.05)
        title_tf = title.text_frame
        title_tf.text = f'{self.spell.name.split("[")[0].strip()}    {self.spell.level}'

        title_tf.fit_text(font_file=self.font)

        title_tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        return title

    def add_body(self, slide: Slide) -> Shape:
        body: Shape = slide.shapes.add_textbox(
            self.left + self.BODY_SIZE_LEFT,
            self.top + self.BODY_SIZE_TOP,
            self.WIDTH - 2 * self.BODY_SIZE_LEFT,
            self.HEIGHT - 2 * self.BODY_SIZE_TOP,
        )
        body.fill.background()
        body.line.color.rgb = RGBColor(0, 0, 0)
        body.line.width = Cm(0.05)

        body_tf = body.text_frame
        body_tf.vertical_anchor = MSO_ANCHOR.TOP

        text = ''
        text += f'Materials: {self.spell.materials.value}\v'
        text += f'Distance: {self.spell.range}\v'
        text += self.spell.description
        body_tf.text = text
        body_tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        body_tf.word_wrap = True
        # fit_text ещё не работает корректно
        body_tf.fit_text(max_size=4, font_family = 'Open Sans', font_file=self.font)
        return body
