from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sales'
urlpatterns = [
	path('', views.index, name='index'),
	path('add_plan', views.add_plan, name="add_plan"),
	path('plan/<int:pk>', views.plan, name='plan'),
	path('visits', views.visits, name='visits'),
	path('visit/<int:visit_id>/', views.visit, name='visit'),
	path('new_visit', views.new_visit, name='new_visit'),
	path('info_competition', views.info_competition, name='competition'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)