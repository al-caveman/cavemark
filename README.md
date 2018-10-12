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
beautifully formatted page:

![rendered output](https://raw.githubusercontent.com/Al-Caveman/cavemark/master/demo.png)


# Benchmark

Speed is certainly not the main reason I made CaveMark, but I think the speed
benchmark is a nice way to show you how honestly I made CaveMark.  E.g. I
wasn't a lazy sucker that just hoped hardware to become faster.

Before CaveMark was born, [mistune](https://github.com/lepture/mistune) used to
be the fastest pure-Python markdown parser.  So I am comparing against mistune
in this benchmark.  I tested against other pure-Python markdown parsers, and
they were too slow, so I am not even bothering with the others.

Results with CPython (repeated 3 times):

```
mistune : 13.928859449 seconds
cavemark: 5.57010197 seconds (2.5 times faster!)

mistune : 13.980875624 seconds
cavemark: 5.646393874 seconds (2.5 times faster!)

mistune : 13.941337609 seconds
cavemark: 5.608549864 seconds (2.5 times faster!)
```

Results with PyPy3 (repeated 3 times):

```
mistune : 10.141159687 seconds
cavemark: 1.728199896 seconds (5.9 times faster!)

mistune : 9.768847644000001 seconds
cavemark: 1.7137211739999998 seconds (5.7 times faster!)

mistune : 9.077121615 seconds
cavemark: 1.703783539 seconds (5.3 times faster!)
```

# Syntax

`#` defines section headings.  E.g. `# heading` becomes `<h1>heading</h1>`, `##
heading` becomes `<h2>heading</h2>`.

`_` emphasizes texts.  E.g.  `_this_` = _this_.

Ordered lists are defined by `+`, and the unordered by `*`.  E.g.:

```
* this item is not orderd.
* another unordered item.
    + this item is nested and is ordered.
    + another ordered item.
```

The most interesting part of CaveMark is how it defines _resources_.  Below is
an example where a figure is defined.  This figure can then be cited later in
the document (as shown later in this section).

```
image  : myimage
url    : http://cave.mn/pics/cat.png
caption: caveman's cat looks happy
alt    : caveman's cat
```

Aside from `image`, many other resource types are defined, e.g. book, footnote,
quote, theorem, etc.  You can also easily add your own custom ones.

Citing a resource is by using `[]`.  E.g. `[myimage]` will cite the `myimage`
resource we defined earlier.

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

# This is a _heading_

[myimage] shows a happy cat[mynote].

* A nice list.
* With items in it.
    + Can be nested.

    With, possibly, multiple paragraphs in it!

    Yep, another paragraph, with citations [mybook].

    + Another ordered item.

A paragraph could have `inline code like this`, or:

```#include <stdio.h>
int main(){
    printf("a code block like this!\\n");
    return 0;
}```
'''

parser = cavemark.CaveMark()
parser.parse(text_input)
parser.flush()
html_output = parser.get_html()

with open('test.html', 'w') as f:
    f.write(html_output)
```

If you open `test.html` using your browser, you will see something neat:

![rendered output](https://raw.githubusercontent.com/Al-Caveman/cavemark/master/test/test001.png)

# CaveMark's Syntax Philosophy

Every single HTML code that CaveMark generates is configurable via
`self.frmt_*` variables.  There is no hard-coded HTML strings.  E.g. while by
default `# This is a heading` becomes `<h1>This is a heading</h1>`, you are
free to change it to be, say, `lol This is a heading rofl`, or whatever.

Another aspect is that CaveMark tries avoid needless features as much as I
could.  E.g. most markdown parsers have several ways of doing the same thing.
For example a heading could be defined by `# This is a heading` or:

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
to emphasize emphasize texts.  E.g. some markdown implementations offer `*`,
`**`, `_`, `__` to denote that a text is emphasized.  I think this is needless.
CaveMark only offers `_` emphasize texts. E.g. `_this_` becomes `<em>this</em>`
in HTML by default.  You can then style the `em` tags as you want, or
completely replace the `em` tags by whatever you want.

# Todo

  - [ ] Tables.
  - [ ] Strike-trough.
  - [ ] Documentation.

**Note 1:**  I currently don't need these features.  My plan is to wait, until
I happen to need them, then implement them.  You are more than welcome to
submit patches/pull requests.  Alternatively, you can try to motivate me enough
so that I implement them for you.

**Note 2:**  CaveMark will remain faster than
[mistune](https://github.com/lepture/mistune) after adding those features.
Design-wise, nothing in CaveMark's architecture indicates any notable slowdown
when those missing features are added.
