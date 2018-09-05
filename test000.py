import cavemark

parser = cavemark.CaveMark()
parser.resources = {
    'mylink' : {
        'TYPE'  : 'url',
        'url'   : 'https://cave.mn',
    },
    'myimage' : {
        'TYPE'      : 'image',
        'url'       : 'https://cave.mn/pics/coffee.png',
        'caption'   : 'this is a nice coffee mug',
        'alt'       : 'mug'
    },
}

s = '''
# this is some main title

## this is some 2nd level title.

look [myimage] is pretty.  no?  also this link [mylink] is also niceee.  agree
right^[nice footnote ;)].  also `this is some code`.

```
this is some code block
```

this is just some innocent paragraphs. this is just some innocent paragraphs.
this is just some innocent paragraphs. this is just some innocent paragraphs.
this is just some innocent paragraphs.
'''

parser.parse(s)
parser.flush()
html = parser.get_html()
print(html)
