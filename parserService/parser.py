import json
import urllib.request
import requests
from tika import parser
from flask import Flask, make_response
from flask import request
import os
from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import array
import bs4
import time
import re

apiURL = "http://54.94.183.24"
apiPort = "6570"

app = Flask(__name__)

def getToken():
	headers = {'Content-Type': 'application/json'}
	data = {'credential': 'userAdmin', 'password':'utn.frba.nlp'}
	r = requests.post(apiURL + ":" + apiPort + "/api/auth/signin", data=json.dumps(data), headers=headers)
	
	return json.loads(r.text)["access_token"]

def getFileContent(documentId):
	token = getToken();
	
	headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
	print(headers)
	response = requests.get(apiURL + ":" + apiPort + "/documents/" + documentId, headers=headers)
	
	y = json.loads(response.content)
	documentURI = y["document_uri"]
	documentName = y["document_name"]	
	
	opener = urllib.request.build_opener()
	opener.addheaders = [('Authorization', 'Bearer ' + token)]
	urllib.request.install_opener(opener)

	urllib.request.urlretrieve(documentURI, "documents/" + documentName)
	parsedPDF = parser.from_file("documents/" + documentName)
	content= parsedPDF["content"]
	
	os.remove("documents/" + documentName)
	
	return content

def getKeyWords(documentId):
	
	nlp = spacy.load('es_core_news_sm')
	
	class TextRank4Keyword():		
		def __init__(self):
			self.d = 0.85 # damping coefficient, usually is .85
			self.min_diff = 1e-5 # convergence threshold
			self.steps = 10 # iteration steps
			self.node_weight = None # save keywords and its weight		
		def set_stopwords(self, stopwords):  
			for word in STOP_WORDS.union(set(stopwords)):
				lexeme = nlp.vocab[word]
				lexeme.is_stop = True		
		def sentence_segment(self, doc, candidate_pos, lower):
			sentences = []
			for sent in doc.sents:
				selected_words = []
				for token in sent:
					# Store words only with cadidate POS tag
					if token.pos_ in candidate_pos and token.is_stop is False:
						if lower is True:
							selected_words.append(token.text.lower())
						else:
							selected_words.append(token.text)
				sentences.append(selected_words)
			return sentences			
		def get_vocab(self, sentences):
			vocab = OrderedDict()
			i = 0
			for sentence in sentences:
				for word in sentence:
					if word not in vocab:
						vocab[word] = i
						i += 1
			return vocab		
		def get_token_pairs(self, window_size, sentences):
			token_pairs = list()
			for sentence in sentences:
				for i, word in enumerate(sentence):
					for j in range(i+1, i+window_size):
						if j >= len(sentence):
							break
						pair = (word, sentence[j])
						if pair not in token_pairs:
							token_pairs.append(pair)
			return token_pairs			
		def symmetrize(self, a):
			return a + a.T - np.diag(a.diagonal())		
		def get_matrix(self, vocab, token_pairs):
			vocab_size = len(vocab)
			g = np.zeros((vocab_size, vocab_size), dtype='float')
			for word1, word2 in token_pairs:
				i, j = vocab[word1], vocab[word2]
				g[i][j] = 1
			g = self.symmetrize(g)
			norm = np.sum(g, axis=0)
			g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm			
			return g_norm		
		def get_keywords(self, number=10):
			node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
			items = []
			for i, (key, value) in enumerate(node_weight.items()):
				data = {}
				data["name"] = key
				data["value"] = str(value)
				items.append(data)
				if i > number:
					break
			return json.dumps(items)
		def analyze(self, text, 
					candidate_pos=['NOUN', 'PROPN'], 
					window_size=4, lower=False, stopwords=list()):
			self.set_stopwords(stopwords)
			
			doc = nlp(text)
			sentences = self.sentence_segment(doc, candidate_pos, lower)
			vocab = self.get_vocab(sentences)
			token_pairs = self.get_token_pairs(window_size, sentences)
			g = self.get_matrix(vocab, token_pairs)
			pr = np.array([1] * len(vocab))
			previous_pr = 0
			for epoch in range(self.steps):
				pr = (1-self.d) + self.d * np.dot(g, pr)
				if abs(previous_pr - sum(pr))  < self.min_diff:
					break
				else:
					previous_pr = sum(pr)
			node_weight = dict()
			for word, index in vocab.items():
				node_weight[word] = pr[index]			
			self.node_weight = node_weight
			
	text = getFileContent(documentId)
			
	tr4w = TextRank4Keyword()
	tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
	return tr4w.get_keywords(10)

def getTextFromURL(url):
	response = requests.get(url)

	data = []
	if response is not None:
		html = bs4.BeautifulSoup(response.text, 'html.parser')

		paragraphs = html.select("p")
		for para in paragraphs:
			data.append(para.text)
	return data

class ScrappingResultItem:
	def __init__(self, url, contents):
		self.url = url
		self.contents = contents


@app.route('/documents/<documentId>/contents')
def route_contents(documentId):
	response = make_response(getFileContent(documentId), 200)
	response.mimetype = "text/plain"
	return response
	
@app.route('/documents/<documentId>/keywords')
def route_keywords(documentId):
	keywords = getKeyWords(documentId)
	print(type(keywords))
	print(keywords)
	response = make_response(keywords, 200)
	response.mimetype = "application/json"
	return response

@app.route('/scrapping/')
def scrappingcontent():
	n = request.args.get('n', default = 10, type = int)
	q = request.args.get('q', default = "nlp")
	
	page = requests.get("https://www.google.com/search?q=" + q + "&num=" + str(n))
	soup = bs4.BeautifulSoup(page.content, 'html.parser')
	urls=[]
	links = soup.findAll("a")
	for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
		urls.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))
	items = []
	for url in urls:
		if(url != urls[len(urls)-1]):
			url=' '.join(url)
			url = url.split('&')[0]
			content = []
			try:
				content = getTextFromURL(url)
			except:
				print("An exception occurred")
			items.append(ScrappingResultItem(url, content).__dict__)
	
	body = json.dumps(items)
	response = make_response(body, 200)
	headers = {'Content-type': 'application/json', 'charset': 'utf-8'}
	response.headers = headers
	return response

app.run(host='0.0.0.0', port=4242)