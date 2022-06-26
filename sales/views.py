from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
import csv

from .models import (
    Visit,
    Agent,
    WeekPlan,
    Product,
    Client,
    Shop,
    County,
    ProductInfo,
    PriceEntry,
    Category,
    Producer,
)
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
                visits = Visit.objects.filter(agent=agent.id).order_by("-date_created")
            except Agent.DoesNotExist:
                agent = None
                return redirect("users:employees")
        else:
            return redirect("users:login")

        pk = request.GET.get("pk")

        week_plans = WeekPlan.objects.all().filter(agent=agent).order_by("-start_date")

        visits = Visit.objects.all().order_by("-date_created")
        paginator = Paginator(visits, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        agent_counties = []
        counties = County.objects.all().order_by("name")

        # Select only the counties from agent's zone
        for county in counties:
            if county.zone == agent.zone:
                agent_counties.append(county)
        # The agent/user has no previous plans added, show blank form
        if not week_plans:
            plan = WeekPlan.objects.create(
                start_date=start_date,
                end_date=end_date,
                agent=agent,
                date_created=my_date,
            )
        else:
            # The plan is selected from homepage dropdown, show plan with specific pk
            if pk != None:
                plan = WeekPlan.objects.get(id=pk)
            # Automaticlly load the plan where today is within start_date and end_date of the plan
            else:
                plan = WeekPlan.objects.filter(agent=agent).latest("start_date")

        form = PlanForm(instance=plan)

        # get county for each day of the week
        if plan.monday_location != None:
            monday_location = int(plan.monday_location.id)
        elif request.GET.get("monday_location") != None:
            monday_location = int(request.GET.get("monday_location"))
        else:
            monday_location = None
        if plan.tuesday_location != None:
            tuesday_location = int(plan.tuesday_location.id)
        elif request.GET.get("tuesday_location") != None:
            tuesday_location = int(request.GET.get("tuesday_location"))
        else:
            tuesday_location = None
        if plan.wendsday_location != None:
            wendsday_location = int(plan.wendsday_location.id)
        elif request.GET.get("wendsday_location") != None:
            wendsday_location = int(request.GET.get("wendsday_location"))
        else:
            wendsday_location = None
        if plan.thursday_location != None:
            thursday_location = int(plan.thursday_location.id)
        elif request.GET.get("thursday_location") != None:
            thursday_location = int(request.GET.get("thursday_location"))
        else:
            thursday_location = None
        if plan.friday_location != None:
            friday_location = int(plan.friday_location.id)
        elif request.GET.get("friday_location") != None:
            friday_location = int(request.GET.get("friday_location"))
        else:
            friday_location = None

    # Save changes to currently showed plan
    elif request.method == "POST":
        form = PlanForm(request.POST, initial={"start_date": start_date, "end_date": end_date})
        if form.is_valid():
            new_plan = form.save(commit=False)
            agent = Agent.objects.get(user_id=request.user.id)
            new_plan.agent_id = agent.id
            new_plan.start_date = request.POST.get("start_date")
            new_plan.end_date = request.POST.get("end_date")
            monday_location = request.POST.get("monday_location")
            tuesday_location = request.POST.get("tuesday_location")
            wendsday_location = request.POST.get("wendsday_location")
            thursday_location = request.POST.get("thursday_location")
            friday_location = request.POST.get("friday_location")

            new_plan.id = request.POST.get("plan_id")
            new_plan.save()
            monday_location = str(new_plan.monday_location.id)
            return redirect("/" + "?monday_location=" + monday_location)
        else:
            print(form.errors)

    return render(
        request,
        "sales/index.html",
        {
            "form": form,
            "plan": plan,
            "page_obj": page_obj,
            "week_plans": week_plans,
            "agent_counties": agent_counties,
            "monday_location": monday_location,
            "tuesday_location": tuesday_location,
            "wendsday_location": wendsday_location,
            "thursday_location": thursday_location,
            "friday_location": friday_location,
            "agent": agent,
        },
    )


def add_plan(request):
    agent = Agent.objects.get(user_id=request.user.id)

    if request.method == "POST":
        form = PlanForm(data=request.POST)

        if form.is_valid():
            new_plan = form.save(commit=False)
            new_plan.agent_id = agent.id
            monday_location = request.POST.get("monday_location")
            tuesday_location = request.POST.get("tuesday_location")
            wendsday_location = request.POST.get("wendsday_location")
            thursday_location = request.POST.get("thursday_location")
            friday_location = request.POST.get("friday_location")
            new_plan.save()

        context = {
            "form": form,
            "monday_location": monday_location,
            "tuesday_location": tuesday_location,
            "wendsday_location": wendsday_location,
            "thursday_location": thursday_location,
            "friday_location": friday_location,
        }
        return redirect("sales:index")

    elif request.method == "GET":
        form = PlanForm()
        agent_counties = []
        counties = County.objects.all().order_by("name")
        for county in counties:
            if county.zone == agent.zone:
                agent_counties.append(county)

        context = {"form": form, "agent_counties": agent_counties}

    return render(request, "sales/add_plan.html", context)


def plan(request, pk):
    plan = WeekPlan.objects.get(id=pk)
    form = PlanForm()
    return render(request, "sales/plan.html", {"plan": plan, "form": form})


def visits(request):
    agent = Agent.objects.get(user_id=request.user.id)
    visits = Visit.objects.filter(agent=agent.id).order_by("-date_created")
    paginator = Paginator(visits, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "sales/visits.html", {"page_obj": page_obj})


def visit(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    products = visit.products.all()
    products_ordered = visit.products_ordered.all()
    return render(
        request,
        "sales/visit.html",
        {"visit": visit, "products": products, "products_ordered": products_ordered},
    )


def select_client(request):
    source = request.GET.get("source")
    if request.method == "GET":
        agent_clients = []
        clients = Client.objects.all()
        agent = Agent.objects.get(user=request.user)
        for client in clients:
            if client.zone == agent.zone:
                agent_clients.append(client.name)
        context = {"agent_clients": agent_clients, "source": source}

    elif request.method == "POST":
        client = request.POST.get("client")
        source = request.POST.get("source")
        context = {"client": client, "source": source}
        return redirect("sales:select_shop", client, source)

    return render(request, "sales/visits/select_client.html", context)


def select_shop(request, client, source):
    if request.method == "GET":
        client_obj = Client.objects.get(name=client)
        shop_list = client_obj.shop_set.all()
        context = {"shop_list": shop_list, "client": client, "source": source}
    elif request.method == "POST":
        shop_id = request.POST.get("shop")
        if source == "visits":
            return redirect("sales:new_visit", shop_id=shop_id)
        else:
            return redirect("sales:priceinfo", shop_id=shop_id)

    return render(request, "sales/visits/select_shop.html", context)


def new_visit(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == "GET":
        form = VisitForm()
        context = {
            "form": form,
            "shop_id": shop_id,
            "client_name": shop.client.name,
            "shop_name": shop.name,
        }

    elif request.method == "POST":
        form = VisitForm(request.POST, request.FILES)
        if form.is_valid():
            agent = Agent.objects.get(user_id=request.user.id)
            client = shop.client
            date_created = form.cleaned_data.get("date_created")
            shelf_image = form.cleaned_data.get("shelf_image")
            quantity_ordered = form.cleaned_data.get("quantity_ordered")
            observations = form.cleaned_data.get("observations")
            visit = Visit.objects.create(
                agent_id=agent.id,
                client_id=client.id,
                shop_id=shop.id,
                date_created=date_created,
                shelf_image=shelf_image,
                quantity_ordered=quantity_ordered,
                observations=observations,
            )
            products = form.cleaned_data.get("products")
            for item in products:
                product = Product.objects.get(id=item)
                visit.products.add(product)

            ordered_products = form.cleaned_data.get("products_ordered")
            for item in ordered_products:
                product = Product.objects.get(id=item)
                visit.products_ordered.add(product)
            return HttpResponseRedirect(reverse("sales:visits"))
        else:
            print(form.errors)

        context = {"form": form, "visit": visit}

    return render(request, "sales/visits/new_visit.html", context)


def info_competition(request):
    data = PriceEntry.objects.exclude(price_value=None)
    context = {"data": data}
    return render(request, "sales/info_competition.html", context)


### Info on competition section with generic views
class ProductInfoCreateView(CreateView):
    model = ProductInfo
    template_name = "sales/productinfo/productinfo_new.html"
    fields = "__all__"
    context_object_name = "productinfo"


class ProductInfoDetailView(DetailView):
    model = ProductInfo
    template_name = "sales/productinfo/productinfo.html"
    context_object_name = "productinfo"


class ProductInfoListView(ListView):
    model = ProductInfo
    template_name = "sales/productinfo/productinfo_list.html"
    fields = "__all__"
    context_object_name = "productinfo_list"


class ProductInfoUpdateView(UpdateView):
    model = ProductInfo
    template_name = "sales/productinfo/productinfo_edit.html"
    fields = "__all__"
    context_object_name = "productinfo"


class ProductInfoDeleteView(DeleteView):
    model = ProductInfo
    template_name = "sales/productinfo/productinfo_delete.html"
    success_url = reverse_lazy("sales:productinfo_list")


# Add information about competition prices
def price_info_collect(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    products = ProductInfo.objects.all().order_by("name")
    agent = Agent.objects.get(user_id=request.user.id)
    if request.method == "GET":
        context = {
            "shop_id": shop_id,
            "client_name": shop.client.name,
            "shop_name": shop.name,
            "products": products,
        }
    elif request.method == "POST":
        price_str = request.POST.getlist("price_value")
        price_map = map(int, price_str)
        price_values = list(price_map)
        x = 0
        for product in products:
            price_entry = PriceEntry(
                price_value=price_values[x],
                product=product,
                agent=agent,
                client=shop.client,
                shop=shop,
            )
            x = x + 1
            if price_entry.price_value != 0:
                price_entry.save()
        context = {"price_entry": price_entry}
        return HttpResponseRedirect(reverse("sales:competition"))

    return render(request, "sales/priceinfo/priceinfo.html", context)


# Weekly Plans reports (select between current week and historical data)
def plans_reports(request):
    agents = Agent.objects.all().order_by("zone").order_by("user")
    context = {"agents": agents}
    return render(request, "sales/weeklyplan_reports/plans_reports.html", context)


def agent_plan_current(request, pk):
    try:
        plan = WeekPlan.objects.get(agent=pk, start_date=start_date)
    except WeekPlan.DoesNotExist:
        plan = None
    except WeekPlan.MultipleObjectsReturned:
        plan = None

    context = {"plan": plan}
    return render(request, "sales/weeklyplan_reports/agent_plan_current.html", context)


def agent_plan_history(request, pk):
    plans = WeekPlan.objects.filter(agent=pk).order_by("start_date")
    context = {"plans": plans}
    return render(request, "sales/weeklyplan_reports/agent_plan_history.html", context)


# Reports on competition pricing
def competition_reports(request):

    agents = Agent.objects.all().order_by("user")
    products = ProductInfo.objects.all().order_by("name")
    categories = Category.objects.all().order_by("name")
    producers = Producer.objects.all().order_by("name")

    context = {
        "agents": agents,
        "products": products,
        "categories": categories,
        "producers": producers,
    }
    return render(request, "sales/competition_reports/filter.html", context)


def by_product_and_agent(request):
    agent = request.GET.get("a")
    product = request.GET.get("p")

    if agent and product:
        items = PriceEntry.objects.filter(agent=agent, product=product)
    elif product and not agent:
        items = PriceEntry.objects.filter(product=product)
    else:
        items = PriceEntry.objects.all()

    context = {"items": items}
    return render(request, "sales/competition_reports/by_product_and_agent.html", context)


def by_category_and_agent(request):
    category = request.GET.get("cat")
    agent = request.GET.get("a")

    if agent and category:
        items = PriceEntry.objects.filter(agent=agent, product__category=category)
    elif category and not agent:
        items = PriceEntry.objects.filter(product__category=category)
    else:
        items = PriceEntry.objects.all()

    context = {"items": items}
    return render(request, "sales/competition_reports/by_category_and_agent.html", context)


def by_producer_and_agent(request):
    producer = request.GET.get("pr")
    agent = request.GET.get("a")

    if agent and producer:
        items = PriceEntry.objects.filter(agent=agent, product__producer=producer)
    elif producer and not agent:
        items = PriceEntry.objects.filter(product__producer=producer)
    else:
        items = PriceEntry.objects.all()

    context = {"items": items}
    return render(request, "sales/competition_reports/by_producer_and_agent.html", context)


def export_competition(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="competition_report.csv"'

    writer = csv.writer(response)

    # Define and write csv header
    header = [
        "Magazin",
        "Producător",
        "Brand",
        "Produs",
        "Gramaj",
        "Pret",
        "Data",
        "Gama",
        "Agent",
    ]
    writer.writerow(header)

    # Get database information
    items = PriceEntry.objects.all()

    # # Define each row
    for item in items:
        row = [
            item.shop,
            item.product.producer,
            item.product.brand,
            item.product.name,
            item.product.weight,
            item.price_value,
            item.date_created,
            item.product.category,
            item.agent,
        ]
        writer.writerow(row)

    return response


# Storechecks (visits) reports
def visits_reports(request):
    agents = Agent.objects.all().order_by("user")
    clients = Client.objects.all().order_by("name")
    shops = Shop.objects.all().order_by("name")
    products = Product.objects.all().order_by("name")
    context = {
        "agents": agents,
        "clients": clients,
        "shops": shops,
        "products": products,
    }
    return render(request, "sales/storecheck_reports/visits_reports.html", context)


def visits_by_agent_and_client(request):
    agent = request.GET.get("a")
    client = request.GET.get("c")
    shop = request.GET.get("s")

    if agent and client and shop:
        visits = Visit.objects.filter(agent=agent, client=client, shop=shop)
        selected_agent = Agent.objects.get(pk=agent)
    elif agent and client and not shop:
        visits = Visit.objects.filter(agent=agent, client=client)
        selected_agent = Agent.objects.get(pk=agent)
    elif agent and shop and not client:
        visits = Visit.objects.filter(agent=agent, shop=shop)
        selected_agent = Agent.objects.get(pk=agent)
    elif client and shop and not agent:
        visits = Visit.objects.filter(client=client, shop=shop)
        selected_agent = "toti agentii"
    elif agent and not client and not shop:
        visits = Visit.objects.filter(agent=agent)
        selected_agent = Agent.objects.get(pk=agent)
    elif client and not agent and not shop:
        visits = Visit.objects.filter(client=client)
        selected_agent = "toti agentii"
    elif shop and not agent and not client:
        visits = Visit.objects.filter(shop=shop)
        selected_agent = "toti agentii"
    else:
        visits = Visit.objects.all().order_by("-date_created")
        selected_agent = "toti agentii"

    context = {"visits": visits, "agent": selected_agent}
    return render(request, "sales/storecheck_reports/by_agent_and_client.html", context)


def visits_by_product(request):
    product = Product.objects.get(id=request.GET.get("p"))
    visits = Visit.objects.all()
    locations = []
    for visit in visits:
        items = visit.products.all()
        if product in items:
            locations.append(visit)
    context = {"locations": locations}
    return render(request, "sales/storecheck_reports/by_product.html", context)


def export_storechecks(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="storechecks_report.csv"'

    writer = csv.writer(response)

    # Get database information
    items = Visit.objects.all()

    # Define and write csv header
    products = Product.objects.all().order_by("name")
    product_list = products.values_list("name", flat=True)
    header = [
        "Agent",
        "Client",
        "Magazin",
        "Data",
        "Produse prezente",
        "Produse comandate",
        "Baxuri",
    ]
    for product in product_list:
        header.append(f"R_{product}")
    for product in product_list:
        header.append(f"O_{product}")
    header.append("Observatii")
    writer.writerow(header)

    # Define each row
    for visit in items:
        row = []

        # Add a client, shop, date
        row.extend([visit.agent, visit.client, visit.shop, visit.date_created])

        # Add an X for each product that was on the shelf at that visit
        visit_products = visit.products.values_list("name", flat=True)
        visit_order_products = visit.products_ordered.values_list("name", flat=True)
        row.extend([len(visit_products), len(visit_order_products), visit.quantity_ordered])

        for product in product_list:
            if product in visit_products:
                row.append("X")
            else:
                row.append("")

        for product in product_list:
            if product in visit_order_products:
                row.append("X")
            else:
                row.append("")
        row.append(visit.observations)
        writer.writerow(row)

    return response
