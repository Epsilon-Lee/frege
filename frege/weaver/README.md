## weaver

`weaver` is a library that is named after the machine translation pioneer [Warren Weaver](https://en.wikipedia.org/wiki/Machine_translation). The initial functionalities of this library are:

- Corpus statistics: total token number, total token type, sentence pair number;

- Google translate api: use [googletrans](https://py-googletrans.readthedocs.io/en/latest/) to do translation:
```python
from googletrans import Translator
translator = Translator()
t = translator.translate("我特别喜欢弗雷格，以及由他带来的数理逻辑与分析哲学变革。", src='zh-CN', dest='en')
>>> print(t.text)
# 'I especially like Frege, and the mathematical logic and analytic philosophy that he brought.'
t_sub = translator.translate("分析哲学变革")
>>> print(t.text)
# 'Analytical philosophy change'
```
- BLEU analyses: a) given prediction text file and reference text file, compute sentence level BLEU; b ) given two different prediction text files corresponds to the same reference text file, analyze the differences in predicted hypothesis which result in various BLEU scores. 

- Post edit analyses: a) use the tool [terp](https://github.com/snover/terp) to annotate the edit operations from prediction to reference.

- Quality estimation: TODO.
