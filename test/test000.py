import cavemark

s = '''
link        : mylink
url         : https://cave.mn
text        : caveman's theories

image       : myimage 
url         : https://cave.mn/pics/caveman.png
caption     : this is _the_ caveman!
alt         : mug

book        : mybook
authors     : Dude McDude and Guy McGuy
title       : the best title ever(tm)
publisher   : cave press
year        : 2018

book        : hisbook
authors     : guy1, guy2 and guy3
title       : the 2nd best title ever
publisher   : some press
year        : 100 BC

book        : lolbook
authors     : Xxxx and Yyyy
title       : the 2nd best title ever
publisher   : some press
year        : 0 BC

footnote    : badass
text        : main title as in badass. hth.

# this is some "main''[badass] title

footnote    : 2ndtitlefn
text        : 2nd level title also badass

## this is some ~~1st~~ 2nd level[2ndtitlefn] title(tm)(R)(c)...

###### H6 heading (with offset should be H7 -- will cavemark make it H6?)

####### H7 heading (with offset should be H8 -- will cavemark make it H6?)

    + this.
        + is.
      * some.

      asdfddf
      adfdfsdf
      asdf.

      adfdfasf
      asdfadf
      asdfds.

      + some.
      * some _lol_[badass].
    * list `#include <stdio.h>`.
  * some
```#include <stdio.h>
int main(){
    return 0;
}```.
  * some.
    * some.
        + some.
            + some.
             + some.

footnote:stupid
text    :lol wat?? foot note in caption? OMG!


* this is some nested list
* this is some nested list
    * this is some nested list
    * this is some nested list
    * this is some nested list
        * this is some nested list
        * this is some nested list
        * this is some nested list
            * this is some nested list
            * this is some nested list
            * this is some nested list
            * this is some nested list
    * this is _some `with code` nested_ list
    * this is some nested list

* this is a liset with paragraphs in it.

  2nd paragraph in 1st list.

* 2nd item in same list

image  : newimage
url    : https://cave.mn/pics/cat.png
caption: a _cApTiOn_[stupid]
alt    :  some alt text

footnote:code1
text    :nice footnote with `print(x);` ;)

look [myimage] is pretty.  no?  how about [newimage]? i just added it myself!
also _this link [mylink] is also niceee_.  agree right[code1].  also `this [not resource] is some code`.  this resource is
errornous [lolimadethisup].

this is a citation with an empty resource identifier [  ].

```# this is some code block
for i in range(0, 100):
    print('lol')
    # hell yeah!
#include <stdio.h>
int main() {
    printf("lol\\n");
    return 0;
}
```

look [myimage] is pretty.  no?  also this link [mylink] is also niceee.  agree
right[code1].  also `this^{not footnote} is some
code`.

footnote:stupid2
text    :yep :) [mybook]]

this is just some innocent paragraphs[stupid2]. this is just some
innocent paragraphs.  this is just some innocent paragraphs. this is just some
innocent paragraphs.  here [mybook] and [mybook] this is just some innocent
paragraphs.

footnote:stupid3
text    :
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

this is some badass footnote[stupid3]

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
)
parser.parse(s + '  and this [lolbook].')
parser.flush(bibliography=False)

parser.forget_cited(resource_type='footnote')
parser.parse(s + '  and this [hisbook].')
parser.flush()

html = parser.get_html()

with open('test000.html', 'w') as f:
    f.write(html)
