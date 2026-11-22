# Word-list sources

The challenge uses the positive and negative word lists from the Hu and Liu Opinion Lexicon as its happy and sad word datasets. These lists cover favorable and unfavorable sentiment more broadly than literal happiness and sadness.

- Happy words: https://raw.githubusercontent.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/master/data/opinion-lexicon-English/positive-words.txt
- Sad words: https://raw.githubusercontent.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/master/data/opinion-lexicon-English/negative-words.txt
- Original project: https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
- Accessed: 23 November 2026

Citation: Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD-2004), Seattle, Washington, August 22–25, 2004.

Original dataset headers and attribution are preserved in both text files. The program ignores semicolon-prefixed header lines and blank lines. It matches whole words without case sensitivity and counts repeated matching words separately. Negation and context are not interpreted by this simple count-based method.
