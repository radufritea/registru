from django.urls import path
from . import views
from .views import ProductInfoCreateView, ProductInfoListView, ProductInfoDetailView, ProductInfoUpdateView, ProductInfoDeleteView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sales'
urlpatterns = [
	path('', views.index, name='index'),
	path('add_plan', views.add_plan, name="add_plan"),
	path('plan/<int:pk>', views.plan, name='plan'),
	path('visits', views.visits, name='visits'),
	path('visit/<int:visit_id>/', views.visit, name='visit'),
	path('visits/select_client', views.select_client, name='select_client'),
	path('visits/<str:client>/select_shop', views.select_shop, name='select_shop'),
	path('visits/<int:shop_id>/new_visit', views.new_visit, name='new_visit'),
	path('info_competition', views.info_competition, name='competition'),
	path('visits_reports', views.visits_reports, name='visits_reports'),
	path('competition_reports', views.competition_reports, name='competition_reports'),
	path('productinfo_list', ProductInfoListView.as_view(), name='productinfo_list'),
	path('productinfo/<int:pk>/', ProductInfoDetailView.as_view(), name='productinfo_detail'),
	path('productinfo/new/', ProductInfoCreateView.as_view(), name='productinfo_new'),
	path('productinfo/<int:pk>/edit/', ProductInfoUpdateView.as_view(), name='productinfo_edit'),
	path('productinfo/<int:pk>/delete/', ProductInfoDeleteView.as_view(), name='productinfo_delete'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)