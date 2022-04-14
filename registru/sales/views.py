from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from datetime import date

from .models import Visit, Client, Shop, Agent, WeekPlan
from .forms import VisitForm, PlanForm

# Create your views here.

def weekly_plan(request):
	my_date = date.today()
	year, week_num, day_of_week = my_date.isocalendar()

	# Create a list with all WeekPlan entries that have week_num field = to the current week's number
	current_plan = WeekPlan.objects.filter(week_num = week_num).values_list('id')

	# If the list is empty (there is no entry with the current week's number), redirect to add plan
	if not current_plan:
		return redirect('sales:add_plan')
	# if the list is not empty, show the data 
	else:
		plan = WeekPlan.objects.get(week_num=week_num)
		form = PlanForm(instance=plan)	
		return render(request, 'sales/sales.html', {'form': form})

def add_plan(request):
	my_date = date.today()
	year, week_num, day_of_week = my_date.isocalendar()

	if request.method != 'POST':
		form = PlanForm()
	else:
		form = PlanForm(data=request.POST)
		if form.is_valid():
			new_plan = form.save(commit=False)
			new_plan.week_num = week_num
			new_plan.save()
			return redirect('sales:sales')
	return render(request, 'sales/add_plan.html', {"form": form})


def visits(request):
	visits = Visit.objects.all()
	form = VisitForm()
	return render(request, 'sales/visits.html', {'visits': visits, 'form': form})

def visit(request, visit_id):
	visit = Visit.objects.get(id=visit_id)
	products = visit.products.all()
	return render(request, 'sales/visit.html', {
		'visit': visit,
		'products': products
		})

def new_visit(request):

	if request.method != 'POST':
		form = VisitForm()
	else:
		form = VisitForm(request.POST, request.FILES)

		if form.is_valid():
			shelf_image = Visit(shelf_image=request.FILES["shelf_image"])
			form.save()
			return redirect('sales:visits')

	return render(request, 'sales/new_visit.html', {'form': form})

def info_competition(request):
	return render(request, 'sales/info_competition.html')