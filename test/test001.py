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
