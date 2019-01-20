"""
Convert Markdown to Confluence Storage Format.
"""
import sys

from mistune import Renderer, Markdown, escape

# Translates GFM code block language IDs to those use in Confluence's Code macro (where they differ)
_LANGS = {
    'erlang': 'erl',
    'html': 'xml',
    'xhtml': 'xml',
    'javascript': 'js',
    'node': 'js',
    'posh': 'powershell',
    'pwsh': 'powershell',
    'python': 'py',
    'python3': 'py',
    'visual basic': 'vb',
    'vb.net': 'vb',
    'vbnet': 'vb',
    'yaml': 'yml',
    'gradle': 'groovy',
    'no-highlight': 'text',
    # add more if needed here
}


def escape_cdata(text: str) -> str:
    """
    Escape text to be safe to embed in a <![CDATA[]]> block.
    """
    return text.replace(']]>', ']]]]><![CDATA[>')


class Confluence(Renderer):
    """
    Render Markdown in Confluence's storage format.

    Confluence's storage format [#]_ is nearly identical to the default
    output format of Renderer.

    .. [#] https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
    """
    next_id: int

    def __init__(self, **kwargs):
        super().__init__(use_xhtml=True, **kwargs)
        self.next_id = 1

    def _id(self) -> int:
        new_id = self.next_id
        self.next_id += 1
        return new_id

    def strikethrough(self, text: str) -> str:
        return f"<span style=\"text-decoration: line-through;\">{text}</span>"

    def block_code(self, code, lang=None):
        if lang is None:
            lang = 'text'

        return f'<ac:structured-macro' \
            f' ac:name="code" ac:schema-version="1" ac:macro-id="{self._id()}">' \
            f'<ac:parameter ac:name="language">{escape(_LANGS.get(lang, lang))}</ac:parameter>' \
            f'<ac:plain-text-body><![CDATA[{escape_cdata(code)}]]></ac:plain-text-body>' \
            f'</ac:structured-macro>\n'

    # todo: translate relative links to Confluence-internal links
    # todo: anchors


md: Markdown = Markdown(renderer=Confluence())

print(md.parse(sys.stdin.read()))
