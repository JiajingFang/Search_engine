import spacy
import math
import operator
import sqlite3
import configparser
from os import listdir
import gensim.downloader as api

class SearchEngine:
    stop_words = set()
    
    config_path = ''
    config_encoding = ''
    
    K1 = 0
    B = 0
    N = 0
    AVG_L = 0

    SIM = 0
    
    conn = None
    
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding = config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.conn = sqlite3.connect(config['DEFAULT']['db_path'])
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])
        self.SIM = int(config['DEFAULT']['SIM'])
        

    def __del__(self):
        self.conn.close()
    

    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            if not i.is_stop:
                n = n + 1
                if i.lemma_ in cleaned_dict:
                    cleaned_dict[i.lemma_] = cleaned_dict[i.lemma_] + 1
                else:
                    cleaned_dict[i.lemma_] = 1
        return n, cleaned_dict

    def fetch_from_db(self, term):
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return(c.fetchone())
    
    def result_by_BM25(self, sentence):
        nlp = spacy.load("en_core_web_md")
        seg_list = nlp(sentence)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[1]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs = r[2].split('\n')
            for doc in docs:
                docid, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s
        BM25_scores = sorted(BM25_scores.items(), key = operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            #print(BM25_scores[:10])
            return 1, BM25_scores

    def query_rewrite(self, sentence):
        nlp = spacy.load("en_core_web_md")
        seg_list = nlp(sentence)
        n, cleaned_dict = self.clean_list(seg_list)
        similar_word = []
        similar_query = []
        for term in cleaned_dict.keys():
            similar_word.append(model.most_similar(term)[:self.SIM])
        for i in range(len(similar_word[0])):
            new_q = " ".join([str(similar_word[j][i]) for j in range(len(similar_word))])
            new_q = new_q.strip().lower()
            similar_query.append(new_q)
        return similar_query


    def fetch_filename(self, rs):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        files = listdir(config['DEFAULT']['doc_dir_path'])
        listnum = {}
        resultBM25 = {}
        for filename in files:
            labels = filename.rstrip('.xml').lower().split('.')
            listnum[labels[0]] = filename
        for r in rs:
            if str(r[0]) in listnum.keys():
                fullname = listnum[str(r[0])]
                resultBM25[fullname] = r[1]
        return resultBM25


    def search(self, sentence, sort_type = 0):
        if sort_type == 0:
            return self.result_by_BM25(sentence)


if __name__ == "__main__":
    se = SearchEngine('../config.ini', 'utf-8')
    model = api.load("glove-wiki-gigaword-100")
    a = input("please input search query:")
    a = a.strip().lower()
    flag, rs = se.search(a, 0)
    rs_result = se.fetch_filename(rs[:10])
    for rs1 in rs_result:
        print(f'{rs_result[rs1]:f}   {rs1}')
        #print(str(rs_result[rs1])+"   "+rs1)
    b = input("Not satisfy with the result? Apply similar search?[y/n]")
    if b == 'y':
        queries = se.query_rewrite(a)
        #print(queries)
        for query in queries:
            print(query)
            flag, rs = se.search(query, 0)
            rs_result = se.fetch_filename(rs[:3])
            for rs2 in rs_result:
                print(f'{rs_result[rs2]:f}   {rs2}')
                #print(str(rs_result[rs2])+"   "+rs2)

    

    