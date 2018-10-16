# Overview

CaveMark is a typesetting markdown parser.  It is also the fastest pure-Python
markdown parser!  

If you don't know what's a typesetting parser read [this
](https://en.wikipedia.org/wiki/Typesetting).  I don't know any typesetting
markdown parser for Python.  So maybe CaveMark is the only one.  I know about
[Madoko](https://www.madoko.net/), but its syntax sucks and I guess it's not a
Python module (JavaScript).  I never used Madoko.

This typesetting aspect makes CaveMark the easiest way to allow you write
pretty documents for your blog/website/whatever, than, say, mistune or any
other conventional markdown parser around.

E.g. by simply typing `[myimage] shows a happy cat[mynote].` (assuming
resources `myimage` and `mynote` are defined) you will conveniently get this
beautifully formatted page, where figures, captions, footnotes, links, etc are
all done automatically:

![rendered output](https://github.com/Al-Caveman/cavemark/blob/master/demo.png)


Every single HTML code that CaveMark generates is configurable via
`self.frmt_*` variables.  There is no hard-coded HTML strings.  E.g. while by
default `# This is a heading` becomes `<h1>This is a heading</h1>`, you are
free to change it to be, say, `lol This is a heading rofl`, or whatever.

For a production demonstration of what CaveMark can do, checkout [this
website](https://cave.mn); all its articles are written in CaveMark!

# Features

* Headings with automatic indices.
* Paragraphs.
* Emphasized texts.
* Strikethrough texts.
* Lists.
* Shortcuts.
* Inline/block codes.
* Inline/box resources (e.g. books, links, figures, quotes, theorems,
  definitions, etc).
* Footnotes.
* Bibliographies.
* Simple, user-friendly, syntax (I think simplest among all typesetting
  parsers).
* Fastest in class.
* Supports CPython2, Cpython3, PyPy2, PyPy3.
* Made with beard.

# Benchmark

Speed is not the main selling point, but I think it shows that I didn't take
too sloppy shortcuts while coding it.  I am benchmarking against
[mistune](https://github.com/lepture/mistune) coz it's the fastest in town.
Others were too slow to even bother.

Since [mistune](https://github.com/lepture/mistune) and CaveMark have different
syntax, this benchmark only tests things where they agree on their syntax.
Even though, I think, CaveMark still does more.  E.g. headings in CaveMark automatically also produce section identifiers.  E.g:

```md
# Heading

## Subheading

# Another heading
```

gives in [mistune](https://github.com/lepture/mistune) this:

```html
<h1>Heading<h1>

<h2>Subheading<h2>

<h1>Another heading<h1>
```

But this in CaveMark (removed links for brevity):

```html
<h1>1. Heading<h1>

<h2>1.1. Subheading<h2>

<h1>2. Another heading<h1>
```


Results with CPython3 (repeated 3 times):

```
mistune : 18.177862088 seconds
cavemark: 9.386662586 seconds (1.9 times faster!)

mistune : 18.733004819999998 seconds
cavemark: 9.601156947 seconds (2.0 times faster!)

mistune : 18.762310276999997 seconds
cavemark: 9.647228555 seconds (1.9 times faster!)
```

Results with CPython2 (repeated 3 times):

```
mistune : 19.7261228561 seconds
cavemark: 9.48487520218 seconds (2.1 times faster!)

mistune : 19.4376080036 seconds
cavemark: 9.53958702087 seconds (2.0 times faster!)

mistune : 20.3399410248 seconds
cavemark: 9.61795091629 seconds (2.1 times faster!)
```

Results with PyPy3 (repeated 3 times):

```
mistune : 12.311563448000001 seconds
cavemark: 3.1916073270000003 seconds (3.9 times faster!)

mistune : 12.470256598999999 seconds
cavemark: 3.376128782 seconds (3.7 times faster!)

mistune : 13.637612451999999 seconds
cavemark: 3.126377384 seconds (4.4 times faster!)
```

Results with PyPy2 (repeated 3 times):

```
mistune : 8.99331712723 seconds
cavemark: 1.47040700912 seconds (6.1 times faster!)

mistune : 9.01434993744 seconds
cavemark: 1.45837283134 seconds (6.2 times faster!)

mistune : 9.00144791603 seconds
cavemark: 1.47606897354 seconds (6.1 times faster!)
```

You can find the full benchmark code in the
[benchmark](https://github.com/Al-Caveman/cavemark/tree/master/benchmark)
directory.

In the future, I may do another benchmark where I test all the overlapping
features, even when the syntax is not identical accross CaveMark and
[mistune](https://github.com/lepture/mistune).  I plan to create two separate
texts, both rendering exactly the same desired HTML document, but one in
CaveMark's superior typesetting syntax, and another in
[mistune](https://github.com/lepture/mistune)'s.

# Syntax

`#` defines section headings.  E.g. `# heading` becomes `<h1>heading</h1>`, `##
heading` becomes `<h2>heading</h2>`.

`_` emphasizes texts.  E.g.  `_this_` = _this_. `~~` to strike through text.
E.g. `~~this~~` = ~~this~~.

Ordered lists are defined by `+`, and the unordered by `*`.  E.g.:

```
* this item is not orderd.
* another unordered item.
    + this item is nested and is ordered.
    + another ordered item.
```

The most interesting part of CaveMark is how it defines _resources_, and uses
them to achieve typesetting.  Below is an example where a figure is defined.
This figure can then be cited later in the document (as shown later in this
section).

```
image  : myimage
url    : http://cave.mn/pics/cat.png
caption: caveman's cat looks happy
alt    : caveman's cat
```

Aside from `image`, many other resource types are defined, e.g. book, footnote,
quote, theorem, etc.  You can also easily add your own custom ones.

Citing a resource is by using `[]`.  E.g. `[myimage]` will cite the `myimage`
resource we defined earlier.  When a resource identifier, e.g. `myimage` is
prefixed by `!`, in a citation box, e.g. `[!myimage], then the resource
`myimage` will not expand into its inline citation format. Using `[!myimage]`
is useful when you want to only place the box/bibliography/footnote expansion
of the resource, without actually citing the resource.

CaveMark also supports shortcuts.  By default:

* `(c)`   = `&copy;`.
* `(tm)`  = `&trade;`.
* `(R)`   = `&reg;`.
* `"`     = `&ldquo;` .
* `''`    = `&rdquo;` .
* `--`    = `&mdash;` .
* `...`   = `&hellip;`.

# Basic Example

```python
import cavemark

text_input = '''
image  : myimage
url    : http://cave.mn/pics/cat.png
caption: Caveman's cat.
alt    : Caveman's cat.

book     : mybook
title    : The Book
authors  : Dude McDudeface
publisher: CavePress
year     : 2018

footnote: mynote
text    : She is 1 years old.

quotation: myquote
text     : Beardless men are entry-level trannis
author   : Dude McDudeface, 2018

# This is a _heading_

[myimage] shows a happy cat[mynote].

* A nice list.
* With items in it.
    + Can be nested.

    With, possibly, multiple paragraphs in it!

    Yep, another paragraph, with citations [mybook].

    + Another ordered item, but this one with ~~some struck-through text~~.

A paragraph could have `inline code like this`, or:

```#include <stdio.h>
int main(){
    printf("a code block like this!\\n");
    return 0;
}```

How about citing [myquote]?
'''

parser = cavemark.CaveMark()
parser.parse(text_input)
parser.flush()
html_output = parser.get_html()

with open('test001.html', 'w') as f:
    f.write(html_output)
```

If you open `test.html` using your browser, you will see something neat:

![rendered output](https://raw.githubusercontent.com/Al-Caveman/cavemark/master/test/test001.png)

# CaveMark's Syntax Philosophy

I tried to avoid needless formatting features in CaveMark.  E.g. most markdown
parsers have several ways of doing the same thing.  For example a heading could
be defined by `# This is a heading` or:

```
This is a heading
-----------------
```

The `#` method is superior, since it allows you to also specify heading's level
by repeating `#`.  E.g. `###### This is a heading` defines a level 6 heading.

Therefore, CaveMark only supports the `#` method, and not the under-dashed one.
I don't see a good reason to do it.  Specially that text editors, such as
`vim`, highlight headings texts accordingly either way.

Another example of avoiding needless features is that there is only one way to
define emphasized texts.  I don't see any reason to allow to offer several ways
to emphasize texts.  E.g. some markdown implementations offer `*`, `**`, `_`,
`__` to denote that a text is emphasized.  I think this is needless.  CaveMark
only offers `_` emphasize texts. E.g. `_this_` becomes `<em>this</em>` in HTML
by default.  You can then style the `em` tags as you want, or completely
replace the `em` tags by whatever you want.

I basically think that emphasization of texts is a semantic unit, and it is of
one type.  I see no case where it is good to emphasize texts by underlines in
some paragraph, and then emphasize by bold in another paragraph.  To me this
makes no sense.  IMO, if you wish to denote that a text is emphasized, then
stick to the standard format for such a thing.  In other words, varying the
emphasization format across your paragraphs is like changing the font and color
used in your section headings.

If you can convince me that more features are needed, I will change my mind.
But so far I have not seen any reason to justify having multiple ways of
defining section headings or emphasized texts.

# Todo

  - [ ] Tables.
  - [ ] Documentation.

**Note 1:**  I currently don't need these features.  My plan is to wait, until
I happen to need them, then implement them.  You are more than welcome to
submit patches/pull requests.  Alternatively, you can try to motivate me enough
so that I implement them for you.
