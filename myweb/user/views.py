from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from film.models import historiuser, film
# Create your views here.

def index(request):
	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Login',
		'Content':'Login',
	}

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(
			username = username,
			password = password
			)

		if user is not None:
			if user.username == "admin":
				auth.login(request, user)
				return redirect('admin:index')
			
			else:
				auth.login(request, user)
				return redirect('loginuser:userprofil')

		else:
			messages.info(request, 'Username/Password Tidak Cocok')
			return redirect('user:index')

	return render(request,'user/index.html', context)

def daftar(request):
	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Daftar',
		'Content':'Daftar',
	}

	if request.method == "POST":
		nama_depan		= request.POST['first_name']
		nama_belakang	= request.POST['last_name']
		username 		= request.POST['username']
		password1		= request.POST['password1']
		password2		= request.POST['password2']

		if password1 == password2:
			if User.objects.filter(username = username).exists():
				messages.info(request, 'Username telah Terpakai')
				return redirect('user:daftar')
			else:
				user = User.objects.create_user(
					first_name = nama_depan,
					last_name = nama_belakang,
					username = username,
					password = password1
					)
				user.save();
				messages.info(request, 'user created')
		else:
			messages.info(request, 'Password Tidak Cocok')
			return redirect('user:daftar')

		return redirect('user:index')

	return render(request,'user/register.html', context)

def keluar(request):
	auth.logout(request)
	
	return redirect('user:index')

def userprofil(request):
	histori = historiuser.objects.all()
	user = request.user.username
	data = []
	counter = 0

	for i in histori:
		# print(i.username)
		if i.username == user:
			counter = 1
			f = film.objects.filter(id_film=i.id_film)
			data.append(f)
		else:
			counter = 0

	context = {
		'Title':'Web Rekomendasi',
		'Title_Web':'Profil ' + user,
		'Content':'Profil',
		'histori':histori,
		'data':data,
		'counter':counter,
	}

	return render(request,'user/profil.html', context)