# Test

## Revision 0

I ran this:

```python
from collections import deque as d
from itertools import count as c
a = d()
n = c(2)
print('Thinking...')
for _ in range(500_000):
    for i in n:
        if 0 not in (i % j for j in a):
            a.append(i)
            break
print('Writing...')
align = lambda s: str(s).rjust(6, ' ')
with open('primes.txt', 'w', encoding = 'UTF8') as f:
    f.writelines('{}, {};\n'.format(*map(align, iv)) for iv in enumerate(a))
print('Done.')
```

The next version [CPU/RAM Speed Test via Prime Number - Pastebin.com](https://pastebin.com/VQmLgGX3) times it.

---

What's next:

1. Multiple cores?

2. Asynchronous deques?

3. *Formatting*

4. **Better names**!

---

## Revision 1

Here's verion 1 updated:

<div>
<html>
<head>
<title>primestest0.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #cc7832;}
.s1 { color: #a9b7c6;}
.s2 { color: #cc7828;}
.s3 { color: #6897bb;}
.s4 { color: #a2c261;}
.s5 { color: #038cff;}
.ln { color: #606366; font-weight: normal; font-style: normal; }
</style>
</head>
<body bgcolor="#2b2b2b">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
primestest0.py</font>
</center></td></tr></table>
<pre><a name="l1"><span class="ln">1    </span></a><span class="s0">from </span><span class="s1">collections </span><span class="s0">import </span><span class="s1">deque</span>
<a name="l2"><span class="ln">2    </span></a><span class="s0">from </span><span class="s1">itertools </span><span class="s0">import </span><span class="s1">count</span>
<a name="l3"><span class="ln">3    </span></a>
<a name="l4"><span class="ln">4    </span></a><span class="s1">array </span><span class="s2">= </span><span class="s1">deque</span><span class="s0">()</span>
<a name="l5"><span class="ln">5    </span></a><span class="s1">integers </span><span class="s2">= </span><span class="s1">count</span><span class="s0">(</span><span class="s3">2</span><span class="s0">)</span>
<a name="l6"><span class="ln">6    </span></a><span class="s1">print</span><span class="s0">(</span><span class="s4">'Thinking...'</span><span class="s0">)</span>
<a name="l7"><span class="ln">7    </span></a><span class="s0">for </span><span class="s1">_ </span><span class="s0">in </span><span class="s1">range</span><span class="s0">(</span><span class="s3">500_000</span><span class="s0">)</span><span class="s2">:</span>
<a name="l8"><span class="ln">8    </span></a>    <span class="s0">for </span><span class="s1">i </span><span class="s0">in </span><span class="s1">integers</span><span class="s2">:</span>
<a name="l9"><span class="ln">9    </span></a>        <span class="s0">if </span><span class="s3">0 </span><span class="s0">not in (</span><span class="s1">i </span><span class="s2">% </span><span class="s1">j </span><span class="s0">for </span><span class="s1">j </span><span class="s0">in </span><span class="s1">array</span><span class="s0">)</span><span class="s2">:</span>
<a name="l10"><span class="ln">10   </span></a>            <span class="s1">array</span><span class="s5">.</span><span class="s1">append</span><span class="s0">(</span><span class="s1">i</span><span class="s0">)</span>
<a name="l11"><span class="ln">11   </span></a>            <span class="s0">break</span>
<a name="l12"><span class="ln">12   </span></a><span class="s1">print</span><span class="s0">(</span><span class="s4">'Writing...'</span><span class="s0">)</span>
<a name="l13"><span class="ln">13   </span></a><span class="s1">align </span><span class="s2">= </span><span class="s0">lambda </span><span class="s1">s</span><span class="s2">: </span><span class="s1">str</span><span class="s0">(</span><span class="s1">s</span><span class="s0">)</span><span class="s5">.</span><span class="s1">rjust</span><span class="s0">(</span><span class="s3">6</span><span class="s0">, </span><span class="s4">' '</span><span class="s0">)</span>
<a name="l14"><span class="ln">14   </span></a><span class="s0">with </span><span class="s1">open</span><span class="s0">(</span><span class="s4">'primes.txt'</span><span class="s0">, </span><span class="s4">'w'</span><span class="s0">, </span><span class="s1">encoding </span><span class="s2">= </span><span class="s4">'UTF8'</span><span class="s0">) as </span><span class="s1">f</span><span class="s2">:</span>
<a name="l15"><span class="ln">15   </span></a>    <span class="s1">f</span><span class="s5">.</span><span class="s1">writelines</span><span class="s0">(</span><span class="s4">'{}, {};</span><span class="s0">\n</span><span class="s4">'</span><span class="s5">.</span><span class="s1">format</span><span class="s0">(</span><span class="s2">*</span><span class="s1">map</span><span class="s0">(</span><span class="s1">align</span><span class="s0">, </span><span class="s1">iv</span><span class="s0">)) for </span><span class="s1">iv </span><span class="s0">in </span><span class="s1">enumerate</span><span class="s0">(</span><span class="s1">array</span><span class="s0">))</span>
<a name="l16"><span class="ln">16   </span></a><span class="s1">print</span><span class="s0">(</span><span class="s4">'Done.'</span><span class="s0">)</span>
<a name="l17"><span class="ln">17   </span></a></pre>
</body>
</html>
</div>

Here's revison 1, straign 2:

<html>
<head>
<title>primestest.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #808080;}
.s1 { color: #a9b7c6;}
.s2 { color: #cc7832;}
.s3 { color: #cc7828;}
.s4 { color: #6897bb;}
.s5 { color: #038cff;}
.ln { color: #606366; font-weight: normal; font-style: normal; }
</style>
</head>
<body bgcolor="#2b2b2b">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
primestest.py</font>
</center></td></tr></table>
<pre><a name="l1"><span class="ln">1    </span></a><span class="s0">#!/usr/bin/python3.8</span>
<a name="l2"><span class="ln">2    </span></a><span class="s2">from </span><span class="s1">collections </span><span class="s2">import </span><span class="s1">deque</span>
<a name="l3"><span class="ln">3    </span></a><span class="s2">from </span><span class="s1">timeit </span><span class="s2">import </span><span class="s1">timeit </span><span class="s2">as </span><span class="s1">t</span>
<a name="l4"><span class="ln">4    </span></a>
<a name="l5"><span class="ln">5    </span></a><span class="s1">TESTS </span><span class="s3">= </span><span class="s4">8</span>
<a name="l6"><span class="ln">6    </span></a><span class="s1">ps </span><span class="s3">= </span><span class="s1">deque</span><span class="s2">()</span>
<a name="l7"><span class="ln">7    </span></a><span class="s1">ts </span><span class="s3">= </span><span class="s2">[</span><span class="s4">0</span><span class="s2">] </span><span class="s3">* </span><span class="s1">TESTS</span>
<a name="l8"><span class="ln">8    </span></a>
<a name="l9"><span class="ln">9    </span></a>
<a name="l10"><span class="ln">10   </span></a><span class="s2">def </span><span class="s1">do</span><span class="s2">()</span><span class="s3">:</span>
<a name="l11"><span class="ln">11   </span></a>    <span class="s1">found </span><span class="s3">= </span><span class="s4">0</span>
<a name="l12"><span class="ln">12   </span></a>    <span class="s1">last </span><span class="s3">= </span><span class="s4">1</span>
<a name="l13"><span class="ln">13   </span></a>    <span class="s2">while </span><span class="s1">found </span><span class="s3">&lt; </span><span class="s4">1_000_000</span><span class="s3">:</span>
<a name="l14"><span class="ln">14   </span></a>        <span class="s1">last </span><span class="s3">+= </span><span class="s4">1</span>
<a name="l15"><span class="ln">15   </span></a>        <span class="s2">if not </span><span class="s1">any</span><span class="s2">(</span><span class="s1">last </span><span class="s3">% </span><span class="s1">x </span><span class="s3">== </span><span class="s4">0 </span><span class="s2">for </span><span class="s1">x </span><span class="s2">in </span><span class="s1">ps</span><span class="s2">)</span><span class="s3">:</span>
<a name="l16"><span class="ln">16   </span></a>            <span class="s1">ps</span><span class="s5">.</span><span class="s1">append</span><span class="s2">(</span><span class="s1">last</span><span class="s2">)</span>
<a name="l17"><span class="ln">17   </span></a>            <span class="s1">found </span><span class="s3">+= </span><span class="s4">1</span>
<a name="l18"><span class="ln">18   </span></a>
<a name="l19"><span class="ln">19   </span></a>
<a name="l20"><span class="ln">20   </span></a><span class="s2">for </span><span class="s1">n </span><span class="s2">in </span><span class="s1">range</span><span class="s2">(</span><span class="s1">TESTS</span><span class="s2">)</span><span class="s3">:</span>
<a name="l21"><span class="ln">21   </span></a>    <span class="s1">ps</span><span class="s5">.</span><span class="s1">clear</span><span class="s2">()</span>
<a name="l22"><span class="ln">22   </span></a>    <span class="s1">print</span><span class="s2">(</span><span class="s1">n</span><span class="s2">)</span>
<a name="l23"><span class="ln">23   </span></a>    <span class="s1">ts</span><span class="s2">[</span><span class="s1">n</span><span class="s2">] </span><span class="s3">= </span><span class="s1">t</span><span class="s2">(</span><span class="s1">do</span><span class="s2">)</span>
<a name="l24"><span class="ln">24   </span></a>
<a name="l25"><span class="ln">25   </span></a><span class="s1">print</span><span class="s2">(</span><span class="s1">ts</span><span class="s2">)</span>
<a name="l26"><span class="ln">26   </span></a></pre>
</body>
</html>

# Conclusion

Awesome!  This markdown document was made by [Mark Text](https://marktext.app/) on [Fedora](https://getfedora.org/).
