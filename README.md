# Search_engine
a search engine index by Inverted index, ranked by BM25, performs work similarity by a pre-trained work2vec model
## Requirements
```shell
pip install python==3.6
pip install bs4
pip install spacy
pip install sqlite3
pip install codecs
pip install onfigparser
pip install gensim
```
besides, two pre-trained model are used
```shell
python -m spacy download en_core_web_md
```
**en_core_web_md** from spacy is used to do the NERD part (tokenization and Lemmatisation) both for the data and the query
```shell
python -m gensim.downloader --download glove-wiki-gigaword-100
```
**glove-wiki-gigaword-100** is a pre-trained word2vec model and is used for query rewriting so that similar words can be applied to search. 

[Here](https://github.com/RaRe-Technologies/gensim-data), dataset can be found to train one's own word2vec model and some pre-trained one can also be found and applied directly(as the limit of time, I use a pre-trained one instead)




## Indexing
![](https://github.com/JiajingFang/Search_engine/blob/main/image/invertindex.png)
In **/code/new_index.py** an Inverted index Algorithm is used to index the raw data, make sure all the raw data is put under the file **/data/blogs** before running the script.

In Inverted index model, not only the term frequency (tf, the appearance frequency for a term in a certain doc d) will be recorded, but the doc frequency (df, the appearance frequency for a term in all docs) 

After buildling the inverted index database, we will get the model **ir.db** under **/data/**. The visualization of this model will be like the pic. 

The left part is the dictionary saving all different terms apear in raw data. 

The right part is a posting for each term, a posting saves all docs info for a term.


## Ranking
![](https://github.com/JiajingFang/Search_engine/blob/main/image/bm25.png)
A traditional BM25 scoring equation is used to retrieve and rank the results. For the pic, BM25 scoring equation is shown for a **given query Q** and **a document d**.

* qtf: term frequency in the query Q
* tf: term frequency in the doc d
* ld: doc length
* avg_l: average doc length
* N: docs amount
* df: document frequency for the given term t and doc d
* b,k1,k2: tuning parameter
from the **first equation**, we known that a BM25 score for a given query and doc is the sum of the score for all terms in the query regard to the given doc.

from the **second equation**, it shows the detail of score equation for a given term and doc. 
* First part is the score of the given term in the query, as we got a short query mostly, we can ignore this part.
* Second part is the score of TF term frequency is the given doc. The more term appears in the given doc, the higher score we got. But we use **ld/avg_l** to normalize the score.
* Third part is the score of IDF. The more term appears in different docs, the lower score we got. In this way, we can give more attention to rare word which can distinguish doc from doc, while ignoring the usual words.

