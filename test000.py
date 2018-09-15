import cavemark

s = '''
# this is some main^{main title as in badass.  hth.} title

## this is some 2nd level^{2nd level title also badass} title.

look [myimage] is pretty.  no?  also this link [mylink] is also niceee.  agree
right^{nice footnote with `print(x);` ;)}.  also `this^{not footnote} is some
code`.

```# this is some code block
for i in range(0, 100):
    print('lol')
    # hell yeah!
```

* some `UNORDERED` list.
* bas_ic ya?
* ye_p.
    * hmm more?^{nice aye} i know.
      * moorrre? ```code block``` yep.
      * no let's wait a bit here..
        + moore numbered?
        + no let's wait a bit here..
      * let's go back.
     * kinda bak?
  * more kinda bak?
* fully back.

+ some `ORDERED` list.
+ bas_ic ya?
+ ye_p.
    * hmm more?^{nice aye} i know.
      * moorrre? ```code block``` yep.
      * no let's wait a bit here..
        + moore numbered?
        + no let's wait a bit here..
      * let's go back.
     * kinda bak?
  * more kinda bak?
+ fully back.


this is just some innocent paragraphs^{yep :) [mybook]]}. this is just some
innocent paragraphs.  this is just some innocent paragraphs. this is just some
innocent paragraphs.  here [mybook] and [mybook] this is just some innocent
paragraphs.

this is some badass footnote^{
such a badass footnote with ignored text interval in it, like this \[
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work\}, \[not this\\\\], \(not this\), $$not
this$$, `not this`, ```not this```
\], `this` and even code block: 
```# this is some code block
for i in range(0, 100):
    print('lol')
    # hell yeah!
```
!!
}

\[
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\\\\], \(not this\), $$not
this$$, `not this`, ```not this```.
\]

\(
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\\\\), $$not
this$$, `not this`, ```not this```.
\)

$$
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), \$$not
this\$$, `not this`, ```not this```.
$$

`
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), $$not
this$$, \`not this\`, \`\`\`not this\`\`\`.
`

```
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), $$not
this$$, `not this`, \```not this\```.
```

this is a very long paragraph that contains this code:
\[
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\\\\], \(not this\), $$not
this$$, `not this`, ```not this```.
\]
, this:
\(
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\\\\), $$not
this$$, `not this`, ```not this```.
\)
, this:
$$
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), \$$not
this\$$, `not this`, ```not this```.
$$
, and this:
`
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), $$not
this$$, \`not this\`, \`\`\`not this\`\`\`.
`

```
this is some ignored text.  nothing should work.  no citations [mybook], and no
footnotes^{this footnote must not work}, \[not this\] \(not this\), $$not
this$$, `not this`, \```not this\```.
```
'''


parser = cavemark.CaveMark(
    heading_offset=1,
    resources={
        'mylink' : {
            'TYPE'  : 'url',
            'url'   : 'https://cave.mn',
        },
        'myimage' : {
            'TYPE'      : 'image',
            'url'       : 'https://cave.mn/pics/caveman.png',
            'caption'   : 'this is the caveman!',
            'alt'       : 'mug'
        },
        'mybook' : {
            'TYPE'      : 'book',
            'authors'   : 'Dude McDude and Guy McGuy',
            'title'     : 'the best title ever',
            'publisher' : 'cave press',
            'year'      : '2018',
        },
        'hisbook' : {
            'TYPE'      : 'book',
            'authors'   : 'guy1, guy2 and guy3',
            'title'     : 'the 2nd best title ever',
            'publisher' : 'some press',
            'year'      : '100 BC',
        },
        'lolbook' : {
            'TYPE'      : 'book',
            'authors'   : 'Xxxx and Yyyy',
            'title'     : 'the 2nd best title ever',
            'publisher' : 'some press',
            'year'      : '0 BC',
        },
    }
)
parser.parse(s + '  and this [lolbook].')
parser.flush(bibliography=False)
parser.parse(s + '  and this [hisbook].')
parser.flush()
html = parser.get_html()
#parser.flush()
#parser.reset(resources=True)
with open('test000.html', 'w') as f:
    f.write(html)
