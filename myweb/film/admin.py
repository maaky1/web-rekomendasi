from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import film, userreview, katapositif, katanegatif, historiuser, userrekomen, dbbosok, historiuserpp
@admin.register(film)
class filmadmin(ImportExportModelAdmin):
	readonly_fields = ['slug', 'bobottfidf', 'labelfilm']	
	# pass

@admin.register(userreview)
class userreviewmadmin(ImportExportModelAdmin):
	readonly_fields = ['id_komentar','labelkomen']
	# pass

@admin.register(katapositif)
class katapositifadmin(ImportExportModelAdmin):
	# list_display = ['id_word', 'word']
	pass

@admin.register(katanegatif)
class katanegatifsadmin(ImportExportModelAdmin):
	# list_display = ['id_word', 'word']
	pass

admin.site.register(historiuser)
admin.site.register(userrekomen)
admin.site.register(dbbosok)
admin.site.register(historiuserpp)