from django.shortcuts import render
from film.models import film, userrekomen
import re
# Create your views here.

def index(request):
	data = film.objects.order_by('?')[:6]
	
	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Homepage',
		'Content':'Halaman Utama',
		'film':data,
	}

	return render(request,'index.html', context)