from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import *
from django.db.models import Count, Sum
import math
import re
from .models import dbbosok, katapositif, katanegatif

def hapussimbol(text):
	data = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t \n])|[0-9]','',text)
	return data


def casefolding(text):
	data = text.lower()
	return data


def tokenisasi(text):
	word = word_tokenize(text)
	stop_words = set(stopwords.words("english"))
	stopw = [k for k in word if k not in stop_words]
	return stopw


def stemming(text):
	ps = PorterStemmer()
	stemm = [ps.stem(w) for w in text]
	return stemm


def filtering(text):
	frekuensi = {}
	for sent in text:
		count = frekuensi.get(sent, 0)
		frekuensi[sent] = count + 1
	return frekuensi


def hitungtf(text):
	hasiltf = []
	for i in text:
		cari = dbbosok.objects.filter(kata=i)
		for k in cari:
			# print(k)
			temp = {'Id Film' : k.film, 'Term' : k.kata, 'Frekuensi' : k.frekuensi}
			hasiltf.append(temp)
	return hasiltf


def hitungidf(text):
	hasilidf = []
	N = 30
	for i in text:
		cari = dbbosok.objects.filter(kata=i).count()
		hitung = math.log10(N/cari)
		temp = {'Term' : i, 'IDF Score' : hitung}
		hasilidf.append(temp)
	return hasilidf


def hitungtfidf(texttf, textidf):	
	hasiltfidf = []
	for tf in texttf:
		id = tf['Id Film']
		for idf in textidf:
			if tf['Term'] == idf ['Term']:
				hitung = tf['Frekuensi'] * idf ['IDF Score']
				temp = {'Id Film' : id, 'Term' : tf['Term'], 'TF-IDF Score' : hitung}
				hasiltfidf.append(temp)
	return hasiltfidf


def prepopsentimen(text):
	KP = katapositif.objects.all()
	KN = katanegatif.objects.all()
	datapos = []
	dataneg = []
	for w in KP:
		datapos.append(w.word)

	for w in KN:
		dataneg.append(w.word)

	stripped = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|[0-9]','',text).lower()
	words = word_tokenize(stripped)
	stop_words = set(stopwords.words("english"))
	stopw = [k for k in words if k not in stop_words]
	hasil = []
	resultsentimen = []
	resultscore = []
	resultpos = []
	resultneg = []
	poscounter = 0
	negcounter = 0
	score = 0

	for i in stopw:
		hasil.append(i)

	for j in hasil:
		if j in datapos:
			poscounter += 1
		elif j in dataneg:
			negcounter += 1
	sentimen = ""
	if poscounter > negcounter:
		score = poscounter / (poscounter + negcounter)
		sentimen = "Positif"

	elif poscounter < negcounter:
		score = poscounter / (poscounter + negcounter)
		sentimen = "Negatif"
		
	else:
		sentimen = "Netral"
	
	resultpos.append(poscounter)
	resultneg.append(negcounter)
	resultscore.append(score)
	resultsentimen.append(sentimen)

	return resultsentimen, resultscore, resultpos, resultneg