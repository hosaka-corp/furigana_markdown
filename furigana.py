"""
# Furigana annotations for Markdown (via <ruby> tags)

The HTML5 specification outlines <ruby> tags for Furigana over characters.
All modern browsers appear to support this. See:

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ruby

## Usage in Markdown
This extension parses patterns of the form:

    {KANJI}(FURIGANA)

... and emits corresponding HTML string:

    <ruby><rb>KANJI</rb><rp>(</rp><rt>FURIGANA</rt><rp>)</rp></ruby>


## Usage in Python

    #!/usr/bin/python
    import markdown
    from furigana import FuriganaExtension

    text = 'The {五}(ご){段}(だん){動}(どう){詞}(し) (Godan verbs) are ...'
    html = markdown.markdown(text, extensions=[FuriganaExtension()])
    ...


## License
furigana_markdown is licensed under the MIT license.
"""

import markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree

# Expects to parse patterns of the form '{kanji}(furigana)'
RUBY1_RE = r'(\{)(.)\}\((.+?)\)'

class FuriganaExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        ruby1 = RubyPattern(RUBY1_RE)
        md.inlinePatterns.add('ruby1', ruby1, '<link')

class RubyPattern(Pattern):
    def handleMatch(self, m):
        el = etree.Element('ruby')
        el1 = etree.SubElement(el, 'rb')
        el1.text = m.group(3)
        el2 = etree.SubElement(el, 'rp')
        el2.text = '('
        el3 = etree.SubElement(el, 'rt')
        el3.text = m.group(4)
        el4 = etree.SubElement(el, 'rp')
        el4.text = ')'
        return el

def makeExtension(configs=None):
    return FuriganaExtension(configs=configs)
