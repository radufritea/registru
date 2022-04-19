from django	import forms 
from .models import Visit, Client, Product, WeekPlan
from datetime import date

class VisitForm(forms.ModelForm):

	date_created = forms.DateTimeField(
		label = "Data vizitei",
		initial=date.today,
		input_formats=['%d/%m/%Y %H:%M'],
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'form_input',
			},
		),
	)

	products = forms.MultipleChoiceField(
		widget = forms.CheckboxSelectMultiple,
		choices = [(product.pk, product.name) for product in Product.objects.all()],
		label = "Lista de produse"
	)
	
	shelf_image = forms.ImageField()
	
	class Meta:
		model = Visit
		fields = "__all__"
		exclude = ("last-modified",)
		labels = {"agent": "Nume ASS", "client": "Client", "shop": "Magazin", "shelf_image": "Adauga imagine raft"}
			
class PlanForm(forms.ModelForm):
	start_date = forms.DateTimeField(
		input_formats=['%d/%m/%Y %H:%M'],
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'form_input',
			},
		),
	)

	end_date = forms.DateTimeField(
		input_formats=['%d/%m/%Y %H:%M'],
		widget=forms.DateInput(
			attrs={
				'type': 'date',
				'class': 'form_input',
			},
		),
	)
	class Meta:
		model = WeekPlan
		fields = "__all__"
		exclude = ("last-modified",)
		labels = {
			"monday_location": "Locație",
			"monday_goal": "Obiective",
			"monday_achieved": "Realizări",
			"tuesday_location": "Locație",
			"tuesday_goal": "Obiective",
			"tuesday_achieved": "Realizări",
			"wendsday_location": "Locație",
			"wendsday_goal": "Obiective",
			"wendsday_achieved": "Realizări",
			"thursday_location": "Locație",
			"thursday_goal": "Obiective",
			"thursday_achieved": "Realizări",
			"friday_location": "Locație",
			"friday_goal": "Obiective",
			"friday_achieved": "Realizări",
		}