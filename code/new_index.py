from os import listdir
import spacy
import sqlite3
import configparser
import re
import os
import codecs
import pandas as pd
import requests, io
from bs4 import BeautifulSoup


class Doc:
    docid = 0
    date_time = ''
    tf = 0
    ld = 0
    def __init__(self, docid, tf, ld):
        self.docid = docid
        self.tf = tf
        self.ld = ld
    def __repr__(self):
        return(str(self.docid) + '\t' + str(self.tf) + '\t' + str(self.ld))
    def __str__(self):
        return(str(self.docid) + '\t' + str(self.tf) + '\t' + str(self.ld))
 
class IndexModule:
    #stop_words = set()
    postings_lists = {}
     
    config_path = ''
    config_encoding = ''
     
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)

    def process_data_text(self,filename):
    	# List of labels processed from file name.
    	config = configparser.ConfigParser()
    	config.read(self.config_path, self.config_encoding)
    	labels = filename.rstrip('.xml').lower().split('.')
    	# Beautiful soup to parse the xml files
    	blog = BeautifulSoup(codecs.open( config['DEFAULT']['doc_dir_path'] + filename, encoding='utf-8', errors='ignore'), "lxml")
    	#f Finds <post> tags inside xml
    	for post in blog.find_all('post'):
    		# Fetches text insidde <post> tags
    		post_text = post.text
    		post_text = re.sub('[^0-9A-Za-z]+', ' ', post_text).strip().lower().split()
    		post_text = ' '.join(post_text)
    		processed_text = 'type:' + labels[3] + ' gender:' + labels[1] + ' age: ' + labels[2] + ' zodiac:' + labels[4] + ' text:' + post_text
    	return labels[0],processed_text

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
     
    def write_postings_to_db(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
         
        c.execute('''DROP TABLE IF EXISTS postings''')
        c.execute('''CREATE TABLE postings
                     (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')
 
        for key, value in self.postings_lists.items():
            doc_list = '\n'.join(map(str,value[1]))
            t = (key, value[0], doc_list)
            c.execute("INSERT INTO postings VALUES (?, ?, ?)", t)
 
        conn.commit()
        conn.close()
     
    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        files = listdir(config['DEFAULT']['doc_dir_path'])
        #print(files)
        AVG_L = 0
        num = 1
        nlp = spacy.load("en_core_web_md")
        for filename in files:
        	docnum, newfile = self.process_data_text(filename)
        	#print(newfile)
        	#print(docnum)
        	docid = docnum
        	num = num + 1
        	seg_list = nlp(newfile)
        	ld, cleaned_dict = self.clean_list(seg_list)
        	print(cleaned_dict)
        	AVG_L = AVG_L + ld
        	for key, value in cleaned_dict.items():
        		d = Doc(docid, value, ld)
        		if key in self.postings_lists:
        			self.postings_lists[key][0] = self.postings_lists[key][0] + 1 # df++
        			self.postings_lists[key][1].append(d)
        		else:
        			self.postings_lists[key] = [1, [d]] # [df, [Doc]]
        AVG_L = AVG_L / len(files)
        print(AVG_L)
        config.set('DEFAULT', 'N', str(len(files)))
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        with open(self.config_path, 'w', encoding = self.config_encoding) as configfile:
        	config.write(configfile)
        self.write_postings_to_db(config['DEFAULT']['db_path'])


if __name__ == "__main__":
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()