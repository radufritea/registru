from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from datetime import date
from django.core.paginator import Paginator

from .models import Visit, Client, Shop, Agent, WeekPlan
from .forms import VisitForm, PlanForm
from datetime import date, timedelta	

# Create your views here.

def index(request):
# WEEKLY PLANNING
	my_date = date.today()
	week_day = my_date.weekday()
	
	if request.method == "POST":
		form = PlanForm(data=request.POST)
		plan = WeekPlan.objects.last()
		if plan == None:
			start_date = my_date - timedelta(days=week_day)
			end_date = my_date + timedelta(days=(4 - week_day))
		else:
			start_date = plan.start_date
			end_date = plan.end_date
		
		if form.is_valid():
			new_plan = form.save(commit=False)
			agent = Agent.objects.get(user_id=request.user.id)
			new_plan.agent_id = agent.id
			new_plan.save()
			return redirect('sales:index')

	elif request.method == "GET":
		plan = WeekPlan.objects.last()
		if plan == None:
			form=PlanForm()
			start_date = my_date - timedelta(days=week_day)
			end_date = my_date + timedelta(days=(4 - week_day))
		else:
			form = PlanForm(instance=plan)
			start_date = plan.start_date
			end_date = plan.end_date

# VISITS
	visits = Visit.objects.all().order_by('-date_created')
	paginator = Paginator(visits, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'sales/index.html', {
		'form': form, 
		'start_date': start_date, 
		'end_date': end_date,
		'page_obj': page_obj,
	})


def add_plan(request):
	if request.method == "POST":
		form = PlanForm(data=request.POST)
		if form.is_valid():
			new_plan = form.save(commit=False)
			agent = Agent.objects.get(user_id=request.user.id)
			new_plan.agent_id = agent.id
			new_plan.save()
			return redirect('sales:index')
	elif request.method == "GET":
		form=PlanForm()

	return render(request, 'sales/add_plan.html', {'form': form})


def visits(request):
	visits = Visit.objects.all().order_by('-date_created')
	paginator = Paginator(visits, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'sales/visits.html', {'page_obj': page_obj})

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