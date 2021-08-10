from django import forms
from user.models import profil

class profilForm(forms.ModelForm):
	class Meta:
		model = profil
		widgets = {
			'password' : forms.PasswordInput(),
		}