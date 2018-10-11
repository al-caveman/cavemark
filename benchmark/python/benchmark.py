import cavemark
import cavemark2
import mistune
import time

basic_things = '''
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

basic_things_with_basic_lists = '''
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

* 2nd item in same list


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

# benchmark stuff
bench_text = basic_things_with_basic_lists
n = 10000

# cavemark output
cm_parser = cavemark.CaveMark(heading_offset=0)
cm_parser.parse(bench_text)
cm_parser.flush(footnotes=False, bibliography=False)
cm_html = cm_parser.get_html()
cm_parser.reset(html=True, footnotes=True, bibliography=True)
with open('output_cavemark.html', 'w') as f:
    f.write(cm_html)

# cavemark2 output
cm2_parser = cavemark.CaveMark(heading_offset=0)
cm2_parser.parse(bench_text)
cm2_parser.flush(footnotes=False, bibliography=False)
cm2_html = cm_parser.get_html()
cm2_parser.reset()
with open('output_cavemark2.html', 'w') as f:
    f.write(cm_html)

# mistune output
mt_renderer = mistune.Renderer(escape=True)
mt_parser = mistune.Markdown(renderer=mt_renderer)
mt_html = mt_parser(bench_text)
with open('output_mistune.html', 'w') as f:
    f.write(mt_html)

# benchmarking cavemark 
cm_start = time.process_time()
for i in range(0, n):
    cm_parser.parse(bench_text)
    cm_parser.flush(footnotes=False, bibliography=False)
    cm_html = cm_parser.get_html()
    cm_parser.reset(html=True, footnotes=True, bibliography=True)
cm_end = time.process_time()

# benchmarking cavemark2
cm2_start = time.process_time()
for i in range(0, n):
    cm2_parser.parse(bench_text)
    cm2_parser.flush(footnotes=False, bibliography=False)
    cm2_html = cm_parser.get_html()
    cm2_parser.reset()
cm2_end = time.process_time()

# benchmarking mistune
mt_start = time.process_time()
for i in range(0, n):
    mt_html = mt_parser(bench_text)
mt_end = time.process_time()

print('cavemark     : {} seconds'.format(cm_end-cm_start))
print('cavemark2    : {} seconds'.format(cm2_end-cm2_start))
print('mistune      : {} seconds'.format(mt_end-mt_start))
print('difference   : {} seconds'.format((cm_end-cm_start)-(mt_end-mt_start)))
print('difference2  : {} seconds'.format((cm2_end-cm2_start)-(mt_end-mt_start)))
