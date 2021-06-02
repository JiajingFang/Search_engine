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
**glove-wiki-gigaword-100** is a pre-trained word2vec model and is used for query rewriting so that similar words can be applied to search. [Here](https://github.com/RaRe-Technologies/gensim-data), dataset can be found to train one's own word2vec model and some pre-trained one can also be found and applied directly(as the limit of time, I use a pre-trained one instead)
## modify template
1.add dependencies in package.json<br>
```shell
yarn install
```
2.import bootstrap in index.js<br>
3.modify App.css and App.js for our need<br>
## develop in Exam folder
It is in src folder
## how to run
```shell
yarn start
```
can also use yarn build to build it
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/1.png)  
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/2.png)  
![](https://github.com/JiajingFang/QuizApp-React-/blob/master/image/3.png)  
