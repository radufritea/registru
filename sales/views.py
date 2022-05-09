from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Visit, Agent, WeekPlan
from .forms import VisitForm, PlanForm

# Create your views here.
my_date = date.today()
week_day = my_date.weekday()

def index(request):
# WEEKLY PLANNING
	pk = request.GET.get('pk')
	start_date = my_date - timedelta(days=week_day)
	end_date = my_date + timedelta(days=(4 - week_day))
	plan = WeekPlan.objects.order_by('start_date').last()
	week_plans = WeekPlan.objects.all().order_by('-start_date')
	
	visits = Visit.objects.all().order_by('-date_created')
	paginator = Paginator(visits, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	if request.method == "GET":
	# first acces, no plans in db
		if not week_plans:
			form=PlanForm(initial={'start_date': start_date, 'end_date': end_date})
		else:
			if pk != None:
				plan = WeekPlan.objects.get(id=pk)
			else:
				plan = WeekPlan.objects.get(start_date=start_date)	
			
			form = PlanForm(instance=plan)

	elif request.method == 'POST':
		form = PlanForm(request.POST, initial={'start_date': start_date, 'end_date': end_date})
		if form.is_valid():
			new_plan = form.save(commit=False)
			agent = Agent.objects.get(user_id=request.user.id)
			new_plan.agent_id = agent.id
			new_plan.start_date = request.POST.get('start_date')
			new_plan.end_date = request.POST.get('end_date')
			if plan == None:
				new_plan.id = 1
			else:
				new_plan.id = request.POST.get('plan_id')
			new_plan.save()
			print(new_plan.end_date)
			return redirect(request.META['HTTP_REFERER'])
		else:
			print (form.errors)
	
	return render(request, 'sales/index.html', {
		'form': form,
		'plan': plan,
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
			new_visit.save()
			return HttpResponseRedirect(reverse('sales:visits'))
		else:
			print(form.errors)
	
	elif request.method == "GET":
		form=VisitForm()

	return render(request, 'sales/new_visit.html', {'form': form})


def info_competition(request):
	return render(request, 'sales/info_competition.html')

def visits_reports(request):
	agents = Agent.objects.all().order_by("user")
	q = request.GET.get('q')
	if q != None:
		selected_agent = Agent.objects.get(id=q)
	else:
		selected_agent = None

	if selected_agent == None:
		visits = Visit.objects.all().order_by("-date_created")
	else:
		visits = Visit.objects.filter(agent=selected_agent)

	return render(request, 'sales/visits_reports.html', {
		'agents': agents,
		'visits': visits,
		'agent': selected_agent,
	})

def competition_reports(request):
	return render(request, 'sales/competition_reports.html')
