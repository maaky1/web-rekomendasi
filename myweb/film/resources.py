from import_export import resources
from .models import katapositif, katanegatif, film, userreview

class filmresource(resources.ModelResource):
	class Meta:
		model = film

class userreviewresource(resources.ModelResource):
	class Meta:
		model = userreview

class katapositifresource(resources.ModelResource):
	class Meta:
		model = katapositif

class katanegatifresource(resources.ModelResource):
	class Meta:
		model = katanegatif