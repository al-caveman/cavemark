import re

# parser states
S_START             = 0
S_HEADING_IN        = 1
S_PARAGRAPH_IN      = 2
S_FOOTNOTE          = 3
S_LIST_IN           = 4

class CaveMark:
    """Create a new CaveMark string parser object,
    """

    def __init__(
        self, resources=None, escape=None, ignore=None, ignore_unescape=None,
        heading_offset=None, frmt_footnote_ss=None, frmt_footnote_item=None,
        frmt_footnote_cnt=None, frmt_cite_inline=None, frmt_cite_box=None,
        frmt_bibliography_item=None, frmt_bibliography_cnt=None,
        frmt_paragraph_prefix=None, frmt_paragraph_suffix=None, frmt_emph=None,
        frmt_ignore=None, frmt_code_inline=None, frmt_code_box=None,
        frmt_olist_prefix=None, frmt_olist_suffix=None, frmt_ulist_prefix=None,
        frmt_ulist_suffix=None, frmt_list_item_prefix=None,
        frmt_list_item_suffix=None, frmt_heading_prefix=None,
        frmt_heading_suffix=None,
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
        self.ignore['```']              =  '```'
        self.ignore['`']                =  '`'
        self.ignore['^{']               =  '}'

        # ignored text intervals to unescape
        if ignore_unescape is None:
            self.ignore_unescape        = set()
        else:
            self.ignore_unescape        = ignore_unescape
        self.ignore_unescape.add('```')
        self.ignore_unescape.add('`')
        self.ignore_unescape.add('^{')

        # offset heading level.  e.g. if offset=1, "# title" becomes
        # "<h2>title</h2>" instead of "<h1>..."
        if heading_offset is None:
            self.heading_offset = 1
        else:
            self.heading_offset = heading_offset

        # footnote superscript format
        if frmt_footnote_ss is None:
            self.frmt_footnote_ss = '<sup>'\
                                    '<a href="#fn_{INDEX}">'\
                                    '{INDEX}'\
                                    '</a>'\
                                    '</sup>'
        else:
            self.frmt_footnote_ss = frmt_footnote_ss

        # footnote items format
        if frmt_footnote_item is None:
            self.frmt_footnote_item = '<li id="fn_{INDEX}">'\
                                      '{INDEX}. {TEXT}'\
                                      '</li>\n'
        else:
            self.frmt_footnote_item = frmt_footnote_item

        # footnote container format
        if frmt_footnote_cnt is None:
            self.frmt_footnote_cnt = '<hr/>\n <ul style="list-style:none;'\
                                     'padding:0; margin:0;">{TEXT}</ul>\n\n'
        else:
            self.frmt_footnote_cnt = frmt_footnote_cnt

        # inline citation format
        if frmt_cite_inline is None:
            self.frmt_cite_inline = {
                'url'       :' <a href="{url}">[{INDEX}]</a>',
                'book'      :' <a href="#cite_{ID}">[{INDEX}]</a>',
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
                'image'     :'<figure id="cite_{ID}" '
                             'style="text-align:center;">\n'
                             '  <img alt="{alt}" src="{url}" />\n'
                             '  <figcaption>\n'
                             '    <strong>Fig. {INDEX}:</strong> {caption}\n'
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

        # bibliography items format
        if frmt_bibliography_item is None:
            self.frmt_bibliography_item = {
                'book'  :'<li id="cite_{ID}">[{INDEX}] {authors}, '
                         '&ldquo;<em>{title}</em>&ldquo;, {publisher}, '
                         '{year}.</li>\n',
            }
        else:
            self.frmt_bibliography_item = frmt_bibliography_item

        # bibliography container format
        if frmt_bibliography_cnt is None:
            self.frmt_bibliography_cnt = '<h4>bibliography</h4>\n'\
                                         '<ul style="list-style:none;'\
                                         'padding:0; margin:0;">\n'\
                                         '{TEXT}</ul>\n\n'
        else:
            self.frmt_bibliography_cnt = frmt_bibliography_cnt

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
        if frmt_emph is None:
            self.frmt_emph = '<em>{TEXT}</em>'
        else:
            self.frmt_emph = frmt_emph

        # ignore format
        if frmt_ignore is None:
            self.frmt_ignore = {
                '\[' : '<strong>{OPEN}{TEXT}{CLOSE}</strong>',
                '\(' : '<strong>{OPEN}{TEXT}{CLOSE}</strong>',
                '$$' : '<strong>{OPEN}{TEXT}{CLOSE}</strong>',
            }
        else:
            self.frmt_ignore = frmt_ignore

        # code format
        if frmt_code_inline is None:
            frmt_code_inline    = '<code>{TEXT}</code>'
        if frmt_code_box is None:
            frmt_code_box       = '<pre><code>{TEXT}</code></pre>'
        self.frmt_ignore['`']   = frmt_code_inline
        self.frmt_ignore['```'] = frmt_code_box

        # ordered lists format
        if frmt_olist_prefix is None:
            self.frmt_olist_prefix = '{LEVEL}<ol>\n'
        else:
            self.frmt_olist_prefix = frmt_olist_prefix
        if frmt_olist_suffix is None:
            self.frmt_olist_suffix = '{LEVEL}</ol>\n\n'
        else:
            self.frmt_olist_suffix = frmt_olist_suffix

        # unordered lists format
        if frmt_ulist_prefix is None:
            self.frmt_ulist_prefix = '{LEVEL}<ul>\n'
        else:
            self.frmt_ulist_prefix = frmt_ulist_prefix
        if frmt_ulist_suffix is None:
            self.frmt_ulist_suffix = '{LEVEL}</ul>\n\n'
        else:
            self.frmt_ulist_suffix = frmt_ulist_suffix

        # listed items format
        if frmt_list_item_prefix is None:
            self.frmt_list_item_prefix = '{LEVEL}  <li>'
        else:
            self.frmt_list_item_prefix = frmt_list_item_prefix
        if frmt_list_item_suffix is None:
            self.frmt_list_item_suffix = '</li>\n'
        else:
            self.frmt_list_item_suffix = frmt_list_item_suffix

        # headings format
        if frmt_heading_prefix is None:
            self.frmt_heading_prefix = '<h{LEVEL}>'
        else:
            self.frmt_heading_prefix = frmt_heading_prefix
        if frmt_heading_suffix is None:
            self.frmt_heading_suffix = '</h{LEVEL}>\n\n'
        else:
            self.frmt_heading_suffix = frmt_heading_suffix

        # states
        self._state = [S_START]
        self._html = []
        self._resources_last_index = {}
        self._resources_pending_boxes = []
        self._resources_bib_flushed = set()
        self._footnotes_last_index = 0
        self._list = [[-1, None]]
        self._list_need_item_suffix = False
        self.resources_cited = {}
        self.footnotes = []

        # compile all regular expressions
        self.compile_re()

    def compile_re(self):
        re_ignore_pattern = r'(?:{})'.format(
            r'|'.join([
                r'(?<!{0})({1})(.*?)((?<!{0}){2})'.format(
                    re.escape(self.escape),
                    re.escape(o),
                    re.escape(self.ignore[o]),

                )
            for o in self.ignore])
        )
        self._re_ignore = re.compile(re_ignore_pattern, flags=re.DOTALL)
        self._re_ignore_unescs = {
            o : re.compile(
                r'{}({})'.format(
                    re.escape(self.escape),
                    re.escape(self.ignore[o])
                )
            ) for o in self.ignore if o in self.ignore_unescape
        }
        self._re_unit_sep   = re.compile(r'\n\s*\n')
        self._re_heading    = re.compile(
            r'^\s*?(?<!{})(#+)\s+(.*)'.format(re.escape(self.escape)),
            flags=re.DOTALL
        )
        self._re_emph       = re.compile(
            r'(?<!{0})_(.*?\S+.*?)(?<!{0})_'.format(re.escape(self.escape)),
            flags=re.DOTALL
        )
        self._re_cite       = re.compile(
            r'(?<!{0})\[\s*(\S+?)\s*(?<!{0})\]'.format(
                re.escape(self.escape)
            )
        )
        self._re_list       = re.compile(
            r' *(?<!{0})(?:\*|\+)'.format(
                re.escape(self.escape)
            ),
            flags=re.DOTALL
        )
        self._re_list_items = re.compile(
            r'( *)(?<!{})(\*|\+)\s*(\S.*?)(?=(?:\n *\*|\n *\+|$))'.format(
                re.escape(self.escape)
            ),
            flags=re.DOTALL
        )

    def parse(self, text):
        """Parse a string text, as per the semantics of CaveMark.
        """

        # remove unsafe things
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('&', '&amp;')
         
        # parse text into html chunks
        prev_endo = 0
        for m in self._re_ignore.finditer(text):
            start, endo = m.span()
            self._parse_units(text[prev_endo:start])
            matched         = [i for i in m.groups() if i is not None]
            ignr_open       = matched[0]
            ignr_text       = matched[1]
            ignr_close      = matched[2]
            if ignr_open in self.ignore_unescape:
                ignr_text   = self._re_ignore_unescs[ignr_open].sub(
                    r'\1',
                    ignr_text
                )
            if ignr_open == '^{':
                self._state.append(S_FOOTNOTE)
                self._parse_units(ignr_text)
            else:
                if ignr_open in self.frmt_ignore:
                    ignr_text = self.frmt_ignore[ignr_open].format(
                        **{
                            'OPEN'  : ignr_open,
                            'TEXT'  : ignr_text,
                            'CLOSE' : ignr_close,
                        }
                    )
                self._html.append(ignr_text)
            prev_endo = endo
        self._parse_units(text[prev_endo:])

    def flush(self, footnotes=True, bibliography=True):
        """Flush all pending objects: cited box resources such as figures,
        footnotes, bibliographies.
        """
        while len(self._state) > 1:
            self._close_pending()
        if len(self._resources_pending_boxes):
            self._html += self._resources_pending_boxes
            self._resources_pending_boxes = []

        if footnotes:
            self._html.append(
                self.frmt_footnote_cnt.format(
                    **{
                        'TEXT':''.join(
                            [
                                self.frmt_footnote_item.format(
                                    **{
                                        'TEXT' :fn[1],
                                        'INDEX':fn[0]
                                    }
                                )
                                for fn in self.footnotes
                            ]
                        )
                    }
                )
            )
            self.footnotes = []

        if bibliography:
            bib_ids = [
                k for k in self.resources_cited if (
                    self.resources[k]['TYPE'] in self.frmt_bibliography_item
                    and k not in self._resources_bib_flushed
                )
            ]
            if len(bib_ids):
                sorted_bib_ids = sorted(
                    bib_ids, 
                    key=lambda k: self.resources_cited[k]
                )
                html_bib_items = []
                for bib_id in sorted_bib_ids:
                    html_bib_items.append(
                        self.frmt_bibliography_item[
                            self.resources[bib_id]['TYPE']
                        ].format(
                            **{
                                'ID'   :bib_id,
                                'INDEX':self.resources_cited[bib_id],
                            },
                            **self.resources[bib_id]
                        )
                    )
                self._html.append(
                    self.frmt_bibliography_cnt.format(
                        **{
                            'TEXT':''.join(html_bib_items)
                        }
                    )
                )
                self._resources_bib_flushed.update(bib_ids)

    def reset(self, html=False, footnotes=False, bibliography=False):
        if html:
            self._state = [S_START]
            self._html = []
        if footnotes:
            self._footnotes_last_index= 0
            self.footnotes = []
        if bibliography:
            self._resources_last_index = {}
            self._resources_pending_boxes = []
            self._resources_bib_flushed = set()
            self.resources_cited = {}

    def get_html(self):
        """Get the HTML representation of parsed texts.
        """
        html = ''.join(self._html)
        self._html = []
        return html

    def _parse_resource(self, m):
        res_id = m.group(1)
        if res_id in self.resources:
            res_type = self.resources[res_id]['TYPE']

            # find resource's index
            if res_id in self.resources_cited:
                res_index = self.resources_cited[res_id]
            else:
                if res_type in self._resources_last_index:
                    self._resources_last_index[res_type] += 1
                else:
                    self._resources_last_index[res_type] = 1
                res_index = self._resources_last_index[res_type]

            # inline resource expansion
            if res_type in self.frmt_cite_inline:
                res_html = self.frmt_cite_inline[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
            else:
                res_html = '[{}]'.format(res_id)

            # in-box resource expansion
            if (
                res_id not in self.resources_cited
                and res_type in self.frmt_cite_box
            ):
                res_html_box = self.frmt_cite_box[res_type].format(
                    **self.resources[res_id],
                    **{'ID':res_id, 'INDEX':res_index}
                )
                self._resources_pending_boxes.append(res_html_box)

            self.resources_cited[res_id] = res_index

        return res_html

    def _parse_sentence(self, sentence):
        # parse emphasized texts
        sentence = self._re_emph.sub(
            self.frmt_emph.format(**{'TEXT':r'\g<1>'}),
            sentence
        )

        # parse cited resources
        sentence = self._re_cite.sub(
            self._parse_resource,
            sentence
        )

        return sentence

    def _parse_list(self, text):
        prev_endo = 0
        for item in self._re_list_items.finditer(text):
            start, endo = item.span()
            pending_text = text[prev_endo:start].strip()
            if len(pending_text):
                self._html.append(' ' + pending_text.strip())
            item_level = len(item.group(1))
            item_text = item.group(3)
            if item.group(2) == '+':
                item_ordered = True
            elif item.group(2) == '*':
                item_ordered = False 
            while True:
                prev_item_level, prev_item_ordered = self._list[-1]
                if self._list_need_item_suffix:
                    self._html.append(
                        self.frmt_list_item_suffix.format(
                            **{'LEVEL':' '*prev_item_level}
                        )
                    )
                if item_level == prev_item_level:
                    self._html.append(
                        self.frmt_list_item_prefix.format(
                            **{'LEVEL':' '*item_level}
                        )
                    )
                    self._html.append(item_text)
                    self._list_need_item_suffix = True
                    break
                elif item_level > prev_item_level:
                    self._list.append([item_level, item_ordered])
                    if item_ordered:
                        self._html.append(
                            self.frmt_olist_prefix.format(
                                **{'LEVEL':' '*item_level}
                            )
                        )
                    else:
                        self._html.append(
                            self.frmt_ulist_prefix.format(
                                **{'LEVEL':' '*item_level}
                            )
                        )
                    self._html.append(
                        self.frmt_list_item_prefix.format(
                            **{'LEVEL':' '*item_level}
                        )
                    )
                    self._html.append(item_text)
                    self._list_need_item_suffix = True
                    break
                else:
                    del self._list[-1]
                    pprev_item_level, pprev_item_ordered = self._list[-1]
                    if item_level > pprev_item_level:
                        item_level = pprev_item_level
                    if prev_item_ordered:
                        self._html.append(
                            self.frmt_olist_suffix.format(
                                **{'LEVEL':' '*prev_item_level}
                            )
                        )
                    else:
                        self._html.append(
                            self.frmt_ulist_suffix.format(
                                **{'LEVEL':' '*prev_item_level}
                            )
                        )
                    self._list_need_item_suffix = False
            prev_endo = endo

    def _parse_unit(self, text):
        # resume heading text insertion
        if self._state[-1] == S_HEADING_IN:
            self._html.append(self._parse_sentence(text))

        # resume paragraph text insertion
        elif self._state[-1] == S_PARAGRAPH_IN:
            self._html.append(self._parse_sentence(text))

        # resume list text insertion
        elif self._state[-1] == S_LIST_IN:
            self._parse_list(self._parse_sentence(text))

        # add footnote
        elif self._state[-1] == S_FOOTNOTE:
            # add formatted footnote index
            self._footnotes_last_index += 1
            self._html.append(
                self.frmt_footnote_ss.format(
                    **{
                        'INDEX':self._footnotes_last_index,
                        'TEXT' :text,
                    }
                )
            )

            # format the footnote text into a temporary list
            footnote_text_temp = []
            prev_endo = 0
            for m in self._re_ignore.finditer(text):
                start, endo = m.span()
                matched         = [i for i in m.groups() if i is not None]
                ignr_open       = matched[0]
                ignr_text       = matched[1]
                ignr_close      = matched[2]
                footnote_text_temp.append(
                    self._parse_sentence(text[prev_endo:start])
                )
                if ignr_open in self.ignore_unescape:
                    ignr_text   = self._re_ignore_unescs[ignr_open].sub(
                        r'\1',
                        ignr_text
                    )
                if ignr_open in self.frmt_ignore:
                    ignr_text = self.frmt_ignore[ignr_open].format(
                        **{
                            'OPEN'  : ignr_open,
                            'TEXT'  : ignr_text,
                            'CLOSE' : ignr_close,
                        }
                    )
                footnote_text_temp.append(ignr_text)
                prev_endo = endo
            footnote_text_temp.append(
                self._parse_sentence(text[prev_endo:])
            )

            # finalize temporary list into a more usable list
            self.footnotes.append(
                (
                    self._footnotes_last_index,
                    ''.join(footnote_text_temp)
                )
            )

            del self._state[-1]

        elif self._state[-1] == S_START:
            # format basic stuff
            text = self._parse_sentence(text)

            # add new heading
            m = self._re_heading.match(text)
            if m:
                self._heading_level = len(m.group(1)) + self.heading_offset
                heading = m.group(2)
                self._html.append(
                    self.frmt_heading_prefix.format(
                        **{'LEVEL':self._heading_level}
                    )
                )
                self._html.append(heading)
                self._state.append(S_HEADING_IN)

            else:
                # add new list
                m = self._re_list.match(text)
                if m:
                    self._parse_list(text)
                    self._state.append(S_LIST_IN)

                # add new paragraph
                else:
                    self._html.append(self.frmt_paragraph_prefix)
                    self._html.append(text)
                    self._state.append(S_PARAGRAPH_IN)

    def _close_pending(self):
        state = self._state.pop()
        if state == S_HEADING_IN:
            self._html.append(
                self.frmt_heading_suffix.format(
                    **{'LEVEL':self._heading_level}
                )
            )
        elif state == S_PARAGRAPH_IN:
            self._html.append(self.frmt_paragraph_suffix)
        elif state == S_LIST_IN:
            if self._list_need_item_suffix:
                self._html.append(self.frmt_list_item_suffix)
            while len(self._list) > 1:
                item_level, item_ordered = self._list[-1]
                if item_ordered:
                    self._html.append(
                        self.frmt_olist_suffix.format(
                            **{'LEVEL':' '*item_level}
                        )
                    )
                else:
                    self._html.append(
                        self.frmt_ulist_suffix.format(
                            **{'LEVEL':' '*item_level}
                        )
                    )
                del self._list[-1]
            self._list_need_item_suffix = False

    def _parse_units(self, text):
        prev_endo = 0
        for match_unit_border in self._re_unit_sep.finditer(text):
            start, endo = match_unit_border.span()
            self._parse_unit(text[prev_endo:start])
            self._close_pending()
            self.flush(footnotes=False, bibliography=False)
            prev_endo = endo
        self._parse_unit(text[prev_endo:])
