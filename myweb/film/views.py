from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum
from django.db import connection
from nltk.tokenize import sent_tokenize, word_tokenize
from django.contrib.auth.models import User, auth
from googletrans import Translator
from .models import film, userreview, historiuser, userrekomen, dbbosok, historiuserpp
from . import preprop
import re, time

def index(request):
	posts = film.objects.all()

	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Film',
		'Content':'Film',
		'posts':posts,
	}
	return render(request,'film/index.html', context)


def carifilm(request):	
	if request.method == "POST":
		search = request.POST['search']
		films = film.objects.filter(judul_film__contains=search)

	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Pencarian Film',
		'Content':'Hasil Pencarian Film',
		'search':search,
		'films':films,
	}
	return render(request,'film/search.html', context)


def detailfilm(request, sluginput):
	posts = film.objects.get(slug=sluginput)
	komen = userreview.objects.filter(datafilm_id=posts)
	user = request.user.username
	translator = Translator()
	datakomen = []
	data = []

	if request.method == "POST":
		username	= user
		komentar 	= request.POST['kolomkomentar']
		komentartl	= translator.translate(komentar, src='id', dest='en').text
		datafilm_id = posts.id_film
 		
		newkomen = userreview.objects.create(
			username = username,
			komentar = komentartl,
			datafilm_id = datafilm_id
			)
		newkomen.save()

		histori = historiuser(username=username, id_film=datafilm_id)
		histori.save()

	for i in komen:
		datakomen.append(i.komentar)

	sentimen = [preprop.prepopsentimen(s) for s in datakomen]

	tempDict = []
	for i in range(len(komen)):
		tempDict = komen[i]
		for j in range(len(sentimen)):
			if j == i:
				komen[i].labelkomen = sentimen[i][0]
				komen[i].save()
	
	jumlahpos = userreview.objects.filter(datafilm_id=posts, labelkomen__contains='positif').count()
	jumlahneg = userreview.objects.filter(datafilm_id=posts, labelkomen__contains='negatif').count()

	sentimen = ""
	if jumlahpos > jumlahneg:
		sentimen = "Positif"	
	elif jumlahpos < jumlahneg:
		sentimen = "Negatif"
	else:
		sentimen = "Netral"
			
	posts.labelfilm = sentimen
	posts.save()

	context = {
		'Title_Web':'Film | ' + posts.judul_film,
		'Content':'Detail Film ' + posts.judul_film,
		'posts':posts,
		'komen':komen,
	}

	return render(request,'film/detail.html', context)


def pptfidf(request):
	user = request.user.username
	histori = historiuser.objects.filter(username=user)
	historipp = historiuserpp.objects.filter(username=user)
	datafilm = film.objects.all()
	testing = histori.count()
	feedbackint = ""
	query = []
	hasil = []
	score = []
	rekomid = []
	hasilrekom = []

	if testing == 0:
		feedbackint = 0
	else:
		feedbackint = 1
		for i in histori:
			id = i.id_film
			data = film.objects.filter(id_film=id)
			for j in data:
				query.append(j.sinopsis_film)
				
		for i in query:
			punctuation = preprop.hapussimbol(i)
			casefolding = preprop.casefolding(punctuation)
			tokenisasi = preprop.tokenisasi(casefolding)
			stemming = preprop.stemming(tokenisasi)
			filtering = preprop.filtering(stemming)
			hitungtf = preprop.hitungtf(filtering)
			hitungidf = preprop.hitungidf(filtering)
			hitungtfidf = preprop.hitungtfidf(hitungtf, hitungidf)
			score.append(hitungtfidf)

		historipp.delete()
		for i in range(len(score)):
			for j in range(len(score[i])):
				for k in score[i][j].keys():
					id = score[i][j]['Id Film']
					kata = score[i][j]['Term']
					bobot = score[i][j]['TF-IDF Score']
					
				inp = historiuserpp.objects.create(
					film = id,
					kata = kata,
					bobottfidf = bobot,
					username = user
					)
				inp.save()	

		for i in datafilm:
			id = i.id_film
			carinilai = historiuserpp.objects.filter(username=user, film=id).aggregate(Sum('bobottfidf'))
			nilai = carinilai.get('bobottfidf__sum')
			if nilai != None:
				nilai = nilai
			else:
				nilai = 0
			inp = film.objects.get(id_film=id)
			inp.bobottfidf = 0
			inp.save()			
			inp.bobottfidf = nilai
			inp.save()

		kecuali = []
		for i in histori:
			kecuali.append(i.id_film)
		ranking = film.objects.filter(labelfilm__contains='positif').exclude(id_film__in=kecuali).order_by('-bobottfidf')
		rekomendasi = ranking[:10]
		
		datarekomen = []		
		for i in range(len(rekomendasi)):
			datarekomen.append(rekomendasi[i].id_film)

		usr = userrekomen.objects.all().count()
		if usr != 0:
			data = userrekomen.objects.all()
			for i in data:
				if i.username == user:
					i.rekomen = 0
					i.save()
					i.rekomen = datarekomen
					i.save()
				else:
					inp = userrekomen.objects.create(
						username = user,
						rekomen = datarekomen
						)
					inp.save()
		else:
			data = userrekomen.objects.create(
				username = user,
				rekomen = datarekomen
				)
			data.save()

		usr = userrekomen.objects.filter(username=user)
		
		
		for i in usr:
			rekomid.append(i.rekomen)
		
		for i in range(len(rekomid)):
			r = re.findall('[0-9]+', rekomid[i])
			for uid in r:
				films = film.objects.get(id_film=uid)
				hasilrekom.append(films)

	context = {
		'Title':'Web Rekomedasi',
		'Title_Web':'Rekomendasi',
		'Content':'Rekomendasi',
		'rekomendasi':hasilrekom,
		'feed':feedbackint,
	}

	return render(request, 'film/tfidf.html', context)