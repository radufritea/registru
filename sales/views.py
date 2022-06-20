from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Visit, Agent, WeekPlan, Product, Client, Shop, County, ProductInfo, PriceEntry
from .forms import VisitForm, PlanForm

# Set date variables
my_date = date.today()
week_day = my_date.weekday()
start_date = my_date - timedelta(days=week_day)
end_date = my_date + timedelta(days=(4 - week_day))

def index(request):
# load homepage
    if request.method == "GET":
        if request.user.is_authenticated:
        # If the user is an agent, get visits and paginate them
            try:
                agent = Agent.objects.get(user_id=request.user)
                visits = Visit.objects.filter(agent=agent.id).order_by('-date_created')
            except Agent.DoesNotExist:
                agent = None
                return redirect ('users:employees')
        else:
            return redirect('users:login')

        pk = request.GET.get('pk')
        
        week_plans = WeekPlan.objects.all().filter(agent=agent).order_by('-start_date')

        visits = Visit.objects.all().order_by('-date_created')
        paginator = Paginator(visits, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        agent_counties = []
        counties = County.objects.all().order_by('name')
    
        # Select only the counties from agent's zone  
        for county in counties:
            if county.zone == agent.zone:
                agent_counties.append(county)
    # The agent/user has no previous plans added, show blank form
        if not week_plans:
            plan = WeekPlan.objects.create(start_date=start_date, end_date=end_date, agent=agent, date_created=my_date)
        else:
    # The plan is selected from homepage dropdown, show plan with specific pk
            if pk != None:
                plan = WeekPlan.objects.get(id=pk)
    # Automaticlly load the plan where today is within start_date and end_date of the plan
            else:
                plan = WeekPlan.objects.get(start_date=start_date, agent=agent)	
            
        form = PlanForm(instance=plan)

        # get county for each day of the week
        if plan.monday_location != None:
            monday_location = int(plan.monday_location.id)
        elif request.GET.get('monday_location') != None:
            monday_location = int(request.GET.get('monday_location'))
        else:
            monday_location = None
        if plan.tuesday_location != None:
            tuesday_location = int(plan.tuesday_location.id)
        elif request.GET.get('tuesday_location') != None:
            tuesday_location = int(request.GET.get('tuesday_location'))
        else:
            tuesday_location = None
        if plan.wendsday_location != None:
            wendsday_location = int(plan.wendsday_location.id)
        elif request.GET.get('wendsday_location') != None:
            wendsday_location = int(request.GET.get('wendsday_location'))
        else:
            wendsday_location = None
        if plan.thursday_location != None:
            thursday_location = int(plan.thursday_location.id)
        elif request.GET.get('thursday_location') != None:
            thursday_location = int(request.GET.get('thursday_location'))
        else:
            thursday_location = None
        if plan.friday_location != None:
            friday_location = int(plan.friday_location.id)
        elif request.GET.get('friday_location') != None:
            friday_location = int(request.GET.get('friday_location'))
        else:
            friday_location = None

# Save changes to currently showed plan
    elif request.method == 'POST':
        form = PlanForm(request.POST, initial={'start_date': start_date, 'end_date': end_date})
        if form.is_valid():
            new_plan = form.save(commit=False)
            agent = Agent.objects.get(user_id=request.user.id)
            new_plan.agent_id = agent.id
            new_plan.start_date = request.POST.get('start_date')
            new_plan.end_date = request.POST.get('end_date')
            monday_location = request.POST.get('monday_location')
            tuesday_location = request.POST.get('tuesday_location')
            wendsday_location = request.POST.get('wendsday_location')
            thursday_location = request.POST.get('thursday_location')
            friday_location = request.POST.get('friday_location')

            new_plan.id = request.POST.get('plan_id')
            new_plan.save()
            monday_location = str(new_plan.monday_location.id)
            return redirect("/"+"?monday_location="+monday_location)
        else:
            print (form.errors)
    
    return render(request, 'sales/index.html', {
        'form': form,
        'plan': plan,
        'page_obj': page_obj,
        'week_plans': week_plans,
        'agent_counties': agent_counties,
        'monday_location': monday_location,
        'tuesday_location': tuesday_location,
        'wendsday_location': wendsday_location,
        'thursday_location': thursday_location,
        'friday_location': friday_location,
        'agent': agent,
    })


def add_plan(request):
    agent = Agent.objects.get(user_id=request.user.id)

    if request.method == "POST":
        form = PlanForm(data=request.POST)

        if form.is_valid():
            new_plan = form.save(commit=False)
            new_plan.agent_id = agent.id
            monday_location = request.POST.get('monday_location')
            tuesday_location = request.POST.get('tuesday_location')
            wendsday_location = request.POST.get('wendsday_location')
            thursday_location = request.POST.get('thursday_location')
            friday_location = request.POST.get('friday_location')
            new_plan.save()
        
        context = {
            'form': form, 
            'monday_location': monday_location,
            'tuesday_location': tuesday_location,
            'wendsday_location': wendsday_location,
            'thursday_location': thursday_location,
            'friday_location': friday_location,
        }
        return redirect('sales:index')

    elif request.method == "GET":
        form=PlanForm()
        agent_counties = []
        counties = County.objects.all().order_by('name')
        for county in counties:
            if county.zone == agent.zone:
                agent_counties.append(county)

        context = {'form': form, 'agent_counties': agent_counties}

    return render(request, 'sales/add_plan.html', context)


def plan(request, pk):
    plan = WeekPlan.objects.get(id=pk)
    form = PlanForm()
    return render(request, 'sales/plan.html', {'plan': plan, 'form': form})


def visits(request):
    agent = Agent.objects.get(user_id=request.user.id)
    visits = Visit.objects.filter(agent=agent.id).order_by('-date_created')
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


def select_client(request):
    source=request.GET.get('source')
    if request.method == "GET":
        agent_clients = []
        clients = Client.objects.all()
        agent = Agent.objects.get(user=request.user)
        for client in clients:
            if client.zone == agent.zone:
                agent_clients.append(client.name)
        context = {'agent_clients': agent_clients, 'source': source}
    
    elif request.method == "POST":
        client = request.POST.get('client')
        source = request.POST.get('source')
        context = {'client': client, 'source': source}
        return redirect('sales:select_shop', client, source)
    
    return render(request, 'sales/visits/select_client.html', context)


def select_shop(request, client, source):
    if request.method == "GET":
        client_obj = Client.objects.get(name=client)
        shop_list = client_obj.shop_set.all()
        context = {'shop_list': shop_list, 'client': client, 'source': source}
    elif request.method == "POST":
        shop_id = request.POST.get('shop')
        if source == 'visits':
            return redirect('sales:new_visit', shop_id=shop_id)
        else:
            return redirect('sales:priceinfo', shop_id=shop_id)

    return render(request, 'sales/visits/select_shop.html', context)


def new_visit(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == "GET":
        form=VisitForm()
        context = {'form': form, 'shop_id': shop_id, 'client_name': shop.client.name, 'shop_name': shop.name}

    elif request.method == "POST":
        form = VisitForm(request.POST, request.FILES)
        if form.is_valid():
            agent = Agent.objects.get(user_id=request.user.id)
            client = shop.client
            date_created = form.cleaned_data.get('date_created')
            shelf_image = form.cleaned_data.get('shelf_image')
            visit = Visit.objects.create(agent_id = agent.id, client_id = client.id, shop_id = shop.id, date_created = date_created, shelf_image = shelf_image)
            products = form.cleaned_data.get('products')
            for item in products:
                product = Product.objects.get(id=item)
                visit.products.add(product)
            return HttpResponseRedirect(reverse('sales:visits'))
        else:
            print(form.errors)
        
        context = {'form': form, 'visit': visit}

    return render(request, 'sales/visits/new_visit.html', context)


def info_competition(request):
    data = PriceEntry.objects.exclude(price_value=None)
    context = {'data': data}

    return render(request, 'sales/info_competition.html', context)

def plans_reports(request):
    agents = Agent.objects.all().order_by('zone').order_by('user')
    context = {'agents': agents}
    return render(request, 'sales/weeklyplan_reports/plans_reports.html', context)

def agent_plan_current(request, pk):
    try:
        plan = WeekPlan.objects.get(agent=pk, start_date=start_date)  
    except WeekPlan.DoesNotExist:
        plan = None
    except WeekPlan.MultipleObjectsReturned:
       plan = None
    
    context = {'plan': plan}
    return render(request, 'sales/weeklyplan_reports/agent_plan_current.html', context)

def agent_plan_history(request, pk):
    plans = WeekPlan.objects.filter(agent=pk).order_by('start_date')
    context = {'plans': plans}
    return render(request, 'sales/weeklyplan_reports/agent_plan_history.html', context)

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


### Info on competition section with generic views

class ProductInfoCreateView(CreateView):
    model = ProductInfo
    template_name = 'sales/productinfo/productinfo_new.html'
    fields = '__all__'
    context_object_name = 'productinfo'

class ProductInfoDetailView(DetailView):
    model = ProductInfo
    template_name = 'sales/productinfo/productinfo.html'
    context_object_name = 'productinfo'  

class ProductInfoListView(ListView):
    model = ProductInfo
    template_name = 'sales/productinfo/productinfo_list.html'
    fields = '__all__'
    context_object_name = 'productinfo_list'

class ProductInfoUpdateView(UpdateView):
    model = ProductInfo
    template_name = 'sales/productinfo/productinfo_edit.html'
    fields = '__all__'
    context_object_name = 'productinfo'

class ProductInfoDeleteView(DeleteView):
    model = ProductInfo
    template_name = 'sales/productinfo/productinfo_delete.html'
    success_url = reverse_lazy('sales:productinfo_list')


def price_info_collect(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    products = ProductInfo.objects.all().order_by('name')
    agent = Agent.objects.get(user_id=request.user.id)
    if request.method == "GET":
        context = {'shop_id': shop_id, 'client_name': shop.client.name, 'shop_name': shop.name, 'products': products}
    elif request.method == "POST":
        price_str = request.POST.getlist('price_value')
        price_map = map(int, price_str)
        price_values = list(price_map)
        x=0
        for product in products:
            price_entry = PriceEntry(price_value=price_values[x],product=product,agent=agent,client=shop.client,shop=shop)
            x=x+1
            if price_entry.price_value != 0:
                price_entry.save()
        context = {'price_entry': price_entry}
        return HttpResponseRedirect(reverse('sales:competition'))

    return render(request, 'sales/priceinfo/priceinfo.html', context)