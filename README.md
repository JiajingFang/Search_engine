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
## how to run
```shell
yarn start
```
can also use yarn build to build it
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/1.png)  
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/2.png)  
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/3.png)  
