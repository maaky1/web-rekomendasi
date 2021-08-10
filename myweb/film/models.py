from django.db import models
from django.utils.text import slugify

# Create your models here.
class film(models.Model):
	id_film 		= models.IntegerField(primary_key=True)
	judul_film		= models.CharField(max_length=255)
	sinopsis_film	= models.TextField()
	image			= models.ImageField(null=True, blank=True)
	slug 			= models.SlugField(blank=True, editable=False)
	bobottfidf		= models.CharField(max_length=50, blank=True, editable=False)
	labelfilm		= models.CharField(max_length=10, blank=True, editable=False)

	def save(self):
		self.slug = slugify(self.judul_film)
		super(film, self).save()

	def __str__(self):
		return "{}. {}".format(self.id_film, self.judul_film)


class userreview(models.Model):
	datafilm 	= models.ForeignKey(film, on_delete=models.PROTECT)
	id_komentar = models.AutoField(primary_key=True)
	username	= models.CharField(max_length=20)
	komentar 	= models.TextField()
	labelkomen 	= models.CharField(max_length=10, blank=True, editable=False)

	def __str__(self):
		return "{} | {}".format(self.id_komentar, self.datafilm)


class katapositif(models.Model):
	word 	= models.CharField(max_length=50)

	def __str__(self):
		return "{}".format(self.word)


class katanegatif(models.Model):
	word 	= models.CharField(max_length=50)

	def __str__(self):
		return "{}".format(self.word)


class historiuser(models.Model):
	id_historiuser	= models.AutoField(primary_key=True)
	username		= models.CharField(max_length=20)
	id_film			= models.TextField(default="")

	def __str__(self):
		return "{} | {} | {}".format(self.id_historiuser, self.username, self.id_film)

class userrekomen(models.Model):
	id_rekom	= models.AutoField(primary_key=True)
	username	= models.CharField(max_length=20)
	rekomen 	= models.TextField(default="")

	def __str__(self):
		return "{}".format(self.rekomen)

class dbbosok(models.Model):
	id 			= models.AutoField(primary_key=True)
	kata 		= models.CharField(max_length=100)
	frekuensi	= models.IntegerField()
	film 		= models.IntegerField()

	def __str__(self):
		return "{} | {} | {}".format(self.kata, self.frekuensi, self.film)

class historiuserpp(models.Model):
	id 			= models.AutoField(primary_key=True)
	film 		= models.IntegerField()
	kata 		= models.CharField(max_length=100)
	bobottfidf 	= models.CharField(max_length=100)
	username	= models.CharField(max_length=20)

	def __str__(self):
		return "{}. {}".format(self.username ,self.bobottfidf)