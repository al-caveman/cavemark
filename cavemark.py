import re

# parser states
S_PENDING_H         = 0
S_PENDING_P         = 1
S_PENDING_UL        = 2
S_PENDING_OL        = 3
S_PENDING_FOOTNOTE  = 4

class CaveMark:
    """Create a new CaveMark string parser object,
    """

    def __init__(
        self, resources=None, escape=None, ignore=None, h_offset=None,
        frmt_fn_sc=None frmt_cite_inline=None, frmt_cite_box=None,
        frmt_p_prefix=None, frmt_p_suffix=None, frmt_emph=None,
        frmt_code_inline=None, frmt_code_box=None, frmt_list_o_prefix=None,
        frmt_list_o_suffix=None, frmt_list_u_prefix=None,
        frmt_list_u_suffix=None, frmt_list_item_prefix=None,
        frmt_list_item_suffix=None, frmt_h_prefix=None, frmt_h_suffix=None,
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

        # opening/closing tags that define substrings to ignore parsing in
        if ignore is None:
            self.ignore                 = {
                '\[' : '\]',
                '\(' : '\)',
                '$$' : '$$',
            }
        else:
            self.ignore                 = ignore
        self.ignore['`']                =  '`'
        self.ignore['```']              =  '```'

        # offset heading level.  e.g. if offset=1, "# title" becomes
        # "<h2>title</h2>" instead of "<h1>..."
        if h_offset is None:
            self.h_offset = 1
        else:
            self.h_offset = h_offset

        # footnote superscript format
        if frmt_fn_sc is None:
            self.frmt_fn_sc = '<sup><a href="#fn_{INDEX}">{INDEX}</a></sup>'
        else:
            self.frmt_fn_sc = frmt_fn_sc

        # inline citation format
        if frmt_cite_inline is None:
            self.frmt_cite_inline = {
                'url'       :' <a href="{url}">[{INDEX}]</a>',
                'image'     :' <a href="#cite_{ID}">Figure {INDEX}</a>',
                'quotation' :' <a href="#cite_{ID}">Quote {INDEX}</a>',
                'definition':' <a href="#cite_{ID}">Definition {INDEX}</a>',
                'theorem'   :' <a href="#cite_{ID}">Theorem {INDEX}</a>',
            }
        else:
            self.frmt_cite_inline = frmt_cite_inline

        # box citation format.
        if frmt_cite_box is None:
            self.frmt_cite_box = {
                'image'     :'<figure id="cite_{ID}">\n'
                             '  <img alt="{alt}" src="{url}" />\n'
                             '  <figcaption>\n'
                             '    <strong>Fig. {INDEX}:</strong> {caption}.\n'
                             '  </figcaption>\n'
                             '</figure>\n\n',
                'quotation' :'<blockquote id="cite_{ID}">\n'
                             '  {text} -- {author}\n'
                             '</blockquote>\n\n',
                'definition':'<p id="cite_{ID}" class="definition">\n'
                             '  {text}\n'
                             '</p>\n\n',
                'theorem'   :'<p id="cite_{ID}" class="theorem">\n'
                             '  {text}\n'
                             '</p>\n\n',
            }
        else:
            self.frmt_cite_box = frmt_cite_box

        # paragraphs format
        if frmt_p_prefix is None:
            self.frmt_p_prefix = '<p>'
        else:
            self.frmt_p_prefix = frmt_p_prefix
        if p_suffix is None:
            self.frmt_p_suffix = '</p>\n\n'
        else:
            self.frmt_p_suffix = frmt_p_suffix

        # emphasized text format
        if frmt_emph is None:
            self.frmt_emph = '<em>{TEXT}</em>'
        else:
            self.frmt_emph = frmt_emph

        # inline code format
        if frmt_code_inline is None:
            self.frmt_code_inline = '<code>{TEXT}</code>'
        else:
            self.frmt_code_inline = frmt_code_inline

        # box code format
        if frmt_code_box is None:
            self.frmt_code_box = '<pre><code>{TEXT}</code></pre>'
        else:
            self.frmt_code_box = frmt_code_box

        # ordered lists format
        if frmt_list_o_prefix is None:
            self.frmt_list_o_prefix = '<ol>\n'
        else:
            self.frmt_list_o_prefix = frmt_list_o_prefix
        if frmt_list_o_suffix is None:
            self.frmt_list_o_suffix = '</ol>\n\n'
        else:
            self.frmt_list_o_suffix = frmt_list_o_suffix

        # unordered lists format
        if frmt_list_u_prefix is None:
            self.frmt_list_u_prefix = '<ul>\n'
        else:
            self.frmt_list_u_prefix = frmt_list_u_prefix
        if frmt_list_u_suffix is None:
            self.frmt_list_u_suffix = '</ul>\n\n'
        else:
            self.frmt_list_u_suffix = frmt_list_u_suffix

        # listed items format
        if frmt_list_item_prefix is None:
            self.frmt_list_item_prefix = '  <li>'
        else:
            self.frmt_list_item_prefix = frmt_list_item_prefix
        if frmt_list_item_suffix is None:
            self.frmt_list_item_suffix = '</li>\n'
        else:
            self.frmt_list_item_suffix = frmt_list_item_suffix

        # headings format
        if frmt_h_prefix is None:
            self.frmt_h_prefix = '<h{LEVEL}>'
        else:
            self.frmt_h_prefix = frmt_h_prefix
        if frmt_h_suffix is None:
            self.frmt_h_suffix = '</h{LEVEL}>\n\n'
        else:
            self.frmt_h_suffix = frmt_h_suffix

        # states
        self._res_last_index = {}
        self._res_inline_cited = {}
        self._res_box_cited = set()
        self._res_pending_boxes = []
        self._fn_last_index = 0
        self.footnotes = []

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
                        re.escape(self.ignore[o][0]),
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
        self._re_unit_sep_mid = re.compile(r'\n\s*?\n')
        self._re_unit_sep_start = re.compile(r'^\s*?\n\s*?\n')
        self._re_unit_sep_end = re.compile(r'\n\s*?\n\s*?$')
        self._re_h          = re.compile(
                r'^\s*?(#+)\s*?(\S+.*?)$', flags=re.DOTALL
        )
        self._re_emph       = re.compile(
            r'[^{0}]_(.*?\S+.*?)[^{0}]_'.format(self.escape),
            flags=re.DOTALL
        )
        self._re_cite       = re.compile(r'(?:\s|^)\[\s*?(\S+)\s*?\]')
        self._re_fn         = re.compile(
            r'[^{0}]\^\[(.+?)([^{0}]\]|$)'.format(self.escape),
            flags=re.DOTALL
        )

    def parse(self, s):
        """Parse a string s, as per the semantics of CaveMark, and return its
        corresponding HTML.
        """

        # set initial states
        self._html = []
        self._units_pending = []

        # remove unsafe things
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        s = s.replace('&', '&amp;')
         
        # parse s into html
        # thx to Yhg1s from freenode/#python for suggesting this general
        # layout: https://paste.pound-python.org/show/tJi254LhZU1rIo2Y7sOo/ 
        first = True
        prev_endo = 0
        for m in self._re_ignore.finditer(s):
            start, endo = m.span()
            self._html.append(self._process(s[prev_end:start]))
            if s[start:start+3] == s[endo-3:endo] == '```':
                unescaped = self._re_unesc.sub(r'\1', s[start+3:endo-3])
                self._html.append(self.code_box_format.format(
                    **{'TEXT':unescaped}
                ))
            elif s[start] == s[end] == '`':
                unescaped = self._re_unesc.sub(r'\1', s[start+1:endo-1])
                self._html.append(self.code_inline_format.format(
                    **{'TEXT':unescaped}
                ))
            else:
                unescapable = self._re_unescable.search(s[start:endo])
                unescaped = self._re_unesc.sub(r'\1', unescapable.group(1))
                html.append(self.code_inline_format.format(
                    **{'TEXT':unescaped}
                ))
            prev_end = endo
            first = False
        self._html.append(self._process(s[prev_endo:]))

    def flush(self):
        """Flush all pending objects.  E.g. pending cited box resources such as
        figures.
        """
        self._html += self._res_pending_boxes
        self._res_pending_boxes = []

    def get_html(self):
        """Get the HTML representation of your CaveMark string.
        """
        return ''.join(self._html)

    def _res_process(self, m):
        res_id = m.group(1)
        if res_id in self.resources:
            res_type = self.resources[res_id]['TYPE']

            # find resource's index
            if res_id in self._res_inline_cited:
                res_index = self._res_inline_cited[res_id]
            else:
                if res_type in self._res_last_index:
                    self._res_last_index[res_type] += 1
                else:
                    self._res_last_index[res_type] = 1
                res_index = self._res_last_index[res_type]
                self._res_inline_cited[res_id] = res_index

            # inline resource expansion - if supported
            if res_type in self.frmt_cite_inline:
                res_html = self.frmt_cite_inline[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
            else:
                res_html = '[{}]'.format(res_id)

            # in-box resource expansion - if supported, and if needed (e.g. if
            # box is placed previously, then no need to do it again)
            if (
                res_id not in self._res_box_cited
                and res_type in self.res_cite_box_format
            ):
                res_html_box = self.frmt_cite_box[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
                self._res_pending_boxes.append(res_html_box)
                self._res_box_cited.add(res_id)

        return res_html

    def _process(self, s):
        # is the ist unit a new one?
        if self._re_unit_sep_start.search(s):
            1st_unit_new = False
        else:
            1st_unit_new = True

        # will the last unit be a pending one?
        if self._re_unit_sep_end.search(s):
            last_unit_pending = False
        else:
            last_unit_pending = True

        # process emphasized texts
        s = self._re_emph.sub(
            self.frmt_emph.format(**{'TEXT':r'\g<1>'}),
            s
        )

        # process cited resources
        s = self._re_citation.sub(self._res_process, s)

        # create units
        units_orig = self._re_unit_sep_mid.split(s)

        # parse units
        for i in range(0, len(units_orig)):
            # place pending boxes.
            units_html += self._res_pending_boxes
            self._res_pending_boxes = []

            # will this unit be pending?
            if i == len(units_orig)-1 and last_unit_pending:
                this_unit_pending = True
            else:
                this_unit_pending = False

            # process new unit
            u = units_orig[i]
            if len(self._units_pending) == 0:
                # new heading
                m = self._re_h.match(u)
                if m:
                    # will this unit be pending?
                    if this_unit_pending:
                        self._units_pending.append(S_PENDING_H)

                    # add prefix
                    level = len(m.group(1))
                    self._html.append(
                        self.frmt_h_prefix.format(
                            **{'LEVEL':level}
                        )
                    )

                    # add heading text, while also processing footnotes
                    text = m.group(2)
                    prev_endo = 0
                    for fn in self._re_fn.finditer(text):
                        start, endo = fn.span()
                        self._html.append(text[prev_endo:start])
                        self._fn_last_index += 1
                        self._html.append(
                            self.frmt_fn_sc.format(
                                **{'INDEX':self._fn_last_index}
                            )
                        )
                        self.footnotes.append(
                            [self._fn_last_index, fn.group(1)]
                        )
                        if fn.group(2) != ']' and this_unit_pending:
                            self._units_pending.append(S_PENDING_FOOTNOTE)
                        prev_endo = endo
                    self._html.append(text[prev_endo:])

                    # add suffix
                    if len(self._units_pending) == 0:
                        self._html.append(
                            self.frmt_h_suffix.format(
                                **{'LEVEL':level}
                            )
                        )

                    continue

                # new paragraph
                # will this unit be pending?
                if this_unit_pending:
                    self._units_pending.append(S_PENDING_P)

                # add prefix
                self._html.append(self.frmt_p_prefix)

                # add paragraph, while also processing footnotes
                prev_endo = 0
                for fn in self._re_fn.finditer(u):
                    start, endo = fn.span()
                    self._html.append(u[prev_endo:start])
                    self._fn_last_index += 1
                    self._html.append(
                        self.frmt_fn_sc.format(
                           **{'INDEX':self._fn_last_index}
                        )
                    )
                    self.footnotes.append(
                        [self._fn_last_index, fn.group(1)]
                    )
                    if fn.group(2) != ']' and last_unit_pending:
                        self._units_pending.append(S_PENDING_FOOTNOTE)
                    prev_endo = endo
                self._html.append(u[prev_endo:])
                continue

            # process pending header
            elif self._units_pending[-1] == S_PENDING_H:
                pass

            # process pending paragraph
            elif self._units_pending[-1] == S_PENDING_P:
                pass

            # process pending footnote
            elif self._units_pending[-1] == S_PENDING_FOOTNOTE:
                pass

            else:
                raise Exception(
                    'unknown state "{}"'.format(self._units_pending[-1])
                )
