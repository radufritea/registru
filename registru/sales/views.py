from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from datetime import date
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Visit, Client, Shop, Agent, WeekPlan
from .forms import VisitForm, PlanForm
from datetime import date, timedelta	

# Create your views here.

def index(request):
# WEEKLY PLANNING
	my_date = date.today()
	week_day = my_date.weekday()
	pk = request.GET.get('pk')
	# Check if user selected a plan from index dropdown list
	if pk != None:
		# if he did, select the plan he chose
		plan = WeekPlan.objects.get(id=pk)
	else:
		# if not, select the plan with the latest "start_date"
		plan = WeekPlan.objects.order_by('start_date').last()

	# Check if there is no plan in the db
	if plan == None:
		start_date = my_date - timedelta(days=week_day)
		end_date = my_date + timedelta(days=(4 - week_day))
		id = 1
	else:
		start_date = plan.start_date
		end_date = plan.end_date
		id = plan.id

	if request.method == "GET":
		week_plans = WeekPlan.objects.all()

		if plan == None:
			form=PlanForm()
		else:
			form = PlanForm(instance=plan)
	
	elif request.method == "POST":
		form = PlanForm(data=request.POST)

		if form.is_valid():
			new_plan = form.save(commit=False)
			new_plan.id = id
			agent = Agent.objects.get(user_id=request.user.id)
			new_plan.agent_id = agent.id
			new_plan.start_date = start_date
			new_plan.end_date = end_date
			new_plan.save()
			return redirect('sales:index')
		else:
			print (form.errors)

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
		'week_plans': week_plans,
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

def plan(request, pk):
	plan = WeekPlan.objects.get(id=pk)
	form = PlanForm()
	return render(request, 'sales/plan.html', {'plan': plan, 'form': form})

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

	if request.method == "POST":
		form = VisitForm(request.POST, request.FILES)
		if form.is_valid():
			new_visit = form.save(commit=False)
			agent = Agent.objects.get(user_id=request.user.id)
			new_visit.agent_id = agent.id
			# new_visit.shelf_image = Visit(shelf_image=request.FILES["shelf_image"])
			new_visit.save()
			return HttpResponseRedirect(reverse('sales:visits'))
		else:
			print(form.errors)
	
	elif request.method == "GET":
		form=VisitForm()

	return render(request, 'sales/new_visit.html', {'form': form})

def info_competition(request):
	return render(request, 'sales/info_competition.html')