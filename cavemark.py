import re


class CaveMark:
    """Create a new CaveMark string parser object, then use the HTML method to
    convert input CaveMark strings into their HTML representation.
    """

    def __init__(
        self, resources=None, escape=None, ignore=None,
        resources_cite_inline_format=None, resources_cite_box_format=None,
        paragraph_prefix=None, paragraph_suffix=None, emphasize_format=None,
        footnote_sc_format=None, footnote_cnt_format=None,
        footnote_item_format=None, code_inline_format=None,
        code_box_format=None, list_ordered_format=None,
        list_unordered_format=None, list_item_format=None, heading_format=None,
        heading_level_offset=None
    ):
        # references/resources dictionary
        if resources is None:
            self.resources              = {}
        else:
            self.resources              = resources

        # escape char is used to literally print stuff
        if escape is None:
            self.escape                 = '\\'
        else:
            self.escape                 = escape     

        # which open/closing tags define intervals to disable parsing on
        if ignore is None:
            self.ignore                 = {
                '\[' : '\]',
                '\(' : '\)',
                '$$' : '$$',
            }
        else:
            self.ignore                 = ignore

        # append ignore tags with cavemark's code tags
        self.ignore['`']                =  '`'
        self.ignore['```']              =  '```'

        # how to expand resources where they are cited in the text
        if resources_cite_inline_format is None:
            self.resources_cite_inline_format = {
                'url'       :' <a href="{url}">[{INDEX}]</a>',
                'image'     :' <a href="#{ID}">Figure {INDEX}</a>',
                'quotation' :' <a href="#{ID}">Quote {INDEX}</a>',
                'definition':' <a href="#{ID}">Definition {INDEX}</a>',
                'theorem'   :' <a href="#{ID}">Theorem {INDEX}</a>',
            }
        else:
            self.resources_cite_inline_format = resources_cite_inline_format

        # how to expand resources after the paragraph where they were cited, in
        # a box of their own.  only add those that should to be expanded into
        # boxes, such as figures, theorems, quotes, etc.  resource types that
        # are not defined here will not have box expansion.
        if resources_cite_box_format is None:
            self.resources_cite_box_format = {
                'image'     :'<figure id="{ID}">\n'
                             '  <img alt="{alt}" src="{url}" />\n'
                             '  <figcaption>\n'
                             '    <strong>Fig. {INDEX}:</strong> {caption}.\n'
                             '  </figcaption>\n'
                             '</figure>\n\n',
                'quotation' :'<blockquote id="{ID}">\n'
                             '  {text} -- {author}\n'
                             '</blockquote>\n\n',
                'definition':'<p id="{ID}" class="definition">\n'
                             '  {text}\n'
                             '</p>\n\n',
                'theorem'   :'<p id="{ID}" class="theorem">\n'
                             '  {text}\n'
                             '</p>\n\n',
            }
        else:
            self.resources_cite_box_format = resources_cite_box_format

        # paragraphs prefix
        if paragraph_prefix is None:
            self.paragraph_prefix       = '<p>'
        else:
            self.paragraph_prefix       = paragraph_prefix

        # paragraphs suffix
        if paragraph_suffix is None:
            self.paragraph_suffix       = '</p>\n\n'
        else:
            self.paragraph_suffix       = paragraph_suffix

        # how should emphasized texts look like
        if emphasize_format is None:
            self.emphasize_format       = '<em>{TEXT}</em>'
        else:
            self.emphasize_format       = emphasize_format

        # how should footnote superscripts look like
        if footnote_sc_format is None:
            self.footnote_sc_format     = '<sup>'\
                                          '<a href="#f{ID}">{ID}</a>'\
                                          '</sup>'
        else:
            self.footnote_sc_format     = footnote_sc_format

        # how should footnotes container look like
        if footnote_cnt_format is None:
            self.footnote_cnt_format    = '<hr />\n'\
                                          '<ol>\n{TEXT}</ol>\n\n'
        else:
            self.footnote_cnt_format    = footnote_cnt_format

        # how should each footnote item look like
        if footnote_item_format is None:
            self.footnote_item_format   = '  <li id="f{ID}">{TEXT}</li>\n'
        else:
            self.footnote_item_format   = footnote_item_format

        # how should code, that's represented inline, look like
        if code_inline_format is None:
            self.code_inline_format     = '<code>{TEXT}</code>'
        else:
            self.code_inline_format     = code_inline_format

        # how should code, that's represented in a box, look like
        if code_box_format is None:
            self.code_box_format        = '<pre><code>{TEXT}</code></pre>'
        else:
            self.code_box_format        = code_box_format

        # how should ordered lists look like
        if list_ordered_format is None:
            self.list_ordered_format    = '<ol>\n{TEXT}</ol>\n\n'
        else:
            self.list_ordered_format    = list_ordered_format

        # how should unordered lists look like
        if list_unordered_format is None:
            self.list_unordered_format  = '<ul>\n{TEXT}</ul>\n\n'
        else:
            self.list_unordered_format  = list_unordered_format

        # how should items in lists look like
        if list_item_format is None:
            self.list_item_format       = '  <li>{TEXT}</li>\n'
        else:
            self.list_item_format       = list_item_format

        # how should headings look like
        if heading_format is None:
            self.heading_format         = '<h{LEVEL}>{TEXT}</h{LEVEL}>\n\n'
        else:
            self.heading_format         = heading_format

        # offset heading level.  e.g. if offset=1, # becomes h2 instead of h1
        if heading_level_offset is None:
            self.heading_level_offset   = 1
        else:
            self.heading_level_offset   = heading_level_offset

        # resource citation states
        self._resources_last_index      = {}
        self._resources_inline_cited    = {}
        self._resources_box_cited       = set()
        self._resources_pending_boxes   = []

        # footnote superscript states
        self._footnotes_last_index      = 1
        self._footnotes_items           = []

        # compile all regular expressions
        self.compile_re()

    def compile_re(self):
        # thanks to squirrel from freenode/#python for suggesting the re
        # pattern to escape stuff: https://regex101.com/r/fdf9Ul/3
        re_ignore_pattern = '(?:{})'.format(
            '|'.join(
                [
                    r'{}(?:{}.|[^{}])+?{}'.format(
                        re.escape(o),
                        re.escape(self.escape),
                        re.escape(re.escape(self.ignore[o][0])),
                        re.escape(self.ignore[o])
                    ) for o in self.ignore
                ]
            )
        )
        re_unescable = '^(?:{OPEN})(.*?)(?:{CLOSE})$'.format(
            **{
                'OPEN' :'|'.join(
                    re.escape(o) for o in self.ignore
                ),
                'CLOSE':'|'.join(
                    re.escape(self.ignore[o]) for o in self.ignore
                ),
            }
        )
        re_unesc = '{}(.)'.format(re.escape(self.escape))
        self._re_ignore     = re.compile(re_ignore_pattern, flags=re.DOTALL)
        self._re_unescable  = re.compile(re_unescable, flags=re.DOTALL)
        self._re_unesc      = re.compile(re_unesc, flags=re.DOTALL)
        self._re_paragraph  = re.compile(r'\n\s*\n')
        self._re_pending_p  = re.compile(r'\n\s*\n\s*$')
        self._re_closing_p  = re.compile(r'^\s*\n\s*\n')
        self._re_emphasize  = re.compile(
            r'\s+[^{0}]_(.*?\S+.*?)[^{0}]_', flags=re.DOTALL
        )
        self._re_citation   = re.compile(r'\s\[\s*?(\S+)\s*?\]')
        self._re_footnote   = re.compile(
            r'\^\[\s*?(\S+.*?)\s*?\]', flags=re.DOTALL
        )
        self._re_headings   = re.compile(r'(#+)\s*?(\S+.*)', flags=re.DOTALL)
        self._re_ul         = re.compile(r'\n\s*?\*')
        self._re_ol         = re.compile(r'\n\s*?\.1')

    def get_html(
        self,
        s,
    ):
        """Parse a string s, as per the semantics of CaveMark, and return its
        corresponding HTML.
        """

        # states
        self._pending_paragraph = False

        # remove unsafe things
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        s = s.replace('&', '&amp;')
         
        # parse s into html
        # thx to Yhg1s from freenode/#python for suggesting this general
        # layout: https://paste.pound-python.org/show/tJi254LhZU1rIo2Y7sOo/ 
        prev_end = -1
        html = ''
        for m in self._re_ignore.finditer(s):
            start, endo = m.span()
            end = endo - 1
            html += self._process(s[prev_end+1:start])
            if s[start:start+3] == s[end-2:endo] == '```':
                unescaped = self._re_unesc.sub(r'\1', s[start+3:end-2])
                html += self.code_box_format.format(
                    **{'TEXT':unescaped}
                )
            elif s[start] == s[end] == '`':
                unescaped = self._re_unesc.sub(r'\1', s[start+1:end])
                html += self.code_inline_format.format(
                    **{'TEXT':unescaped}
                )
            else:
                unescapable = self._re_unescable.search(s[start:endo])
                unescaped = self._re_unesc.sub(r'\1', unescapable.group(1))
                html += self.code_inline_format.format(
                    **{'TEXT':unescaped}
                )
            prev_end = end
        html += self._process(s[prev_end+1:])

        # cited boxy resources that didn't get the opporrtunity to be added yet
        for box in self._resources_pending_boxes:
            html += box
        self._resources_pending_boxes = []

        # footnotes list
        html += self.footnote_cnt_format.format(
            **{
                'TEXT' : ''.join(
                    [
                        self.footnote_item_format.format(
                            **{
                                'ID'    :   i,
                                'TEXT'  :   j,
                            }
                        ) for i, j in self._footnotes_items
                    ]
                )
            }
        )
        self._footnotes_items = []

        return html

    def _res_process(self, m):
        res_id = m.group(1)
        if res_id in self.resources:
            res_type = self.resources[res_id]['TYPE']

            # find resource's index
            if res_id in self._resources_inline_cited:
                res_index = self._resources_inline_cited[res_id]
            else:
                if res_type in self._resources_last_index:
                    self._resources_last_index[res_type] += 1
                else:
                    self._resources_last_index[res_type] = 1
                res_index = self._resources_last_index[res_type]
                self._resources_inline_cited[res_id] = res_index

            # inline resource expansion - if supported
            if res_type in self.resources_cite_inline_format:
                res_html = self.resources_cite_inline_format[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
            else:
                res_html = '[{}]'.format(res_id)

            # in-box resource expansion - if supported, and if needed (e.g. if
            # box is placed previously, then no need to do it again)
            if (
                res_id not in self._resources_box_cited
                and res_type in self.resources_cite_box_format
            ):
                res_html_box = self.resources_cite_box_format[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
                self._resources_pending_boxes.append(res_html_box)
                self._resources_box_cited.add(res_id)

        return res_html

    def _footnotes_process(self, m):
        footnote_text               = m.group(1)
        footnote_id                 = self._footnotes_last_index
        self._footnotes_last_index += 1

        footnote_html = self.footnote_sc_format.format(
            **{
                'ID'    :   footnote_id,
                'TEXT'  :   footnote_text,
            }
        )

        self._footnotes_items.append((footnote_id, footnote_text))

        return footnote_html

    def _process(self, s):
        paragraphs_orig = self._re_paragraph.split(s)
        paragraphs_html = []

        # will last paragraph be a pending one?
        if self._re_pending_p.search(s):
            pending_paragraph_to_be = False
        else:
            pending_paragraph_to_be = True

        # is the pending paragraph closed now?
        if self._re_closing_p.search(s):
            paragraphs_html.append(self.paragraph_suffix)
            self._pending_paragraph = False

        # parse paragraphs
        for i in range(0, len(paragraphs_orig)):
            # identify paragraph treatment
            if i == 0 and self._pending_paragraph:
                paragraph_openable = False
            else:
                paragraph_openable = True

            if i == len(paragraphs_orig) - 1 and pending_paragraph_to_be:
                paragraph_closeable = False
            else:
                paragraph_closeable = True

            # finish pending boxes.
            if paragraph_openable:
                for box in self._resources_pending_boxes:
                    paragraphs_html.append(box)
                self._resources_pending_boxes = []

            # if paragraph is empty, skip this iteration.
            p = paragraphs_orig[i]
            p = p.strip()
            if not len(p):
                continue

            # emphasized text
            p = self._re_emphasize.sub(
                self.emphasize_format.format(**{'TEXT':r'\g<1>'}),
                p
            )

            # format cited resources
            p = self._re_citation.sub(self._res_process, p)

            # format footnotes
            p = self._re_footnote.sub(self._footnotes_process, p)

            # headings
            if p[0] == '#' and paragraph_openable:
                m = self._re_headings.match(p)
                paragraphs_html.append(
                    self.heading_format.format(
                        **{
                            'LEVEL' : (
                                len(m.group(1))
                                + self.heading_level_offset
                            ),
                            'TEXT'  : m.group(2),
                        }
                    )
                )

            # unordered lists
            elif p[0] == '*' and paragraph_openable:
                items = self._re_ul.split(p[1:])
                paragraphs_html.append(
                    self.list_unordered_format.format(
                        **{
                            'TEXT'  : ''.join(
                                [
                                    self.list_item_format.format(
                                        **{'TEXT':item}
                                    )
                                    for item in items
                                ]
                            )
                        }
                    )
                )

            # ordered lists
            elif p[0:2] == '.1' and paragraph_openable:
                items = self._re_ol.split(p[2:])
                paragraphs_html.append(
                    self.list_ordered_format.format(
                        **{
                            'TEXT'  : ''.join(
                                [
                                    self.list_item_format.format(
                                        **{'TEXT':item}
                                    )
                                    for item in items
                                ]
                            )
                        }
                    )
                )

            # paragraphs
            else:
                paragraphs_html.append('{}{}{}'.format(
                    self.paragraph_prefix if paragraph_openable else '',
                    p,
                    self.paragraph_suffix if paragraph_closeable else '',
                ))

        self._pending_paragraph = pending_paragraph_to_be

        return ''.join(paragraphs_html)
