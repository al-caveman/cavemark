# Copyright 2018 caveman <toraboracaveman@protonmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

# parser states
_S_START                            = 0
_S_PARAGRAPH_IN                     = 1
_S_EMPHASIZE_IN                     = 2
_S_STRIKE_IN                        = 3
_S_CITATION_IN                      = 4
_S_CITATIONDATA_IN                  = 5
_S_HEADING_IN                       = 6
_S_LIST_IN                          = 7
_S_LISTPARAGRAPH_IN                 = 8
_S_RESOURCE_IN                      = 9
_S_RESOURCE_IGNORED_KEY_IN          = 10
_S_CODE_IN                          = 11

# tag indices
_I_OPEN_ANY_SEP                     = 1
_I_OPEN_ANY_EMPHASIZE               = 2
_I_OPEN_ANY_STRIKE                  = 3
_I_OPEN_ANY_CITATION                = 4
_I_OPEN_ANY_HEADING_LEVEL           = 5
_I_OPEN_ANY_HEADING_BOOKMARK        = 6
_I_OPEN_ANY_LIST_LEVEL              = 7
_I_OPEN_ANY_LIST_TYPE               = 8
_I_OPEN_ANY_RESOURCE_TYPE           = 9
_I_OPEN_ANY_RESOURCE_ID             = 10
_I_OPEN_ANY_CODE                    = 11
_I_OPEN_ANY_SHORTCUT                = 12

_I_CLOSE_HEADING                    = 1
_I_CLOSE_HEADING_EMPHASIZE          = 2
_I_CLOSE_HEADING_STRIKE             = 3
_I_CLOSE_HEADING_CITATION           = 4
_I_CLOSE_HEADING_CODE               = 5
_I_CLOSE_HEADING_SHORTCUT           = 6

_I_CLOSE_LIST_PARAGRAPH             = 1
_I_CLOSE_LIST                       = 2
_I_CLOSE_LIST_EMPHASIZE             = 3
_I_CLOSE_LIST_STRIKE                = 4
_I_CLOSE_LIST_CITATION              = 5
_I_CLOSE_LIST_LIST_LEVEL            = 6
_I_CLOSE_LIST_LIST_TYPE             = 7
_I_CLOSE_LIST_CODE                  = 8
_I_CLOSE_LIST_SHORTCUT              = 9

_I_CLOSE_LISTPARAGRAPH_PARAGRAPH    = 1
_I_CLOSE_LISTPARAGRAPH              = 2
_I_CLOSE_LISTPARAGRAPH_LIST_LEVEL   = 3
_I_CLOSE_LISTPARAGRAPH_LIST_TYPE    = 4

_I_CLOSE_PARAGRAPH                  = 1
_I_CLOSE_PARAGRAPH_EMPHASIZE        = 2
_I_CLOSE_PARAGRAPH_STRIKE           = 3
_I_CLOSE_PARAGRAPH_CITATION         = 4
_I_CLOSE_PARAGRAPH_CODE             = 5
_I_CLOSE_PARAGRAPH_SHORTCUT         = 6

_I_CLOSE_RESOURCE                   = 1
_I_CLOSE_RESOURCE_ENTRY_KEY         = 2
_I_CLOSE_RESOURCE_EMPHASIZE         = 3
_I_CLOSE_RESOURCE_STRIKE            = 4
_I_CLOSE_RESOURCE_CITATION          = 5
_I_CLOSE_RESOURCE_CODE              = 6
_I_CLOSE_RESOURCE_SHORTCUT          = 7

_I_CLOSE_RESOURCEIGNK               = 1
_I_CLOSE_RESOURCEIGNK_ENTRY_KEY     = 2

_I_CLOSE_EMPHASIZE                  = 1
_I_CLOSE_EMPHASIZE_STRIKE           = 2
_I_CLOSE_EMPHASIZE_CITATION         = 3
_I_CLOSE_EMPHASIZE_CODE             = 4
_I_CLOSE_EMPHASIZE_SHORTCUT         = 5

_I_CLOSE_STRIKE                     = 1
_I_CLOSE_STRIKE_EMPHASIZE           = 2
_I_CLOSE_STRIKE_CITATION            = 3
_I_CLOSE_STRIKE_CODE                = 4
_I_CLOSE_STRIKE_SHORTCUT            = 5

_I_CLOSE_CITATION                   = 1
_I_CLOSE_CITATION_DATA              = 2

_I_CLOSE_CITATIONDATA               = 1
_I_CLOSE_CITATIONDATA_EMPHASIZE     = 2
_I_CLOSE_CITATIONDATA_STRIKE        = 3
_I_CLOSE_CITATIONDATA_CITATION      = 4
_I_CLOSE_CITATIONDATA_CODE          = 5
_I_CLOSE_CITATIONDATA_SHORTCUT      = 6

_I_CLOSE_CITATIONDATAIGNORED        = 1

_I_CLOSE_CODE                       = 1

