import cavemark

text_input = '''
# this is a _heading_

image  : myimage
url    : http://cave.mn/pics/cat.png
caption: caveman's cat
alt    : caveman's cat

footnote: mynote
text    : the cat is 1 yrs old

[myimage] shows a happy cat[mynote].
'''

parser = cavemark.CaveMark()
parser.parse(text_input)
parser.flush()
html_output = parser.get_html()

with open('test001.html', 'w') as f:
    f.write(html_output)
