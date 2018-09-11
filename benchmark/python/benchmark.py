import cavemark
import mistune
import time

common_things = '''
# this is some heading `with some code in it; i guess must be cool?`.. we will see

this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.
this is some long paragraph i guess.  this is some long paragraph i guess.


this is some long paragraph _with some italic texts_ i guess.  this is some
long paragraph i guess.  this is some long paragraph _with some italic texts_ i
guess.  this is some long paragraph i guess.  this is some long paragraph _with
some italic texts_ i guess.  this is some long paragraph i guess.  this is some
long paragraph _with some italic texts_ i guess.  this is some long paragraph i
guess.  this is some long paragraph _with some italic texts_ i guess.  this is
some long paragraph i guess.  this is some long paragraph _with some italic
texts_ i guess.  this is some long paragraph i guess.  this is some long
paragraph _with some italic texts_ i guess.  this is some long paragraph i
guess.  this is some long paragraph _with some italic texts_ i guess.  this is
some long paragraph i guess.  this is some long paragraph _with some italic
texts_ i guess.  this is some long paragraph i guess.  this is some long
paragraph _with some italic texts_ i guess.  this is some long paragraph i
guess.  this is some long paragraph _with some italic texts_ i guess.  this is
some long paragraph i guess.  this is some long paragraph _with some italic
texts_ i guess.


```
# this is some code block
for i in range(0, 100):
    print('lol')
    # hell yeah!
```

another one:
```
    # this code block list mistune's benchmark
    Parsing the Markdown Syntax document 1000 times...
    Mistune: 12.9425s
    Misaka: 0.537176s
    Markdown: 47.7091s
    Markdown2: 80.5163s
    cMarkdown: 0.680664s
    Discount is not available
    
    Parsing the Markdown Syntax document 1000 times...
    Mistune: 12.7255s
    Misaka: 0.553476s
    Markdown: 47.9369s
    Markdown2: 79.5075s
    cMarkdown: 0.71733s
    Discount is not available
```

### done.

let's hope all is good.  how fast is _CaveMark_?  one way to find out :)
'''


# cavemark output
cm_parser = cavemark.CaveMark(heading_offset=0)
cm_parser.parse(common_things)
cm_parser.flush(pending=True, footnotes=False, bibliography=False)
cm_html = cm_parser.get_html()
cm_parser.reset(html=True, footnotes=True, bibliography=True)
with open('output_cavemark.html', 'w') as f:
    f.write(cm_html)

# mistune output
mt_renderer = mistune.Renderer(escape=True)
mt_parser = mistune.Markdown(renderer=mt_renderer)
mt_parser(common_things)
mt_html = mt_parser(common_things)
with open('output_mistune.html', 'w') as f:
    f.write(mt_html)

# benchmarking cavemark 
n = 10000
cm_start = time.process_time()
for i in range(0, n):
    cm_parser.parse(common_things)
    cm_parser.flush(pending=True, footnotes=False, bibliography=False)
    cm_html = cm_parser.get_html()
    cm_parser.reset(html=True, footnotes=True, bibliography=True)
cm_end = time.process_time()

# benchmarking mistune
mt_start = time.process_time()
for i in range(0, n):
    mt_html = mt_parser(common_things)
mt_end = time.process_time()

print('cavemark     : {} seconds'.format(cm_end-cm_start))
print('mistune      : {} seconds'.format(mt_end-mt_start))
print('difference   : {} seconds'.format((cm_end-cm_start)-(mt_end-mt_start)))