class CaveMark:
    """Create a new CaveMark string parser object,
    """

    def __init__(
        self, resources=None, resource_keys_ignored=None,
        resource_counters=None, escape=None, code=None, code_inline=None,
        code_unescape=None, heading_offset=None, shortcuts=None,
        cite_id_default=None, cite_type_default=None, cite_key_default=None,
        frmt_cite_inline=None, frmt_cite_box=None, frmt_cite_data_default=None,
        frmt_cite_error_inline=None, frmt_cite_error_box=None,
        frmt_bibliography_prefix=None, frmt_bibliography_suffix=None,
        frmt_bibliography_item=None, frmt_bibliography_error_item=None,
        frmt_footnote_prefix=None, frmt_footnote_suffix=None,
        frmt_footnote_item=None, frmt_footnote_error_item=None,
        frmt_paragraph_prefix=None, frmt_paragraph_suffix=None,
        frmt_emph_prefix=None, frmt_emph_suffix=None, frmt_strike_prefix=None,
        frmt_strike_suffix=None, frmt_code_prefix=None, frmt_code_suffix=None,
        frmt_olist_prefix=None, frmt_olist_suffix=None, frmt_ulist_prefix=None,
        frmt_ulist_suffix=None, frmt_list_item_prefix=None,
        frmt_list_item_suffix=None, frmt_heading_prefix=None,
        frmt_heading_suffix=None
    ):
        # references/resources dictionary
        if resources is None:
            self.resources = {}
        else:
            self.resources = resources

        # ignored resource keys
        if resource_keys_ignored is None:
            self.resource_keys_ignored = {'url'}
        else:
            self.resource_keys_ignored = resource_keys_ignored

        # counters per resource
        if resource_counters is None:
            self.resource_counters = {
                'link'      :'counter_a',
                'book'      :'counter_a',
                'image'     :'counter_c',
                'note'      :'counter_d',
                'quotation' :'counter_e',
                'rule'      :'counter_f',
                'definition':'counter_g',
                'axiom'     :'counter_h',
                'assumption':'counter_i',
                'theorem'   :'counter_j',
                'corollary' :'counter_k',
                'conjecture':'counter_l',
                'hypothesis':'counter_m',
                'SECTION'   :'counter_n',
                'question'  :'counter_o',
                'answer'    :'counter_p',
                'footnote'  :'counter_q',
            }
        else:
            self.resource_counters = resource_counters

        # escape char is used to literally print stuff
        if escape is None:
            self.escape = '\\'
        else:
            self.escape = escape     

        # opening/closing tags that define substrings to ignore parsing them
        if code is None:
            self.code = {
                '$$' : '$$',
                '$'  : '$',
                '`'  : '`',
                '```': '```',
            }
        else:
            self.code = code

        # specify which code is inline so that when it appears alone, it gets
        # encapsulated in a paragraph
        if code_inline is None:
            self.code_inline = {'$$', '$', '`'}
        else:
            self.code_inline = code_inline

        # ignored text intervals to unescape
        if code_unescape is None:
            self.code_unescape = {'`', '```'}
        else:
            self.code_unescape = code_unescape

        # offset heading level.  e.g. if offset=1, "# title" becomes
        # "<h2>title</h2>" instead of "<h1>..."
        if heading_offset is None:
            self.heading_offset = 1
        else:
            self.heading_offset = heading_offset

        # inline quotes format
        if shortcuts is None:
            self.shortcuts = {
                '(c)'   : '&copy;', 
                '(tm)'  : '&trade;', 
                '(R)'   : '&reg;', 
                '"'     : '&ldquo;', 
                "''"    : '&rdquo;', 
                '---'   : '&mdash;', 
                '...'   : '&hellip;', 
            }
        else:
            self.shortcuts = shortcuts

        # default id for citations that lack an identifier
        if cite_id_default is None:
            self.cite_id_default = '__'
        else:
            self.cite_id_default = cite_id_default

        # default type for citations that lack an identifier
        if cite_type_default is None:
            self.cite_type_default = 'footnote'
        else:
            self.cite_type_default = cite_type_default

        # default data key for citations that lack an identifier
        if cite_key_default is None:
            self.cite_key_default = {
                'link'      : 'text',
                'footnote'  : 'text',
            }
        else:
            self.cite_key_default = cite_key_default

        # inline citation format
        if frmt_cite_inline is None:
            self.frmt_cite_inline = {
            'link'      :' <a href="{url}">{text}</a>',
            'book'      :' <a href="#cite_{ID}">[{INDEX}]</a>',
            'image'     :' <a href="#cite_{ID}">Figure {INDEX}</a>',
            'note'      :' <a href="#cite_{ID}">Note {INDEX}</a>',
            'quotation' :' <a href="#cite_{ID}">Quote {INDEX}</a>',
            'rule'      :' <a href="#cite_{ID}">Rule {INDEX}</a>',
            'definition':' <a href="#cite_{ID}">Definition {INDEX}</a>',
            'axiom'     :' <a href="#cite_{ID}">Axiom {INDEX}</a>',
            'assumption':' <a href="#cite_{ID}">Assumption {INDEX}</a>',
            'theorem'   :' <a href="#cite_{ID}">Theorem {INDEX}</a>',
            'corollary' :' <a href="#cite_{ID}">Corollary {INDEX}</a>',
            'conjecture':' <a href="#cite_{ID}">Conjecture {INDEX}</a>',
            'hypothesis':' <a href="#cite_{ID}">Hypothesis {INDEX}</a>',
            'SECTION'   :' <a href="#{BOOKMARK}">Section {INDEX}</a>',
            'question'  :' <a href="#cite_{ID}">Question {INDEX}</a>',
            'answer'    :' <a href="#cite_{ID}">Answer {INDEX}</a>',
            'footnote'  :'<sup><a href="#fn_{ID}">{INDEX}</a></sup>',
            }
        else:
            self.frmt_cite_inline = frmt_cite_inline

        # box citation format.
        if frmt_cite_box is None:
            self.frmt_cite_box = {
                'image'     :'<figure id="cite_{ID}" '
                             'style="text-align:center;">'
                             '<img alt="{alt}" src="{url}" />'
                             '<figcaption>'
                             '<strong><a href="#cite_{ID}">'
                             'Figure {INDEX}.'
                             '</a></strong>'
                             ' {caption}'
                             '</figcaption>'
                             '</figure>\n\n',
                'note'      :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Note {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'quotation' :'<figure id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Quote {INDEX}:'
                             '</a></strong>'
                             '<blockquote><em>'
                             '&ldquo;{text}&rdquo;'
                             '</em></blockquote>'
                             '<footer style="text-align:right;">'
                             '&mdash; <cite>{author}</cite>'
                             '</footer>'
                             '</figure>\n\n',
                'rule'      :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Rule {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'definition':'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Definition {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'axiom'     :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Axiom {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'assumption' :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Assumption {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'theorem'   :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Theorem {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'corollary' :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Corollary {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'conjecture':'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Conjecture {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'hypothesis':'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Hypothesis {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'question'  :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Question {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
                'answer'    :'<p id="cite_{ID}">'
                             '<strong><a href="#cite_{ID}">'
                             'Answer {INDEX}.'
                             '</a></strong>'
                             ' <em>{text}</em>'
                             '</p>\n\n',
            }
        else:
            self.frmt_cite_box = frmt_cite_box

        # default resource data when data is not supplied
        if frmt_cite_data_default is None:
            self.frmt_cite_data_default = {
                'link'      :'[{INDEX}]',
                'book'      :' <a href="#cite_{ID}">[{INDEX}]</a>',
            }
        else:
            self.frmt_cite_data_default = frmt_cite_data_default

        # errornous inline citation format
        if frmt_cite_error_inline is None:
            self.frmt_cite_error_inline = '<span class="error">'\
                                          '[err: {ERROR}]</span>'
        else:
            self.frmt_cite_error_inline = frmt_cite_error_inline

        # errornous box citation format
        if frmt_cite_error_box is None:
            self.frmt_cite_error_box = '<p class="error" '\
                                       'style="text-align:center">'\
                                       '[err: {ERROR}]'\
                                       '</p>'
        else:
            self.frmt_cite_error_box = frmt_cite_error_box

        # bibliography container prefix
        if frmt_bibliography_prefix is None:
            self.frmt_bibliography_prefix = '<footer>\n'\
                                            '<h4>Bibliography</h4>\n'\
                                            '<ul style="list-style:none;'\
                                            'padding:0; margin:0;">\n'
        else:
            self.frmt_bibliography_prefix = frmt_bibliography_prefix

        # bibliography container suffix
        if frmt_bibliography_suffix is None:
            self.frmt_bibliography_suffix = '</ul>\n</footer>\n\n'
        else:
            self.frmt_bibliography_suffix = frmt_bibliography_suffix

        # bibliography items format
        if frmt_bibliography_item is None:
            self.frmt_bibliography_item = {
                'book'  :'<li id="cite_{ID}"><small>'
                         '[{INDEX}] {authors}, '
                         '&ldquo;<em>{title}</em>&ldquo;, {publisher}, '
                         '{year}.</small></li>\n',
            }
        else:
            self.frmt_bibliography_item = frmt_bibliography_item

        # errornous bibliography item format
        if frmt_bibliography_error_item is None:
            self.frmt_bibliography_error_item = '<li class="error">'\
                                                '<small>err: {ERROR}</small>'\
                                                '</li>'
        else:
            self.frmt_bibliography_error_item = frmt_bibliography_error_item

        # footnote container prefix
        if frmt_footnote_prefix is None:
            self.frmt_footnote_prefix = '<footer>\n<hr/>\n'\
                                        '<ul style="list-style:none;'\
                                        'padding:0; margin:0;">'
        else:
            self.frmt_footnote_prefix = frmt_footnote_prefix

        # footnote container suffix
        if frmt_footnote_suffix is None:
            self.frmt_footnote_suffix = '</ul>\n</footer>\n\n'
        else:
            self.frmt_footnote_suffix = frmt_footnote_suffix

        # footnote items format
        if frmt_footnote_item is None:
            self.frmt_footnote_item = {
                'footnote'  :'<li id="fn_{ID}">'\
                             '<small>{INDEX}. {text}</small>'\
                             '</li>\n',
            }
        else:
            self.frmt_footnote_item = frmt_footnote_item

        # errornous footnote item format
        if frmt_footnote_error_item is None:
            self.frmt_footnote_error_item = '<li class="error">'\
                                            '<small>err: {ERROR}</small>'\
                                            '</li>'
        else:
            self.frmt_footnote_error_item = frmt_footnote_error_item

        # paragraphs format
        if frmt_paragraph_prefix is None:
            self.frmt_paragraph_prefix = '<p>'
        else:
            self.frmt_paragraph_prefix = frmt_paragraph_prefix
        if frmt_paragraph_suffix is None:
            self.frmt_paragraph_suffix = '</p>\n\n'
        else:
            self.frmt_paragraph_suffix = frmt_paragraph_suffix

        # emphasized text format
        if frmt_emph_prefix is None:
            self.frmt_emph_prefix = '<em>'
        else:
            self.frmt_emph_prefix = frmt_emph_prefix
        if frmt_emph_suffix is None:
            self.frmt_emph_suffix = '</em>'
        else:
            self.frmt_emph_suffix = frmt_emph_suffix

        # struck-through text format
        if frmt_strike_prefix is None:
            self.frmt_strike_prefix = '<s>'
        else:
            self.frmt_strike_prefix = frmt_strike_prefix
        if frmt_strike_suffix is None:
            self.frmt_strike_suffix = '</s>'
        else:
            self.frmt_strike_suffix = frmt_strike_suffix

        # code prefix format
        if frmt_code_prefix is None:
            self.frmt_code_prefix = {
                '$$'    : '<span class="ignored">{OPEN}',
                '$'     : '<span class="ignored">{OPEN}',
                '`'     : '<code>',
                '```'   : '<pre><code>',
            }
        else:
            self.frmt_code_prefix = frmt_code_prefix

        # code suffix format
        if frmt_code_suffix is None:
            self.frmt_code_suffix = {
                '$$'    : '{CLOSE}</span>',
                '$'     : '{CLOSE}</span>',
                '`'     : '</code>',
                '```'   : '</code></pre>',
            }
        else:
            self.frmt_code_suffix = frmt_code_suffix

        # ordered lists format
        if frmt_olist_prefix is None:
            self.frmt_olist_prefix = '<ol>\n'
        else:
            self.frmt_olist_prefix = frmt_olist_prefix
        if frmt_olist_suffix is None:
            self.frmt_olist_suffix = '</ol>\n'
        else:
            self.frmt_olist_suffix = frmt_olist_suffix

        # unordered lists format
        if frmt_ulist_prefix is None:
            self.frmt_ulist_prefix = '<ul>\n'
        else:
            self.frmt_ulist_prefix = frmt_ulist_prefix
        if frmt_ulist_suffix is None:
            self.frmt_ulist_suffix = '</ul>\n'
        else:
            self.frmt_ulist_suffix = frmt_ulist_suffix

        # listed items format
        if frmt_list_item_prefix is None:
            self.frmt_list_item_prefix = '<li>'
        else:
            self.frmt_list_item_prefix = frmt_list_item_prefix
        if frmt_list_item_suffix is None:
            self.frmt_list_item_suffix = '</li>\n'
        else:
            self.frmt_list_item_suffix = frmt_list_item_suffix

        # headings format
        if frmt_heading_prefix is None:
            self.frmt_heading_prefix = '<h{LEVEL} id="{BOOKMARK}">'\
                                       '<a class="hindex"'\
                                       ' href="#{BOOKMARK}">{INDEX}.</a> '
        else:
            self.frmt_heading_prefix = frmt_heading_prefix
        if frmt_heading_suffix is None:
            self.frmt_heading_suffix = '</h{LEVEL}>\n\n'
        else:
            self.frmt_heading_suffix = frmt_heading_suffix

        # states that need to be defined early
        self._state = [_S_START]
        self._html = [[]]

        self._resource_cur_entry_key = None

        self._citations_last_index = {}
        self._citations_last_default_id_prefix = 0
        self._citations_pending_boxes = []
        self._citation_cur_id = None
        self._citation_cur_data = None
        self.resources_cited = {}

        self._footnote_items = []

        self._bibliography_items = []

        self._list = [[-1, None]]

        self._heading_index = [0] * 6
        self._heading_bookmark = [''] * 6

        # compile re and other stuff
        self.update()

    def update(self):
        """Run this when you modify self.code or add/remove resource types.
        """
        # open tag any
        tags_open_code = list(self.code)
        tags_open_code.sort(key=len, reverse=True)
        shortcuts_raw = list(self.shortcuts)
        shortcuts_raw.sort(key=len, reverse=True)
        resource_types = list(self.resource_counters)
        self._re_tag_open_any = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(^\s*\n|\n\s*\n)',            # unit separator
                    r'(_)',                         # emphasize open
                    r'(\~\~)',                      # strike open
                    r'(\[)',                        # cite open
                    r'^ *(#+)(?:(\S+)|)(?: +| *\n)(?=\S)',  # heading open
                    r'^( *)(\*|\+)',                # list open
                    r'^ *({}) *: *(\S+)'.format(    # resource definition open
                        r'|'.join(resource_types)
                    ), 
                    r'({})\n?'.format(              # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(                 # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag heading
        self._re_tag_close_heading = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\n\s*\n)',           # heading close
                    r'(_)',                 # emphasize open
                    r'(\~\~)',              # strike open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag list
        self._re_tag_close_list = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\n\s*\n +)(?=[^\*\+\s])',# open paragraph
                    r'(\n\s*\n)(?=[^\*\+\s])',  # list close
                    r'(_)',                     # emphasize open
                    r'(\~\~)',                  # strike open
                    r'(\[)',                    # cite open
                    r'(?:^|\n)( *)(\*|\+)',     # list open
                    r'({})\n?'.format(          # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(             # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag listparagraph
        self._re_tag_close_listparagraph = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'^( +)(?=[^\*\+\s])',  # open paragraph
                    r'^()(?=[^\*\+\s])',    # list close
                    r'^( *)(\*|\+)',        # list open
                    r'\Z',
                ])
            )
        )

        # close tag paragraph
        self._re_tag_close_paragraph = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\n\s*\n)',           # paragraph close
                    r'(_)',                 # emphasize open
                    r'(\~\~)',              # strike open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag resource
        self._re_tag_close_resource = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\n\s*\n)',           # resource close
                    r'\n *([^\[\s]\S*?) *: *',# resource entry key
                    r'(_)',                 # emphasize open
                    r'(\~\~)',              # strike open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag resource ignored key
        self._re_tag_close_resource_ignored_key = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\n\s*\n)',           # resource close
                    r'\n *(\S+) *: *',      # resource entry key
                    r'\Z',
                ])
            )
        )

        # close tag emphasize
        self._re_tag_close_emphasize = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(_)',                 # emphasize close
                    r'(\~\~)',              # strike open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag strike
        self._re_tag_close_strike = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\~\~)',              # strike close
                    r'(_)',                 # emphasize open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag citation
        self._re_tag_close_citation = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\])',                # cite close
                    r'(:)',                 # data open
                    r'\Z',
                ])
            )
        )

        # close tag citationdata
        self._re_tag_close_citationdata = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\])',                # citationdata close
                    r'(_)',                 # emphasize open
                    r'(\~\~)',              # strike open
                    r'(\[)',                # cite open
                    r'({})\n?'.format(      # code open
                        r'|'.join(re.escape(o) for o in tags_open_code)
                    ),
                    r'({})'.format(         # shortcuts
                        r'|'.join(re.escape(s) for s in shortcuts_raw)
                    ),
                    r'\Z',
                ])
            )
        )

        # close tag citationdata when the data key is to be ignored
        self._re_tag_close_citationdata_ignored = re.compile(
            r'(?<!{0})(?:{1})'.format(
                re.escape(self.escape),
                r'|'.join([
                    r'(\])',                # citationdata close
                    r'\Z',
                ])
            )
        )

        # close tag code
        self._re_tag_close_code = {
            o : re.compile(
                r'(?<!{0})(?:{1})'.format(
                    re.escape(self.escape),
                    r'|'.join([
                        r'\n?({})'.format( # code close
                            re.escape(self.code[o])
                        ),
                        r'\Z',
                    ])
                )
            )
            for o in tags_open_code
        }

        # unescape
        self._re_unescape = re.compile(
            r'{}(.)'.format(re.escape(self.escape))
        )

    def parse(self, text):
        """Parse input CaveMark string.
        """
        text = self._replace_unsafe(text)
        while True:
            if len(text) == 0:
                break

            # parse new unit
            elif self._state[-1] == _S_START:
                m = self._re_tag_open_any.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]

                if len(self._citations_pending_boxes):
                    self._flush_pending_boxes()

                if len(text_behind.strip()):
                    self._paragraph_open()
                    self._html[-1].append(text_behind)
                    if m.group(_I_OPEN_ANY_SEP) is not None:
                        self._paragraph_close()
                        continue

                if m.group(_I_OPEN_ANY_EMPHASIZE) is not None:
                    self._emphasize_open()

                elif m.group(_I_OPEN_ANY_STRIKE) is not None:
                    self._strike_open()

                elif m.group(_I_OPEN_ANY_CODE) is not None:
                    self._code_open(m.group(_I_OPEN_ANY_CODE))

                elif m.group(_I_OPEN_ANY_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_OPEN_ANY_SHORTCUT))

                elif m.group(_I_OPEN_ANY_CITATION) is not None:
                    self._citation_open()

                elif self._state[-1] == _S_START:
                    if m.group(_I_OPEN_ANY_HEADING_LEVEL) is not None:
                        self._heading_open(
                            m.group(_I_OPEN_ANY_HEADING_LEVEL),
                            m.group(_I_OPEN_ANY_HEADING_BOOKMARK)
                        )

                    elif m.group(_I_OPEN_ANY_LIST_LEVEL) is not None:
                        self._list_open(
                            len(m.group(_I_OPEN_ANY_LIST_LEVEL)),
                            m.group(_I_OPEN_ANY_LIST_TYPE)
                        )

                    elif m.group(_I_OPEN_ANY_RESOURCE_TYPE) is not None:
                        self._resource_open(
                            m.group(_I_OPEN_ANY_RESOURCE_TYPE),
                            m.group(_I_OPEN_ANY_RESOURCE_ID),
                        )

            # resume parsing paragraph
            elif self._state[-1] == _S_PARAGRAPH_IN:
                m = self._re_tag_close_paragraph.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_PARAGRAPH) is not None:
                    self._paragraph_close()
                elif m.group(_I_CLOSE_PARAGRAPH_EMPHASIZE) is not None:
                    self._emphasize_open()
                elif m.group(_I_CLOSE_PARAGRAPH_STRIKE) is not None:
                    self._strike_open()
                elif m.group(_I_CLOSE_PARAGRAPH_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_PARAGRAPH_CODE))
                elif m.group(_I_CLOSE_PARAGRAPH_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_PARAGRAPH_SHORTCUT))
                elif m.group(_I_CLOSE_PARAGRAPH_CITATION) is not None:
                    self._citation_open()

            # resume parsing emphasized text
            elif self._state[-1] == _S_EMPHASIZE_IN:
                m = self._re_tag_close_emphasize.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_EMPHASIZE) is not None:
                    self._emphasize_close()
                elif m.group(_I_CLOSE_EMPHASIZE_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_EMPHASIZE_CODE))
                elif m.group(_I_CLOSE_EMPHASIZE_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_EMPHASIZE_SHORTCUT))
                elif m.group(_I_CLOSE_EMPHASIZE_CITATION) is not None:
                    self._citation_open()

            # resume parsing struck-through text
            elif self._state[-1] == _S_STRIKE_IN:
                m = self._re_tag_close_strike.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_STRIKE) is not None:
                    self._strike_close()
                elif m.group(_I_CLOSE_STRIKE_EMPHASIZE) is not None:
                    self._emphasize_open()
                elif m.group(_I_CLOSE_STRIKE_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_STRIKE_CODE))
                elif m.group(_I_CLOSE_STRIKE_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_STRIKE_SHORTCUT))
                elif m.group(_I_CLOSE_STRIKE_CITATION) is not None:
                    self._citation_open()

            # resume parsing code
            elif self._state[-1] == _S_CODE_IN:
                m = self._re_tag_close_code[self._code_tag_open].search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(
                    text_behind,
                    tag=self.code[self._code_tag_open]
                )
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_CODE) is not None:
                    self._code_close()

            # resume parsing list
            elif self._state[-1] == _S_LIST_IN:
                m = self._re_tag_close_list.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_LIST) is not None:
                    while len(self._list) > 1:
                        self._list_close()
                elif m.group(_I_CLOSE_LIST_PARAGRAPH) is not None:
                    self._listparagraph_open()
                    self._paragraph_open()
                elif m.group(_I_CLOSE_LIST_EMPHASIZE) is not None:
                    self._emphasize_open()
                elif m.group(_I_CLOSE_LIST_STRIKE) is not None:
                    self._strike_open()
                elif m.group(_I_CLOSE_LIST_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_LIST_CODE))
                elif m.group(_I_CLOSE_LIST_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_LIST_SHORTCUT))
                elif m.group(_I_CLOSE_LIST_CITATION) is not None:
                    self._citation_open()
                elif m.group(_I_CLOSE_LIST_LIST_LEVEL) is not None:
                    self._list_item_new(
                        len(m.group(_I_CLOSE_LIST_LIST_LEVEL)),
                        m.group(_I_CLOSE_LIST_LIST_TYPE)
                    )

            # resume parsing pararagraphs in list
            elif self._state[-1] == _S_LISTPARAGRAPH_IN:
                m = self._re_tag_close_listparagraph.search(text)
                start, endo = m.span()
                text = text[endo:]
                self._listparagraph_close()
                if m.group(_I_CLOSE_LISTPARAGRAPH) is not None:
                    while len(self._list) > 1:
                        self._list_close()
                elif m.group(_I_CLOSE_LISTPARAGRAPH_PARAGRAPH) is not None:
                    self._listparagraph_open()
                    self._paragraph_open()
                elif m.group(_I_CLOSE_LISTPARAGRAPH_LIST_LEVEL) is not None:
                    self._list_item_new(
                        len(m.group(_I_CLOSE_LISTPARAGRAPH_LIST_LEVEL)),
                        m.group(_I_CLOSE_LISTPARAGRAPH_LIST_TYPE)
                    )

            # resume parsing heading
            elif self._state[-1] == _S_HEADING_IN:
                m = self._re_tag_close_heading.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_HEADING) is not None:
                    self._heading_close()
                elif m.group(_I_CLOSE_HEADING_EMPHASIZE) is not None:
                    self._emphasize_open()
                elif m.group(_I_CLOSE_HEADING_STRIKE) is not None:
                    self._strike_open()
                elif m.group(_I_CLOSE_HEADING_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_HEADING_CODE))
                elif m.group(_I_CLOSE_HEADING_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_HEADING_SHORTCUT))
                elif m.group(_I_CLOSE_HEADING_CITATION) is not None:
                    self._citation_open()

            # resume parsing resource
            elif self._state[-1] == _S_RESOURCE_IN:
                m = self._re_tag_close_resource.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                if self._resource_cur_entry_key is not None:
                    self._html[-1].append(text_behind)
                if m.group(_I_CLOSE_RESOURCE) is not None:
                    self._resource_close()
                elif m.group(_I_CLOSE_RESOURCE_ENTRY_KEY) is not None:
                    self._resource_close_entry()
                    self._resource_cur_entry_key = m.group(
                        _I_CLOSE_RESOURCE_ENTRY_KEY
                    )
                    if (
                        self._resource_cur_entry_key
                        in self.resource_keys_ignored
                    ):
                        self._resource_ignored_key_open()
                elif m.group(_I_CLOSE_RESOURCE_EMPHASIZE) is not None:
                    self._emphasize_open()
                elif m.group(_I_CLOSE_RESOURCE_STRIKE) is not None:
                    self._strike_open()
                elif m.group(_I_CLOSE_RESOURCE_CODE) is not None:
                    self._code_open(m.group(_I_CLOSE_RESOURCE_CODE))
                elif m.group(_I_CLOSE_RESOURCE_SHORTCUT) is not None:
                    self._shortcut_add(m.group(_I_CLOSE_RESOURCE_SHORTCUT))
                elif m.group(_I_CLOSE_RESOURCE_CITATION) is not None:
                    self._citation_open()

            # resume parsing resource ignored key
            elif self._state[-1] == _S_RESOURCE_IGNORED_KEY_IN:
                m = self._re_tag_close_resource_ignored_key.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text_behind = self._unescape(text_behind)
                text = text[endo:]
                self._html[-1].append(text_behind)
                self._resource_ignored_key_close()
                if m.group(_I_CLOSE_RESOURCEIGNK) is not None:
                    self._resource_close()
                elif m.group(_I_CLOSE_RESOURCEIGNK_ENTRY_KEY) is not None:
                    self._resource_close_entry()
                    self._resource_cur_entry_key = m.group(
                        _I_CLOSE_RESOURCEIGNK_ENTRY_KEY
                    )
                    if (
                        self._resource_cur_entry_key
                        in self.resource_keys_ignored
                    ):
                        self._resource_ignored_key_open()

            # resume parsing citation
            elif self._state[-1] == _S_CITATION_IN:
                m = self._re_tag_close_citation.search(text)
                start, endo = m.span()
                text_behind = text[0:start]
                text = text[endo:]
                resource_id = text_behind.strip()
                if len(resource_id):
                    self._citation_cur_id = resource_id
                if m.group(_I_CLOSE_CITATION) is not None:
                    self._citation_close()
                if m.group(_I_CLOSE_CITATION_DATA) is not None:
                    self._citationdata_open()

            # parsing citationdata
            elif self._state[-1] == _S_CITATIONDATA_IN:
                if self._citation_cur_id is None:
                    res_type = self.cite_type_default
                else:
                    res_type = self.resources[self._citation_cur_id]['TYPE']
                res_key = self.cite_key_default[res_type]

                # ignore formatting the data if it is destined to an ignored
                # resource key
                if res_key in self.resource_keys_ignored:
                    m = self._re_tag_close_citationdata_ignored.search(text)
                    start, endo = m.span()
                    text_behind = text[0:start]
                    text_behind = self._unescape(text_behind, tag=']')
                    text = text[endo:]
                    self._html[-1].append(text_behind)
                    if m.group(_I_CLOSE_CITATIONDATAIGNORED) is not None:
                        self._citationdata_close()
                else:
                    m = self._re_tag_close_citationdata.search(text)
                    start, endo = m.span()
                    text_behind = text[0:start]
                    text_behind = self._unescape(text_behind)
                    text = text[endo:]
                    self._html[-1].append(text_behind)
                    if m.group(_I_CLOSE_CITATIONDATA) is not None:
                        self._citationdata_close()
                    elif m.group(_I_CLOSE_CITATIONDATA_EMPHASIZE) is not None:
                        self._emphasize_open()
                    elif m.group(_I_CLOSE_CITATIONDATA_STRIKE) is not None:
                        self._strike_open()
                    elif m.group(_I_CLOSE_CITATIONDATA_CODE) is not None:
                        self._code_open(m.group(_I_CLOSE_CITATIONDATA_CODE))
                    elif m.group(_I_CLOSE_CITATIONDATA_SHORTCUT) is not None:
                        self._shortcut_add(m.group(
                            _I_CLOSE_CITATIONDATA_SHORTCUT)
                        )
                    elif m.group(_I_CLOSE_CITATIONDATA_CITATION) is not None:
                        self._citation_open()

    def flush(self, footnotes=True, bibliography=True):
        """Flush all pending objects: cited box resources such as figures,
        footnotes, bibliographies.
        """
        while len(self._state) > 1:
            state = self._state[-1]
            if   state == _S_PARAGRAPH_IN: self._paragraph_close()
            elif state == _S_EMPHASIZE_IN: self._emphasize_close()
            elif state == _S_STRIKE_IN   : self._strike_close()
            elif state == _S_CODE_IN     : self._code_close()
            elif state == _S_LIST_IN     : self._list_close()
            elif state == _S_LISTPARAGRAPH_IN : self._listparagraph_close()
            elif state == _S_HEADING_IN  : self._heading_close()
            elif state == _S_RESOURCE_IN : self._resource_close()
            elif state == _S_CITATION_IN : self._citation_close()
            elif state == _S_CITATIONDATA_IN : self._citationdata_close()

        if len(self._citations_pending_boxes):
            self._flush_pending_boxes()

        if footnotes:
            if len(self._footnote_items):
                self._html[-1].append(self.frmt_footnote_prefix)
                for bib_item in self._footnote_items:
                    self._html[-1].append(bib_item)
                self._html[-1].append(self.frmt_footnote_suffix)
                self._footnote_items = []

        if bibliography:
            if len(self._bibliography_items):
                self._html[-1].append(self.frmt_bibliography_prefix)
                for bib_item in self._bibliography_items:
                    self._html[-1].append(bib_item)
                self._html[-1].append(self.frmt_bibliography_suffix)
                self._bibliography_items = []

    def get_html(self):
        """Get the HTML representation of parsed texts.
        """
        html = ''.join(self._html[-1])
        self._html[-1] = []
        return html

    def forget_resources(self, resource=None):
        """Forget whether resources of given type were cited previously.
        """
        if resource is None:
            self.resources = {}
        else:
            if res_id in self.resources:
                del self.resources[res_id]

    def forget_citations(self, resource_type=None):
        """Forget whether resources of given type were cited previously.
        """
        if resource_type is None:
            self.resources_cited = {}
        else:
            for res_id in list(self.resources_cited):
                # i must remove need on self.resources.  currently this is
                # causing an inconvenience, since it forces user to never call
                # forget_citations() after forget_resources
                if resource_type == self.resources[res_id]['TYPE']:
                    del self.resources_cited[res_id]

    def forget_citation_counters(self, resource_type=None):
        """Reset the resource's counter of the given type.
        """
        if resource_type is None:
            self._citations_last_index = {}
        else:
            counter = self.resource_counters[resource_type]
            if counter in self._citations_last_index:
                del self._citations_last_index[counter]

    def forget_section_counters(self):
        """Reset the section index counters.
        """
        self._heading_index = [0] * 6
        self._heading_bookmark = [''] * 6

    def _unescape(self, text, tag=None):
        if tag is None:
            return self._re_unescape.sub(r'\1', text)
        else:
            return text.replace(self.escape + tag, tag)

    def _shortcut_add(self, s):
        if self._state[-1] == _S_START:
            self._paragraph_open()
        self._html[-1].append(self.shortcuts[s])

    def _replace_unsafe(self, text):
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def _flush_pending_boxes(self):
        self._html[-1] += self._citations_pending_boxes
        self._citations_pending_boxes = []

    def _paragraph_open(self):
        self._state.append(_S_PARAGRAPH_IN)
        self._html[-1].append(self.frmt_paragraph_prefix)

    def _paragraph_close(self):
        del self._state[-1]
        self._html[-1].append(self.frmt_paragraph_suffix)

    def _emphasize_open(self):
        if self._state[-1] == _S_START:
            self._paragraph_open()
        self._state.append(_S_EMPHASIZE_IN)
        self._html[-1].append(self.frmt_emph_prefix)

    def _emphasize_close(self):
        del self._state[-1]
        self._html[-1].append(self.frmt_emph_suffix)

    def _strike_open(self):
        if self._state[-1] == _S_START:
            self._paragraph_open()
        self._state.append(_S_STRIKE_IN)
        self._html[-1].append(self.frmt_strike_prefix)

    def _strike_close(self):
        del self._state[-1]
        self._html[-1].append(self.frmt_strike_suffix)

    def _code_open(self, tag_open):
        if self._state[-1] == _S_START and tag_open in self.code_inline:
            self._paragraph_open()
        self._state.append(_S_CODE_IN)
        self._code_tag_open = tag_open
        self._html[-1].append(
            self.frmt_code_prefix[tag_open].format(**{'OPEN':tag_open})
        )

    def _code_close(self):
        del self._state[-1]
        tag_close = self.code[self._code_tag_open]
        self._html[-1].append(
            self.frmt_code_suffix[self._code_tag_open].format(
                **{'CLOSE':tag_close}
            )
        )

    def _list_open(self, level, list_type):
        self._state.append(_S_LIST_IN)
        ordered = True if list_type == '+' else False
        self._list.append([level, ordered])
        if ordered:
            self._html[-1].append(self.frmt_olist_prefix)
        else:
            self._html[-1].append(self.frmt_ulist_prefix)
        self._html[-1].append(self.frmt_list_item_prefix)

    def _list_close(self):
        del self._state[-1]
        _, ordered = self._list[-1]
        del self._list[-1]
        self._html[-1].append(self.frmt_list_item_suffix)
        if ordered:
            self._html[-1].append(self.frmt_olist_suffix)
        else:
            self._html[-1].append(self.frmt_ulist_suffix)

    def _list_item_new(self, cur_level, cur_type):
        self._flush_pending_boxes()
        while True:
            prev_level, _ = self._list[-1]
            prev2_level, _ = self._list[-2]
            if cur_level == prev_level:
                self._html[-1].append(self.frmt_list_item_suffix)
                self._html[-1].append(self.frmt_list_item_prefix)
                break
            elif cur_level > prev_level:
                self._list_open(cur_level, cur_type)
                break
            elif cur_level > prev2_level:
                self._html[-1].append(self.frmt_list_item_suffix)
                self._html[-1].append(self.frmt_list_item_prefix)
                break
            elif cur_level < prev_level:
                self._list_close()

    def _listparagraph_open(self):
        self._flush_pending_boxes()
        self._state.append(_S_LISTPARAGRAPH_IN)

    def _listparagraph_close(self):
        del self._state[-1]

    def _heading_open(self, level, bookmark):
        self._state.append(_S_HEADING_IN)
        level = len(level) + self.heading_offset
        if level > 6: level = 6 
        self._heading_level = level
        self._heading_index[level-1] += 1
        self._heading_index[level:] = [0] * (6 - level)
        if bookmark is None:
            self._heading_bookmark[level-1] = str(self._heading_index[level-1])
            fullbookmark = '.'.join(
                i for i in self._heading_bookmark[self.heading_offset:level]
            )
        else:
            self._heading_bookmark[level-1] = bookmark
            fullbookmark = bookmark
        fullindex = '.'.join(
            str(i) for i in self._heading_index[self.heading_offset:level]
        )
        self._heading_fullindex = fullindex
        self._heading_fullbookmark = fullbookmark
        self._html[-1].append(
            self.frmt_heading_prefix.format(
                **{'LEVEL':level, 'INDEX':fullindex, 'BOOKMARK':fullbookmark}
            )
        )
        self.resources[fullbookmark] = {
            'TYPE'      : 'SECTION',
            'INDEX'     : fullindex,
            'BOOKMARK'  : fullbookmark
        }

    def _heading_close(self):
        del self._state[-1]
        self._html[-1].append(
            self.frmt_heading_suffix.format(
                **{
                    'LEVEL':self._heading_level,
                    'INDEX':self._heading_fullindex,
                    'BOOKMARK':self._heading_fullbookmark
                }
            )
        )

    def _resource_open(self, res_type, res_id):
        self._state.append(_S_RESOURCE_IN)
        self._resource_cur_id = res_id
        self.resources[res_id] = {'TYPE':res_type}
        self._html.append([])

    def _resource_close_entry(self):
        if self._resource_cur_entry_key is not None:
            resource = self.resources[self._resource_cur_id]
            resource[self._resource_cur_entry_key] = ''.join(self._html[-1])
            self._html[-1] = []
            self._resource_cur_entry_key = None

    def _resource_close(self):
        del self._state[-1]
        self._resource_close_entry()
        del self._html[-1]

    def _resource_ignored_key_open(self):
        self._state.append(_S_RESOURCE_IGNORED_KEY_IN)

    def _resource_ignored_key_close(self):
        del self._state[-1]

    def _citation_open(self):
        self._state.append(_S_CITATION_IN)

    def _citation_close(self):
        del self._state[-1]
        res_id = self._citation_cur_id
        res_data = self._citation_cur_data
        self._citation_cur_id = None
        self._citation_cur_data = None

        # assume a default resource identifier and type if appropriate
        if res_id is None and res_data is not None:
            self._citations_last_default_id_prefix += 1
            res_id = '{}{}'.format(
                self.cite_id_default,
                self._citations_last_default_id_prefix
            )
            self.resources[res_id] = {'TYPE': self.cite_type_default}

        # missing resource identifier?
        if res_id is None:
            self._html[-1].append(self.frmt_cite_error_inline.format(
                **{'ERROR':'no resource identifier'}
            ))
            return

        # should inline citation be disabled?
        if len(res_id) > 1 and res_id[0] == '!':
            inline_citation_enabled = False
            res_id = res_id[1:]
        else:
            inline_citation_enabled = True

        # get cited resource
        if res_id in self.resources:
            resource = self.resources[res_id]
        else:
            self._html[-1].append(self.frmt_cite_error_inline.format(
                **{'ERROR':"undefined resource '{}'".format(res_id)}
            ))
            return

        # get resource's type
        try:
            res_type = resource['TYPE']
        except KeyError as k:
            self._html[-1].append(self.frmt_cite_error_inline.format(
                **{'ERROR':"resource '{}' lacks {}".format(res_id, k)}
            ))
            return 

        # get resource's counter
        try:
            res_counter = self.resource_counters[res_type]
        except KeyError:
            self._html[-1].append(self.frmt_cite_error_inline.format(
                **{'ERROR':"resource '{}' lacks counter".format(res_id)}
            ))
            return 

        # get cited resource's index
        if res_id in self.resources_cited:
            res_index = self.resources_cited[res_id]
        else:
            if res_counter in self._citations_last_index:
                self._citations_last_index[res_counter] += 1
            else:
                self._citations_last_index[res_counter] = 1
            res_index = self._citations_last_index[res_counter]

        # add resource data into the resource if appropriate
        if res_type in self.cite_key_default and res_data is not None:
            resource[self.cite_key_default[res_type]] = res_data

        # build footnote items
        values = {'ID':res_id, 'INDEX':res_index}
        values.update(resource)
        if (
            res_id not in self.resources_cited
            and res_type in self.frmt_footnote_item
        ):
            try:
                self._footnote_items.append(
                    self.frmt_footnote_item[res_type].format(**values)
                )
            except KeyError as k:
                self._footnote_items.append(
                    self.frmt_cite_error_inline.format(
                        **{'ERROR':"resource '{}' lacks {}".format(res_id,k)}
                    )
                )

        # build bibliography items
        if (
            res_id not in self.resources_cited
            and res_type in self.frmt_bibliography_item
        ):
            try:
                self._bibliography_items.append(
                    self.frmt_bibliography_item[res_type].format(**values)
                )
            except KeyError as k:
                self._bibliography_items.append(
                    self.frmt_cite_error_inline.format(
                        **{'ERROR':"resource '{}' lacks {}".format(res_id,k)}
                    )
                )

        # inline resource citation
        if res_type in self.frmt_cite_inline and inline_citation_enabled:
            try:
                if self._state[-1] == _S_START:
                    self._paragraph_open()
                self._html[-1].append(self.frmt_cite_inline[res_type].format(
                    **values
                ))
            except KeyError as k:
                self._html[-1].append(self.frmt_cite_error_inline.format(
                    **{'ERROR':"resource '{}' lacks {}".format(res_id, k)}
                ))

        # box resource citation
        if res_id not in self.resources_cited:
            if res_type in self.frmt_cite_box:
                try:
                    self._citations_pending_boxes.append(
                        self.frmt_cite_box[res_type].format(**values)
                    )
                except KeyError as k:
                    self._citations_pending_boxes.append(
                        self.frmt_cite_error_box.format(
                            **{
                                'ERROR':"resource '{}' lacks '{}'".format(
                                    res_id, k
                                )
                            }
                        )
                    )

        self.resources_cited[res_id] = res_index

    def _citationdata_open(self):
        self._state.append(_S_CITATIONDATA_IN)
        self._html.append([])

    def _citationdata_close(self):
        self._citation_cur_data = ''.join(self._html[-1])
        del self._html[-1]
        del self._state[-1]
        self._citation_close()
